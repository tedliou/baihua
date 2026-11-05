"""用題庫的評分條件評一組既有輸出，和作者的判斷比對。
用法：judge.py <repo> <輸出資料夾> <作者判斷資料夾> <結果.json>
"""
import json, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
repo, outdir, revdir, dest = map(Path, sys.argv[1:5])
items = {p.stem: json.load(open(p, encoding="utf-8")) for p in (repo / "experiments/2026-11-04-bank-review/items").glob("*.json")}
name2id = {v["name"]: k for k, v in items.items()}
def fm(text):
    m = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S); return m.group(1), m.group(2).strip()
def field(f, k):
    m = re.search(rf"^{k}:\s*(.*)$", f, re.M); return m.group(1).strip().strip("'\"") if m else None
jobs = []
for case in sorted((repo / "eval-bank").iterdir()):
    if case.name == "_common" or case.name not in name2id: continue
    iid = name2id[case.name]; out = (outdir / f"{iid}.txt")
    if not out.is_file(): continue
    task = fm((case / "prompt.md").read_text(encoding="utf-8"))[1]
    output = out.read_text(encoding="utf-8").strip()
    for g in sorted((case / "graders").glob("*.md")):
        f, body = fm(g.read_text(encoding="utf-8"))
        jobs.append((case.name, iid, g.stem, field(f, "type"), field(f, "pattern"), field(f, "match") or "contains", body, task, output))
def run(j):
    name, iid, g, typ, pat, match, body, task, output = j
    if typ == "regex":
        found = re.search(pat, output) is not None
        return (name, g, found if match == "contains" else not found, "")
    prompt = f"你是評分員。依「評分條件」判斷「輸出」是否通過。只看條件，不要加入自己的標準。\n\n# 任務\n{task}\n\n# 輸出\n{output}\n\n# 評分條件\n{body}\n\n先用一兩句說明理由，最後一行只寫 PASS 或 FAIL。"
    r = subprocess.run(["claude", "-p", "--model", "sonnet", "--tools", "", "--disable-slash-commands"], input=prompt, capture_output=True, text=True, timeout=300, cwd="/tmp")
    last = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ""
    return (name, g, "PASS" in last and "FAIL" not in last, r.stdout.strip()[-400:])
with ThreadPoolExecutor(6) as ex: res = list(ex.map(run, jobs))
author = {}
for p in revdir.glob("*.json"):
    r = json.load(open(p, encoding="utf-8")); author[items[r["item"]]["name"]] = r["verdict"] == "pass"
per = {}
for name, g, ok, why in res: per.setdefault(name, {})[g] = {"pass": ok, "why": why}
summary = {n: {"author": author.get(n), "graders": gs, "all_pass": all(v["pass"] for v in gs.values())} for n, gs in per.items()}
agree = sum(1 for s in summary.values() if s["author"] is not None and s["author"] == s["all_pass"])
json.dump(summary, open(dest, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"一致 {agree}/{len(summary)}")
for n, s in sorted(summary.items()):
    if s["author"] != s["all_pass"]:
        print(f"不一致 {n}: 作者={'通過' if s['author'] else '不通過'} 評分={'通過' if s['all_pass'] else '不通過'} 失敗項={[g for g,v in s['graders'].items() if not v['pass']]}")
