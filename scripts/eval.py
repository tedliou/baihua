"""分層執行 eval，從題庫抽考，並和 baseline 比較分數。

用法：
  python scripts/eval.py L1 --tag false-positive      改 skill 時，只跑相關的題目
  python scripts/eval.py L2                           發 release 前：固定題、抽考 8 題、trigger
  python scripts/eval.py L3 --update-baseline         換模型時：全部題目加 without-skill，重建 baseline
  python scripts/eval.py L2 --dry-run                 只列出會跑哪些題目，不花額度
  python scripts/eval.py compare <aggregate-result.json>

私有題庫放在 repo 之外，用 --private <資料夾> 合併進來。資料夾裡可以放：
  <題目>/prompt.md、<題目>/graders/*.md   和 eval-bank 相同的格式
  baseline.json                          私有題的基準分數
  forbidden.txt                          一行一個不得出現在公開題目裡的字串

只用 Python 標準函式庫。
"""

import argparse
import fnmatch
import json
import random
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
CATEGORIES = ["ai-flavor", "translationese", "glossary", "core-rule"]
SAMPLE_SIZE = 8
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


def sample(bank, size, rng):
    """每個類別至少抽一題，剩下的名額從其餘題目隨機抽。"""
    pool = list(bank)
    picked = []
    for cat in CATEGORIES:
        candidates = [c for c in pool if c.category == cat]
        if candidates and len(picked) < size:
            choice = rng.choice(candidates)
            picked.append(choice)
            pool.remove(choice)
    rest = rng.sample(pool, min(size - len(picked), len(pool)))
    return sorted(picked + rest, key=lambda c: c.name)


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
    """把題目複製到一個暫存的 eval 目錄。題庫題會加上共用的評分項。"""
    target.mkdir(parents=True)
    for case in cases:
        dest = target / case.name
        shutil.copytree(case.path, dest)
        if case.path.parent == FIXED_DIR:
            continue
        for g in COMMON_GRADERS.glob("*.md"):
            if g.stem == "cjk-latin-spacing" and "no-spacing" in case.tags:
                continue
            if g.stem == "fullwidth-punctuation" and "keep-punct" in case.tags:
                continue
            shutil.copy(g, dest / "graders" / f"common-{g.name}")


def run_group(stamp, group, cases, ablation, args):
    if not cases:
        return None
    eval_dir = RUN_DIR / stamp / group
    out_dir = RUN_DIR / stamp / f"{group}-result"
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
        "--ablation", ablation,
        "--runs", str(args.runs),
        "-j", str(args.jobs),
        "--threshold", "0",
        "--no-publish",
        "--trust-plugin",
    ]
    print(f"\n== {group}：{len(cases)} 題，ablation {ablation}")
    subprocess.run(cmd, cwd=ROOT, check=False)
    result = out_dir / "aggregate-result.json"
    return result if result.is_file() else None


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
            "without": round(agg["scoreWithout"], 3) if "scoreWithout" in agg else None,
            "trigger": "trigger" in case["dir"] or case["name"].startswith("trigger-"),
        }
    return out, data.get("costUsd", 0)


def compare(results, baseline):
    """回傳退化的題目清單。單題下降 CASE_DROP 以上，或平均下降 MEAN_DROP 以上，都算退化。"""
    problems, drops = [], []
    print(f"\n{'題目':<40}{'基準':>8}{'這次':>8}{'差':>8}")
    for name, s in sorted(results.items()):
        if s["trigger"]:
            if s["with"] < 1:
                problems.append(f"{name}：trigger 判斷錯誤（{s['with']}）")
            continue
        base = baseline.get(name, {}).get("with")
        diff = "" if base is None else f"{s['with'] - base:+.2f}"
        print(f"{name:<40}{'' if base is None else base:>8}{s['with']:>8}{diff:>8}")
        if base is None:
            continue
        drops.append(base - s["with"])
        if base - s["with"] >= CASE_DROP:
            problems.append(f"{name}：{base} → {s['with']}")
    if drops and sum(drops) / len(drops) >= MEAN_DROP:
        problems.append(f"平均下降 {sum(drops) / len(drops):.3f}")
    return problems


def write_baseline(results, private_dir, claude_version):
    stamp = time.strftime("%Y-%m-%d")
    public = {n: s for n, s in results.items() if not n.startswith("p-") and not s["trigger"]}
    private = {n: s for n, s in results.items() if n.startswith("p-")}
    targets = [(BASELINE, public)]
    if private_dir and private:
        targets.append((private_dir / "baseline.json", private))
    for path, cases in targets:
        old = json.loads(path.read_text(encoding="utf-8"))["cases"] if path.is_file() else {}
        for n, s in cases.items():
            without = s["without"] if s["without"] is not None else old.get(n, {}).get("without")
            old[n] = {"with": s["with"], "without": without}
        body = {"model": MODEL, "claudeVersion": claude_version, "updated": stamp, "cases": dict(sorted(old.items()))}
        path.write_text(json.dumps(body, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"已更新 {path}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("tier", choices=["L1", "L2", "L3", "compare"])
    parser.add_argument("result", nargs="?", help="compare 用：aggregate-result.json 的路徑")
    parser.add_argument("--tag", nargs="*", default=[], help="L1：要跑的 tag")
    parser.add_argument("--case", nargs="*", default=[], help="L1：要跑的題目名稱，可用 glob")
    parser.add_argument("--private", type=Path, help="私有題庫資料夾")
    parser.add_argument("--sample", type=int, default=SAMPLE_SIZE, help="L2 抽考題數")
    parser.add_argument("--seed", type=int, help="抽題用的 seed，預設用目前時間")
    parser.add_argument("--runs", type=int, default=1)
    parser.add_argument("-j", "--jobs", type=int, default=4)
    parser.add_argument("--with-without", action="store_true", help="L1：也跑沒有 skill 的一組，用來補基準")
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

    fixed = load_cases(FIXED_DIR)
    bank = [c for c in load_cases(BANK_DIR) if c.path.name != "_common"]
    if args.private:
        bank += load_cases(args.private, private=True)
        check_forbidden(args.private, fixed + bank)

    behavior = [c for c in fixed if "behavior" in c.tags]
    trigger = [c for c in fixed if "trigger" in c.tags]
    seed = args.seed if args.seed is not None else int(time.time())

    if args.tier == "L1":
        if not args.tag and not args.case:
            parser.error("L1 需要 --tag 或 --case")
        ablation = "with-without" if args.with_without else "none"
        groups = [
            ("behavior", [c for c in behavior + bank if matches(c, args.tag, args.case)], ablation),
            ("trigger", [c for c in trigger if matches(c, args.tag, args.case)], "none"),
        ]
    elif args.tier == "L2":
        picked = sample(bank, args.sample, random.Random(seed))
        groups = [("behavior", behavior + picked, "none"), ("trigger", trigger, "none")]
        print(f"抽考 seed：{seed}")
    else:
        groups = [("behavior", behavior + bank, "with-without"), ("trigger", trigger, "none")]

    for group, cases, ablation in groups:
        print(f"{group}（{ablation}）：{len(cases)} 題")
        for c in cases:
            print(f"  {c.name}  [{', '.join(c.tags)}]")
    if args.dry_run:
        return

    stamp = time.strftime("%Y%m%d-%H%M%S")
    results, cost, version = {}, 0.0, ""
    for group, cases, ablation in groups:
        path = run_group(stamp, group, cases, ablation, args)
        if cases and not path:
            sys.exit(f"{group} 沒有產生結果，請看上面 claude plugin eval 的輸出。")
        if path:
            r, c = scores(path)
            results.update(r)
            cost += c
            version = json.loads(path.read_text(encoding="utf-8")).get("claudeVersion", version)

    manifest = {"tier": args.tier, "seed": seed, "costUsd": round(cost, 2), "scores": results}
    (RUN_DIR / stamp / "summary.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n費用約 {cost:.2f} 美元，結果在 {RUN_DIR / stamp}")

    if args.update_baseline:
        write_baseline(results, args.private, version)
        return
    problems = compare(results, load_baseline(args.private))
    print("\n".join(["", "退化："] + problems) if problems else "\n沒有退化。")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
