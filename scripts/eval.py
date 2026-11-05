"""執行 eval，並和 baseline 比較分數。

每一題都是一段明顯是 AI 寫的文字，測 skill 能不能把它改成像人寫的。題目開頭會加上
「使用 zh-tw-prose skill。」，只跑有 skill 的一組。

用法：
  python scripts/eval.py L1 --case <題目…>            改 skill 時，只跑相關的題目（--tag 也可以）
  python scripts/eval.py L2                           發 release 前：跑全部題目
  python scripts/eval.py L2 --update-baseline         重建 baseline
  python scripts/eval.py L2 --dry-run                 只列出會跑哪些題目，不花額度
  python scripts/eval.py compare <aggregate-result.json>

每次執行都把每題的輸出存成 eval-run/<時間>/outputs/<題目>.txt，方便人工審閱。

私有題庫放在 repo 之外，用 --private <資料夾> 合併進來。資料夾裡可以放：
  <題目>/prompt.md、<題目>/graders/*.md   和 eval-bank 相同的格式
  baseline.json                          私有題的基準分數
  forbidden.txt                          一行一個不得出現在公開題目裡的字串

只用 Python 標準函式庫。
"""

import argparse
import fnmatch
import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXED_DIR = ROOT / "evals"
BANK_DIR = ROOT / "eval-bank"
COMMON_GRADERS = BANK_DIR / "_common" / "graders"
RUN_DIR = ROOT / "eval-run"
BASELINE = FIXED_DIR / "baseline.json"

MODEL = "sonnet"
INVOKE = "使用 zh-tw-prose skill。"
CATEGORIES = ["ai-flavor", "translationese", "glossary", "core-rule"]
CASE_DROP = 0.17
MEAN_DROP = 0.03


class Case:
    def __init__(self, path, private=False):
        self.path = path
        self.private = private
        self.name = ("p-" if private else "") + path.name
        text = (path / "prompt.md").read_text(encoding="utf-8")
        m = re.search(r"^tags:\s*\[(.*?)\]", text, re.M)
        self.tags = [t.strip() for t in m.group(1).split(",")] if m else []
        self.text = text

    @property
    def category(self):
        return next((t for t in self.tags if t in CATEGORIES), None)


def load_cases(directory, private=False):
    if not directory.is_dir():
        return []
    return [
        Case(p, private)
        for p in sorted(directory.iterdir())
        if (p / "prompt.md").is_file()
    ]


def matches(case, tags, globs):
    if tags and set(tags) & set(case.tags):
        return True
    return any(fnmatch.fnmatch(case.name, g) for g in globs)


def check_forbidden(private_dir, cases):
    path = private_dir / "forbidden.txt"
    if not path.is_file():
        return
    words = [w.strip() for w in path.read_text(encoding="utf-8").splitlines() if w.strip()]
    leaks = []
    for case in cases:
        if case.private:
            continue
        for f in case.path.rglob("*.md"):
            body = f.read_text(encoding="utf-8")
            leaks += [f"{f.relative_to(ROOT)}：{w}" for w in words if w in body]
    if leaks:
        sys.exit("公開題目出現私有字串，先移到私有題庫：\n" + "\n".join(leaks))


def assemble(target, cases):
    """把題目複製到一個暫存的 eval 目錄。

    每題開頭加上 INVOKE，照實際用法由使用者或其他 skill 寫明使用本 skill。題庫題另外加上共用的評分項。
    """
    target.mkdir(parents=True)
    for case in cases:
        dest = target / case.name
        shutil.copytree(case.path, dest)
        prompt = dest / "prompt.md"
        head, front, body = prompt.read_text(encoding="utf-8").split("---", 2)
        prompt.write_text(f"{head}---{front}---\n\n{INVOKE}\n\n{body.lstrip()}", encoding="utf-8")
        if case.path.parent == FIXED_DIR:
            continue
        (dest / "graders").mkdir(exist_ok=True)
        for g in COMMON_GRADERS.glob("*.md"):
            if g.stem == "cjk-latin-spacing" and "no-spacing" in case.tags:
                continue
            if g.stem == "fullwidth-punctuation" and "keep-punct" in case.tags:
                continue
            if g.stem == "author-rubric":
                # llm 評審只看得到最後的回覆，把題目與原文寫進評分表，評審才能對照任務要求與原文。
                g_head, g_front, g_body = g.read_text(encoding="utf-8").split("---", 2)
                task = case.text.split("---", 2)[2].strip()
                text = f"{g_head}---{g_front}---\n\n# 題目（任務說明與原文）\n\n{task}\n\n# 評分條件\n\n{g_body.strip()}\n"
                (dest / "graders" / f"common-{g.name}").write_text(text, encoding="utf-8")
                continue
            shutil.copy(g, dest / "graders" / f"common-{g.name}")


def run_group(stamp, group, cases, args):
    if not cases:
        return None
    eval_dir = RUN_DIR / stamp / group
    out_dir = RUN_DIR / stamp / f"{group}-result"
    full = RUN_DIR / stamp / f"{group}-full.json"
    assemble(eval_dir, cases)
    claude = shutil.which("claude")
    if not claude:
        sys.exit("找不到 claude 指令。")
    cmd = [
        claude, "plugin", "eval", ".",
        "--eval-dir", eval_dir.relative_to(ROOT).as_posix(),
        "--output-dir", str(out_dir),
        "--model", MODEL,
        "--judge-model", MODEL,
        "--ablation", "none",
        "--runs", str(args.runs),
        "-j", str(args.jobs),
        "--threshold", "0",
        "--no-publish",
        "--trust-plugin",
        "--keep-temp",
        "--json", str(full),
    ]
    print(f"\n== {group}：{len(cases)} 題")
    subprocess.run(cmd, cwd=ROOT, check=False)
    if full.is_file():
        save_outputs(full, RUN_DIR / stamp / "outputs")
    result = out_dir / "aggregate-result.json"
    return result if result.is_file() else None


def save_outputs(full_json, target):
    """從每次執行的 trace 取出最後的回覆存成文字檔，再刪掉 --keep-temp 留下的暫存資料夾。"""
    target.mkdir(parents=True, exist_ok=True)
    data = json.loads(full_json.read_text(encoding="utf-8"))
    reads = {}
    for case in data.get("cases", []):
        arms = case["arms"]
        runs = arms.get("with", []) if isinstance(arms, dict) else arms
        for n, run in enumerate(runs, 1):
            trace = Path(run.get("tracePath") or "")
            text = ""
            if trace.is_file():
                for line in trace.read_text(encoding="utf-8").splitlines():
                    try:
                        event = json.loads(line)
                    except ValueError:
                        continue
                    if not isinstance(event, dict):
                        continue
                    if event.get("type") == "result":
                        text = event.get("result") or ""
                    for block in (event.get("message") or {}).get("content") or []:
                        if isinstance(block, dict) and block.get("type") == "tool_use" and block.get("name") == "Read":
                            path = str((block.get("input") or {}).get("file_path", ""))
                            reads.setdefault(case["name"], []).append(path.split("zh-tw-prose/")[-1])
            suffix = f"-{n}" if len(runs) > 1 else ""
            (target / f"{case['name']}{suffix}.txt").write_text(text.strip() + "\n", encoding="utf-8")
            temp = trace.parents[1] if len(trace.parents) > 1 else None
            if temp is not None and temp.name.startswith("claude-eval-") and temp.is_dir():
                for p in sorted(temp.rglob("*"), key=lambda q: len(q.parts), reverse=True):
                    try:
                        p.chmod(0o700) if p.is_dir() else p.chmod(0o600)
                    except OSError:
                        pass
                shutil.rmtree(temp, ignore_errors=True)
    names = [c["name"] for c in data.get("cases", [])]
    read_register = [n for n in names if any("registers/" in r for r in reads.get(n, []))]
    summary = {"read_register": f"{len(read_register)}/{len(names)}", "reads": {n: reads.get(n, []) for n in names}}
    (target / "_reads.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"讀了語域檔案的題目：{summary['read_register']}")


def load_baseline(private_dir):
    base = {}
    for path in [BASELINE] + ([private_dir / "baseline.json"] if private_dir else []):
        if path.is_file():
            base.update(json.loads(path.read_text(encoding="utf-8"))["cases"])
    return base


def scores(result_path):
    data = json.loads(Path(result_path).read_text(encoding="utf-8"))
    out = {}
    for case in data["cases"]:
        agg = case["aggregates"]
        out[case["name"]] = {
            "with": round(agg["score"], 3),
        }
    return out, data.get("costUsd", 0)


def compare(results, baseline):
    """回傳退化清單。平均下降 MEAN_DROP 以上算退化。

    單題分數在兩次執行之間可能差到 0.3，所以單題下降 CASE_DROP 以上只列出來提醒，不算退化。
    """
    problems, drops, notes = [], [], []
    print(f"\n{'題目':<40}{'基準':>8}{'這次':>8}{'差':>8}")
    for name, s in sorted(results.items()):
        base = baseline.get(name, {}).get("with")
        diff = "" if base is None else f"{s['with'] - base:+.2f}"
        print(f"{name:<40}{'' if base is None else base:>8}{s['with']:>8}{diff:>8}")
        if base is None:
            continue
        drops.append(base - s["with"])
        if base - s["with"] >= CASE_DROP:
            notes.append(f"{name}：{base} → {s['with']}")
    if drops:
        mean = sum(drops) / len(drops)
        print(f"\n平均變化 {-mean:+.3f}（{len(drops)} 題）")
        if mean >= MEAN_DROP:
            problems.append(f"平均下降 {mean:.3f}")
    if notes:
        print("\n單題下降較多，可以用 --case 加 --runs 3 確認：\n" + "\n".join(notes))
    return problems


def write_baseline(results, private_dir, claude_version, keep=None):
    """把分數寫進 baseline。keep 是現有題目的名稱集合，給了就順便刪掉已經不在題庫的題目。"""
    stamp = time.strftime("%Y-%m-%d")
    public = {n: s for n, s in results.items() if not n.startswith("p-")}
    private = {n: s for n, s in results.items() if n.startswith("p-")}
    targets = [(BASELINE, public)]
    if private_dir and private:
        targets.append((private_dir / "baseline.json", private))
    for path, cases in targets:
        old = json.loads(path.read_text(encoding="utf-8"))["cases"] if path.is_file() else {}
        if keep is not None:
            old = {n: v for n, v in old.items() if n in keep}
        for n, s in cases.items():
            old[n] = {"with": s["with"]}
        body = {"model": MODEL, "claudeVersion": claude_version, "updated": stamp, "cases": dict(sorted(old.items()))}
        path.write_text(json.dumps(body, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"已更新 {path}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("tier", choices=["L1", "L2", "compare"])
    parser.add_argument("result", nargs="?", help="compare 用：aggregate-result.json 的路徑")
    parser.add_argument("--tag", nargs="*", default=[], help="L1：要跑的 tag")
    parser.add_argument("--case", nargs="*", default=[], help="L1：要跑的題目名稱，可用 glob")
    parser.add_argument("--private", type=Path, help="私有題庫資料夾")
    parser.add_argument("--runs", type=int, default=1)
    parser.add_argument("-j", "--jobs", type=int, default=4)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--update-baseline", action="store_true")
    args = parser.parse_args()

    if args.tier == "compare":
        if not args.result:
            parser.error("compare 需要 aggregate-result.json 的路徑")
        results, _ = scores(args.result)
        problems = compare(results, load_baseline(args.private))
        print("\n".join(["", "退化："] + problems) if problems else "\n沒有退化。")
        sys.exit(1 if problems else 0)

    bank = [c for c in load_cases(BANK_DIR) if c.path.name != "_common"]
    if args.private:
        bank += load_cases(args.private, private=True)
        check_forbidden(args.private, bank)

    if args.tier == "L1":
        if not args.tag and not args.case:
            parser.error("L1 需要 --tag 或 --case")
        cases = [c for c in bank if matches(c, args.tag, args.case)]
    else:
        cases = bank

    print(f"{len(cases)} 題")
    for c in cases:
        print(f"  {c.name}  [{', '.join(c.tags)}]")
    if args.dry_run:
        return

    stamp = time.strftime("%Y%m%d-%H%M%S")
    path = run_group(stamp, "bank", cases, args)
    if not path:
        sys.exit("沒有產生結果，請看上面 claude plugin eval 的輸出。")
    results, cost = scores(path)
    version = json.loads(path.read_text(encoding="utf-8")).get("claudeVersion", "")

    manifest = {"tier": args.tier, "costUsd": round(cost, 2), "scores": results}
    (RUN_DIR / stamp / "summary.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n費用約 {cost:.2f} 美元，結果在 {RUN_DIR / stamp}，每題的輸出在 outputs/")

    if args.update_baseline:
        keep = {c.name for c in bank} if args.tier == "L2" else None
        write_baseline(results, args.private, version, keep)
        return
    problems = compare(results, load_baseline(args.private))
    print("\n".join(["", "退化："] + problems) if problems else "\n沒有退化。")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
