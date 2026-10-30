import json, subprocess, sys, os, re
from concurrent.futures import ThreadPoolExecutor
E=sys.argv[1]; EMPTY=os.path.join(E,"empty"); os.makedirs(EMPTY,exist_ok=True); TF=sys.argv[2]; PAIRS=[tuple(p.split("-")) for p in sys.argv[3].split(",")]; OUT=sys.argv[4]; JD=sys.argv[5]; os.makedirs(JD,exist_ok=True)
tasks=json.load(open(TF,encoding="utf-8"))
TPL="""你是在台灣長大、做過多年編輯的審稿人。下面是一個寫作任務，以及兩份不同人交出的成品 A 與 B。請判斷哪一份比較好。

判斷標準，依重要性排列：
1. 讀起來像熟悉主題的台灣人自己寫的：語序與句子的組法自然，沒有翻譯腔（例如多餘的代名詞、連接詞、冗長的「的」字修飾、被動句），沒有 AI 腔（例如空泛評價、假對比、說教、套話）。
2. 忠於任務的素材：沒有漏掉或捏造事實。潤稿題要保留原文沒問題的寫法。
3. 符合任務的語域與用途，台灣用語與標點正確。

兩份差不多時可以判平手。只輸出一行 JSON：{{"winner":"A"或"B"或"tie","reason":"一句話"}}

## 任務
{task}

## 成品 A
{a}

## 成品 B
{b}
"""
jobs=[]
for t in tasks:
    for x,y in PAIRS:
        for s in [1,2]:
            for order in ["xy","yx"]:
                jobs.append((t,x,y,s,order))
def read(t,c,s): return open(f"{OUT}/{t['id']}__{c}__{s}.txt",encoding="utf-8").read()
def run(j):
    t,x,y,s,order=j; out=f"{JD}/{t['id']}__{x}-{y}__{s}__{order}.json"
    if os.path.exists(out): return
    a,b=(read(t,x,s),read(t,y,s)) if order=="xy" else (read(t,y,s),read(t,x,s))
    prompt=TPL.format(task=t["prompt"],a=a,b=b)
    for _ in range(3):
        r=subprocess.run(["claude","-p","--model","opus","--tools",""],cwd=EMPTY,input=prompt,capture_output=True,text=True,timeout=300)
        m=re.search(r"\{.*\}",r.stdout,re.S)
        if m:
            try:
                d=json.loads(m.group(0)); w=d["winner"]
                win = "tie" if w=="tie" else ((x if w=="A" else y) if order=="xy" else (y if w=="A" else x))
                d["resolved"]=win; json.dump(d,open(out,"w",encoding="utf-8"),ensure_ascii=False); return
            except Exception: pass
    print("FAIL",out,r.stdout[:200],r.stderr[:200])
with ThreadPoolExecutor(8) as ex: list(ex.map(run,jobs))
print("done",len(os.listdir(JD)),"of",len(jobs))
