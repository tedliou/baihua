import json, subprocess, sys, os
from concurrent.futures import ThreadPoolExecutor
E=sys.argv[1]; EMPTY=os.path.join(E,"empty"); os.makedirs(EMPTY,exist_ok=True); TF=sys.argv[2]; CONDS=sys.argv[3].split(","); OUT=sys.argv[4]; os.makedirs(OUT,exist_ok=True)
tasks=json.load(open(TF,encoding="utf-8"))
jobs=[(t,c,s) for t in tasks for c in CONDS for s in [1,2]]
def run(j):
    t,c,s=j; out=f"{OUT}/{t['id']}__{c}__{s}.txt"
    if os.path.exists(out) and os.path.getsize(out)>0: return
    cmd=["claude","-p","--model","sonnet","--tools",""]
    if c!="none": cmd+=["--append-system-prompt-file",f"{E}/skill-prompts/{c}.md"]
    for _ in range(3):
        r=subprocess.run(cmd,cwd=EMPTY,input=t["prompt"],capture_output=True,text=True,timeout=300)
        if r.returncode==0 and r.stdout.strip():
            open(out,"w",encoding="utf-8").write(r.stdout.strip()); return
    print("FAIL",out,r.stderr[:200])
with ThreadPoolExecutor(8) as ex: list(ex.map(run,jobs))
print("done", len(os.listdir(OUT)))
