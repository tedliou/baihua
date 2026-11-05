"""用共用評分表加上各題的 regex 評一組輸出，和作者判斷比對。
用法：judge2.py <repo> <rubric.md> <結果.json> <輸出資料夾:作者標記>...
作者標記是判斷資料夾的路徑，或 "all-pass-except:<題目,...>"。
"""
import json, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
repo, rubric, dest = Path(sys.argv[1]), Path(sys.argv[2]).read_text(encoding="utf-8"), Path(sys.argv[3])
items = {p.stem: json.load(open(p, encoding="utf-8")) for p in (repo / "experiments/2026-11-04-bank-review/items").glob("*.json")}
name2id = {v["name"]: k for k, v in items.items()}
def fm(t):
    m = re.match(r"---\n(.*?)\n---\n(.*)", t, re.S); return m.group(1), m.group(2).strip()
def field(f, k):
    m = re.search(rf"^{k}:\s*(.*)$", f, re.M); return m.group(1).strip().strip("'\"") if m else None
jobs = []
for spec in sys.argv[4:]:
    outdir, label = spec.split(":", 1)
    if label.startswith("all-pass-except"):
        fails = set(label.split(":", 1)[1].split(",")); author = lambda n, f=fails: n not in f
    else:
        rv = {items[json.load(open(p))["item"]]["name"]: json.load(open(p))["verdict"] == "pass" for p in Path(label).glob("*.json")}
        author = lambda n, rv=rv: rv.get(n)
    for case in sorted((repo / "eval-bank").iterdir()):
        if case.name not in name2id: continue
        out = Path(outdir) / f"{name2id[case.name]}.txt"
        if not out.is_file(): continue
        jobs.append((outdir, case, out.read_text(encoding="utf-8").strip(), author(case.name)))
def run(j):
    outdir, case, output, a = j
    task = fm((case / "prompt.md").read_text(encoding="utf-8"))[1]
    regex_ok = True
    for g in (case / "graders").glob("*.md"):
        f, _ = fm(g.read_text(encoding="utf-8"))
        if field(f, "type") == "regex":
            found = re.search(field(f, "pattern"), output) is not None
            regex_ok &= found if (field(f, "match") or "contains") == "contains" else not found
    prompt = f"你是評分員。依「評分條件」判斷「輸出」是否通過。只看條件，不要加入自己的標準。\n\n# 任務\n{task}\n\n# 輸出\n{output}\n\n# 評分條件\n{rubric}\n\n先用一兩句說明理由，最後一行只寫 PASS 或 FAIL。"
    votes = []
    for _ in range(3):
        r = subprocess.run(["claude", "-p", "--model", "sonnet", "--tools", "", "--disable-slash-commands"], input=prompt, capture_output=True, text=True, timeout=300, cwd="/tmp")
        last = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ""
        votes.append(("PASS" in last and "FAIL" not in last, r.stdout.strip()[-300:]))
    rub = sum(v for v, _ in votes) >= 2
    return {"set": outdir, "case": case.name, "author": a, "regex": regex_ok, "rubric": rub, "pass": regex_ok and rub, "why": [w for _, w in votes]}
with ThreadPoolExecutor(6) as ex: res = list(ex.map(run, jobs))
json.dump(res, open(dest, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
ok = [r for r in res if r["author"] is not None]
agree = sum(r["author"] == r["pass"] for r in ok)
tp = sum(r["author"] and r["pass"] for r in ok); tn = sum((not r["author"]) and (not r["pass"]) for r in ok)
print(f"一致 {agree}/{len(ok)}；作者通過且評分通過 {tp}/{sum(r['author'] for r in ok)}，作者不通過且評分不通過 {tn}/{sum(not r['author'] for r in ok)}")
for r in ok:
    if r["author"] != r["pass"]:
        print(f"不一致 [{Path(r['set']).parent.name}] {r['case']}: 作者={'通過' if r['author'] else '不通過'} regex={r['regex']} 評分表={r['rubric']}")
