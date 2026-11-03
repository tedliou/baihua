"""產生單份審閱用的輸出。cur：照實際用法載入已安裝的 baihua plugin，允許 Read/Glob/Grep/Skill/Bash；none：停用所有 skill、不給工具。"""
import json, subprocess, sys, os
from concurrent.futures import ThreadPoolExecutor
tasks = json.load(open(sys.argv[1], encoding="utf-8")); OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
EMPTY = os.path.join(os.path.dirname(os.path.abspath(OUT)), "work"); os.makedirs(EMPTY, exist_ok=True)
jobs = [(t, c) for t in tasks for c in ["cur", "none"]]
def run(j):
    t, c = j; base = f"{OUT}/{t['id']}__{c}"
    if os.path.exists(base + ".txt") and os.path.getsize(base + ".txt") > 0: return
    if c == "none":
        cmd = ["claude", "-p", "--model", "sonnet", "--tools", "", "--disable-slash-commands"]
    else:
        cmd = ["claude", "-p", "--model", "sonnet", "--allowed-tools", "Read,Glob,Grep,Skill,Bash",
               "--output-format", "stream-json", "--verbose", "--max-turns", "12"]
    for _ in range(3):
        r = subprocess.run(cmd, cwd=EMPTY, input=t["prompt"], capture_output=True, text=True, timeout=600)
        if r.returncode != 0 or not r.stdout.strip(): continue
        if c == "none":
            open(base + ".txt", "w", encoding="utf-8").write(r.stdout.strip()); return
        open(base + ".jsonl", "w", encoding="utf-8").write(r.stdout)
        final = None
        for line in r.stdout.splitlines():
            try: e = json.loads(line)
            except ValueError: continue
            if e.get("type") == "result": final = e.get("result")
        if final and final.strip():
            open(base + ".txt", "w", encoding="utf-8").write(final.strip()); return
    print("FAIL", base, r.stderr[:300])
with ThreadPoolExecutor(6) as ex: list(ex.map(run, jobs))
print("done", len([f for f in os.listdir(OUT) if f.endswith(".txt")]))
