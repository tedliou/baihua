"""盲測配對：同一題分別跑有 skill 與沒有 skill，由人挑哪一個寫得好。

寫作的好壞要靠人判斷，模型評審只當參考。流程：

  python scripts/blind.py run   --out <資料夾> --cases <題目…> [--private <私有題庫>]
      跑兩組、各 1 次，存下輸出與機械檢查結果，A、B 隨機排列
  python scripts/blind.py judge --out <資料夾>
      模型評審：每組配對交換順序各評一次，兩次結論不同算平手
  python scripts/blind.py page  --out <資料夾>
      產生 review.html，在瀏覽器打開後逐題選擇，最後下載 feedback.json 放進同一個資料夾
  python scripts/blind.py stats --out <資料夾>
      計算勝率、機械檢查通過率，以及模型評審和人的一致率

--out 放在 repo 之外，因為裡面可能有私有題。哪一邊是有 skill 的版本記在 key.json，審完之前不要打開。
只用 Python 標準函式庫。
"""

import argparse
import html
import json
import math
import random
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import eval as runner  # noqa: E402

CHECK = ROOT / "skills" / "zh-tw-prose" / "scripts" / "check.py"
JUDGE_BATCH = 6


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save_json(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")


def prompt_body(case):
    return case.text.split("---", 2)[2].strip()


def read_trace(trace):
    """回傳最後一段回覆文字，以及有沒有呼叫 Skill。"""
    text, used = None, False
    if not trace or not Path(trace).is_file():
        return None, False
    for line in Path(trace).read_text(encoding="utf-8").splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        msg = event.get("message") if isinstance(event, dict) else None
        if isinstance(msg, dict) and event.get("type") == "assistant" and isinstance(msg.get("content"), list):
            for block in msg["content"]:
                if isinstance(block, dict) and block.get("type") == "text":
                    text = block["text"]
                if isinstance(block, dict) and block.get("type") == "tool_use" and block.get("name") == "Skill":
                    used = True
    return text, used


def facts(body):
    """原文裡必須原樣保留的東西：網址與行內程式碼。表格列不算，因為那多半是用詞表。"""
    lines = [l for l in body.splitlines() if not l.lstrip().startswith("|")]
    text = "\n".join(lines)
    return sorted(set(re.findall(r"https?://[^\s)）]+", text)) | set(re.findall(r"`[^`\n]+`", text)))


def mechanical(body, output, regex_results, tags):
    if output is None:
        return {"ok": False, "issues": ["沒有輸出"]}
    issues = [f"評分項 {name} 沒通過" for name, ok in regex_results if not ok]
    issues += [f"少了 {f}" for f in facts(body) if f not in output]
    tmp = ROOT / "eval-run" / "_check.md"
    tmp.write_text(output, encoding="utf-8")
    flags = ["--no-spacing"] + (["--allow-semicolon"] if "keep-punct" in tags else [])
    proc = subprocess.run([sys.executable, str(CHECK), str(tmp), *flags], capture_output=True, text=True, encoding="utf-8")
    issues += [l.split(": ", 1)[-1] for l in proc.stdout.splitlines() if " error " in l]
    return {"ok": not issues, "issues": issues}


def cmd_run(args):
    out = args.out
    out.mkdir(parents=True, exist_ok=True)
    fixed = runner.load_cases(runner.FIXED_DIR)
    bank = [c for c in runner.load_cases(runner.BANK_DIR) if c.path.name != "_common"]
    if args.private:
        bank += runner.load_cases(args.private, private=True)
    pool = {c.name: c for c in fixed + bank}
    missing = [n for n in args.cases if n not in pool]
    if missing:
        sys.exit("找不到題目：" + "、".join(missing))
    cases = [pool[n] for n in args.cases]

    stamp = time.strftime("%Y%m%d-%H%M%S")
    eval_dir = ROOT / "eval-run" / f"blind-{stamp}"
    runner.assemble(eval_dir, cases)
    # 只留機械檢查。語感交給人判斷，不讓 llm 評分項花錢。
    for g in eval_dir.rglob("graders/*.md"):
        if re.search(r"^type:\s*(llm|baseline)\s*$", g.read_text(encoding="utf-8"), re.M):
            g.unlink()
    for d in eval_dir.iterdir():
        if not any((d / "graders").glob("*.md")):
            shutil.copy(runner.COMMON_GRADERS / "no-emoji.md", d / "graders" / "common-no-emoji.md")

    result_dir = ROOT / "eval-run" / f"blind-{stamp}-result"
    cmd = [
        shutil.which("claude"), "plugin", "eval", ".",
        "--eval-dir", eval_dir.relative_to(ROOT).as_posix(),
        "--output-dir", str(result_dir),
        "--model", "sonnet", "--ablation", "with-without", "--runs", "1",
        "-j", str(args.jobs), "--threshold", "0", "--no-publish", "--trust-plugin",
        "--keep-temp", "--max-cost-usd", str(args.max_cost),
    ]
    subprocess.run(cmd, cwd=ROOT, check=False)
    agg = load_json(result_dir / "aggregate-result.json")

    rng = random.Random(args.seed if args.seed is not None else int(time.time()))
    items, key, cost = [], {}, agg.get("costUsd", 0)
    for i, case in enumerate(agg["cases"], 1):
        body = prompt_body(pool[case["name"]])
        sides = {}
        for arm in ("with", "without"):
            run = case["arms"][arm][0]
            text, used = read_trace(run.get("tracePath"))
            regex = [(g["name"], g["passed"]) for g in run["graders"] if not g.get("withOnly")]
            sides[arm] = {
                "text": text,
                "loaded_skill": used,
                "mech": mechanical(body, text, regex, pool[case["name"]].tags),
            }
        first = rng.choice(["with", "without"])
        second = "without" if first == "with" else "with"
        item_id = f"{i:02d}"
        key[item_id] = {
            "name": case["name"], "A": first, "B": second,
            "loaded_skill": sides["with"]["loaded_skill"],
            "mech": {a: sides[a]["mech"] for a in sides},
        }
        items.append({
            "id": item_id,
            "description": re.search(r'^description:\s*"?(.*?)"?$', pool[case["name"]].text, re.M).group(1),
            "prompt": body,
            "A": sides[first]["text"],
            "B": sides[second]["text"],
        })
    save_json(out / "round.json", {"created": stamp, "costUsd": round(cost, 2), "items": items})
    save_json(out / "key.json", key)
    print(f"完成 {len(items)} 題，費用約 {cost:.2f} 美元。輸出在 {out}")


JUDGE_PROMPT = """你是正體中文（台灣）的資深編輯。下面每一題有一個寫作或改稿任務，以及 A、B 兩份輸出。
請判斷哪一份更好地完成任務。依重要性考慮：
1. 有沒有保留原文與素材的事實，沒有加入沒有的事實。
2. 讀起來是否像熟悉主題的台灣人寫的：句子完整、自然，沒有 AI 腔、翻譯腔與對岸用語。
3. 原文已經自然的地方有沒有保留，沒有為了改而改。
差異很小或各有優缺點時選 tie。不要因為較長或改得較多就判較好。

每題輸出一行 JSON，不要輸出其他文字：
{"id": "題號", "winner": "A" 或 "B" 或 "tie", "reason": "一句理由"}
"""


def judge_batch(items, order):
    parts = [JUDGE_PROMPT]
    for it in items:
        a, b = (it["A"], it["B"]) if order == "AB" else (it["B"], it["A"])
        parts.append(f"\n=== 題號 {it['id']} ===\n<task>\n{it['prompt']}\n</task>\n<A>\n{a}\n</A>\n<B>\n{b}\n</B>")
    proc = subprocess.run(
        [shutil.which("claude"), "-p", "--model", "sonnet", "--disable-slash-commands",
         "--no-session-persistence", "--output-format", "json", "--disallowedTools",
         "Bash", "Read", "Write", "Edit", "Glob", "Grep", "WebFetch", "WebSearch", "Task", "Skill"],
        input="\n".join(parts), capture_output=True, text=True, encoding="utf-8",
        cwd=Path(__file__).resolve().parent.parent / "eval-run",
    )
    data = json.loads(proc.stdout)
    verdicts = {}
    for line in data.get("result", "").splitlines():
        line = line.strip().strip("`")
        if line.startswith("{"):
            try:
                v = json.loads(line)
            except ValueError:
                continue
            w = v.get("winner")
            if order == "BA" and w in ("A", "B"):
                w = "B" if w == "A" else "A"
            # 理由裡的 A、B 是評審當時看到的順序，交換順序那一次和頁面上的標示相反。
            verdicts[str(v.get("id"))] = {"winner": w, "reason": v.get("reason", ""), "shown": order}
    return verdicts, data.get("total_cost_usd", 0)


def cmd_judge(args):
    items = load_json(args.out / "round.json")["items"]
    items = [it for it in items if it["A"] and it["B"]]
    result, cost = {}, 0.0
    for order in ("AB", "BA"):
        for i in range(0, len(items), JUDGE_BATCH):
            verdicts, c = judge_batch(items[i:i + JUDGE_BATCH], order)
            cost += c
            for k, v in verdicts.items():
                result.setdefault(k, {})[order] = v
    for k, v in result.items():
        ab, ba = v.get("AB", {}).get("winner"), v.get("BA", {}).get("winner")
        v["final"] = ab if ab == ba else "tie"
    save_json(args.out / "judge.json", {"costUsd": round(cost, 2), "verdicts": result})
    print(f"模型評審完成，費用約 {cost:.2f} 美元。")


PAGE = """<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>盲測配對</title>
<style>
:root { --bg:#fbfaf7; --fg:#1f1f1f; --muted:#666; --card:#fff; --line:#ddd; --accent:#2f6f5e; }
@media (prefers-color-scheme: dark) { :root { --bg:#17181a; --fg:#e8e6e1; --muted:#9a9a9a; --card:#212225; --line:#3a3b3f; --accent:#7cc4ad; } }
body { margin:0; background:var(--bg); color:var(--fg); font:16px/1.75 "Noto Sans TC","PingFang TC","Microsoft JhengHei",sans-serif; }
main { max-width:1200px; margin:0 auto; padding:24px 16px 80px; }
h1 { font-size:22px; margin:0 0 4px; } .muted { color:var(--muted); font-size:14px; }
section { background:var(--card); border:1px solid var(--line); border-radius:8px; padding:16px; margin:20px 0; }
h2 { font-size:17px; margin:0 0 8px; }
details summary { cursor:pointer; color:var(--muted); font-size:14px; }
pre { white-space:pre-wrap; word-break:break-word; font:inherit; margin:8px 0 0; }
.pair { display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-top:12px; }
@media (max-width:760px) { .pair { grid-template-columns:1fr; } }
.side { border:1px solid var(--line); border-radius:6px; padding:12px; }
.side h3 { margin:0; font-size:15px; color:var(--accent); }
.choice { display:flex; flex-wrap:wrap; gap:16px; margin-top:12px; }
textarea { width:100%; box-sizing:border-box; margin-top:8px; min-height:48px; background:var(--bg); color:var(--fg); border:1px solid var(--line); border-radius:6px; font:inherit; }
.bar { position:fixed; bottom:0; left:0; right:0; background:var(--card); border-top:1px solid var(--line); padding:10px 16px; display:flex; gap:16px; align-items:center; justify-content:center; }
button { font:inherit; padding:6px 16px; border-radius:6px; border:1px solid var(--accent); background:var(--accent); color:var(--bg); cursor:pointer; }
</style></head><body><main>
<h1>盲測配對</h1>
<p class="muted">每題的 A、B 是同一個任務的兩份輸出，順序隨機。選擇會自動存在這個瀏覽器，全部選完後按下方按鈕下載 feedback.json。</p>
__ITEMS__
</main>
<div class="bar"><span id="progress"></span><button id="copy">複製結果</button><button id="dl">下載 feedback.json</button></div>
<main><textarea id="out" readonly hidden style="min-height:160px"></textarea></main>
<script>
const KEY = "blind-__CREATED__";
let state = {};
try { state = JSON.parse(localStorage.getItem(KEY) || "{}"); } catch (e) {}
const save = () => { try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) {} update(); };
const ids = [...document.querySelectorAll("section[data-id]")].map(s => s.dataset.id);
function update() {
  const done = ids.filter(id => state[id] && state[id].choice).length;
  document.getElementById("progress").textContent = `已完成 ${done} / ${ids.length}`;
}
document.querySelectorAll("section[data-id]").forEach(sec => {
  const id = sec.dataset.id, s = state[id] || {};
  sec.querySelectorAll("input[type=radio]").forEach(r => {
    if (s.choice === r.value) r.checked = true;
    r.addEventListener("change", () => { state[id] = {...(state[id]||{}), choice: r.value}; save(); });
  });
  const t = sec.querySelector("textarea"); t.value = s.note || "";
  t.addEventListener("input", () => { state[id] = {...(state[id]||{}), note: t.value}; save(); });
});
document.getElementById("dl").addEventListener("click", () => {
  const blob = new Blob([JSON.stringify({round: "__CREATED__", answers: state}, null, 1)], {type: "application/json"});
  const a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = "feedback.json"; a.click();
});
document.getElementById("copy").addEventListener("click", async () => {
  const text = JSON.stringify({round: "__CREATED__", answers: state});
  const out = document.getElementById("out");
  out.hidden = false; out.value = text; out.select();
  try { await navigator.clipboard.writeText(text); } catch (e) { try { document.execCommand("copy"); } catch (e2) {} }
  out.scrollIntoView();
});
update();
</script></body></html>
"""


def cmd_page(args):
    data = load_json(args.out / "round.json")
    blocks = []
    for it in data["items"]:
        e = html.escape
        blocks.append(f"""<section data-id="{it['id']}">
<h2>第 {it['id']} 題</h2>
<p class="muted">{e(it['description'])}</p>
<details open><summary>任務與原文</summary><pre>{e(it['prompt'])}</pre></details>
<div class="pair">
<div class="side"><h3>A</h3><pre>{e(it['A'] or '（沒有輸出）')}</pre></div>
<div class="side"><h3>B</h3><pre>{e(it['B'] or '（沒有輸出）')}</pre></div>
</div>
<div class="choice">
<label><input type="radio" name="c{it['id']}" value="A"> A 較好</label>
<label><input type="radio" name="c{it['id']}" value="tie"> 差不多</label>
<label><input type="radio" name="c{it['id']}" value="B"> B 較好</label>
</div>
<textarea placeholder="意見（選填）"></textarea>
</section>""")
    page = PAGE.replace("__ITEMS__", "\n".join(blocks)).replace("__CREATED__", data["created"])
    (args.out / "review.html").write_text(page, encoding="utf-8")
    print(f"已產生 {args.out / 'review.html'}")


def sign_test(wins, losses):
    """雙尾符號檢定的 p 值。平手不計。"""
    n = wins + losses
    if n == 0:
        return 1.0
    k = min(wins, losses)
    p = sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n
    return min(1.0, 2 * p)


def tally(verdicts, key):
    """把 A／B 的選擇換算成有 skill 的勝、負、平手。"""
    w = l = t = 0
    per = {}
    for item_id, choice in verdicts.items():
        if choice not in ("A", "B", "tie") or item_id not in key:
            continue
        if choice == "tie":
            t += 1
            per[item_id] = "tie"
        elif key[item_id][choice] == "with":
            w += 1
            per[item_id] = "with"
        else:
            l += 1
            per[item_id] = "without"
    return w, l, t, per


def cmd_stats(args):
    key = load_json(args.out / "key.json")
    lines = []
    fb_path = args.out / "feedback.json"
    human = {}
    if fb_path.is_file():
        answers = load_json(fb_path)["answers"]
        human = {k: v.get("choice") for k, v in answers.items()}
        w, l, t, hper = tally(human, key)
        rate = w / (w + l) if w + l else float("nan")
        lines += [
            "## 人工盲測",
            f"有 skill 勝 {w}、負 {l}、平手 {t}。勝率（不計平手）{rate:.0%}，符號檢定 p = {sign_test(w, l):.3f}。",
        ]
    judge_path = args.out / "judge.json"
    if judge_path.is_file():
        verdicts = {k: v["final"] for k, v in load_json(judge_path)["verdicts"].items()}
        w, l, t, jper = tally(verdicts, key)
        flips = sum(1 for v in load_json(judge_path)["verdicts"].values() if v.get("AB", {}).get("winner") != v.get("BA", {}).get("winner"))
        lines += [
            "", "## 模型評審",
            f"有 skill 勝 {w}、負 {l}、平手 {t}。交換順序後結論改變 {flips} 題，這些都算平手。",
        ]
        if human:
            _, _, _, hper = tally(human, key)
            both = [k for k in hper if k in jper]
            agree = sum(1 for k in both if hper[k] == jper[k])
            lines.append(f"和人工的一致率 {agree}/{len(both)}。")
    mech = {"with": [0, 0], "without": [0, 0]}
    for v in key.values():
        for arm, m in v["mech"].items():
            mech[arm][0] += m["ok"]
            mech[arm][1] += 1
    lines += ["", "## 機械檢查", f"有 skill 通過 {mech['with'][0]}/{mech['with'][1]}，沒有 skill 通過 {mech['without'][0]}/{mech['without'][1]}。"]
    lines += ["", "## 逐題", "| 題號 | 題目 | A | 人工 | 模型 | 有 skill 的機械問題 | 沒有 skill 的機械問題 |", "| --- | --- | --- | --- | --- | --- | --- |"]
    jv = load_json(judge_path)["verdicts"] if judge_path.is_file() else {}
    for item_id, v in sorted(key.items()):
        h = human.get(item_id, "")
        hj = {"A": v["A"], "B": v["B"]}.get(h, h)
        j = jv.get(item_id, {}).get("final", "")
        jj = {"A": v["A"], "B": v["B"]}.get(j, j)
        lines.append(f"| {item_id} | {v['name']} | {v['A']} | {hj} | {jj} | {'；'.join(v['mech']['with']['issues']) or '無'} | {'；'.join(v['mech']['without']['issues']) or '無'} |")
    report = "\n".join(lines) + "\n"
    (args.out / "stats.md").write_text(report, encoding="utf-8")
    print(report)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=["run", "judge", "page", "stats"])
    parser.add_argument("--out", type=Path, required=True, help="這一輪的資料夾，放在 repo 之外")
    parser.add_argument("--cases", nargs="*", default=[])
    parser.add_argument("--private", type=Path)
    parser.add_argument("--seed", type=int)
    parser.add_argument("-j", "--jobs", type=int, default=6)
    parser.add_argument("--max-cost", type=float, default=5)
    args = parser.parse_args()
    {"run": cmd_run, "judge": cmd_judge, "page": cmd_page, "stats": cmd_stats}[args.command](args)


if __name__ == "__main__":
    main()
