import json, sys, re, statistics, collections
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[3]/"skills"/"zh-tw-prose"/"scripts"))
import check
E=sys.argv[1]; TF=sys.argv[2]; OUT=sys.argv[3]; CONDS=sys.argv[4].split(","); tasks=json.load(open(TF,encoding="utf-8"))
terms=check.load_usage_terms(check.USAGE_TABLE)
agg=collections.defaultdict(lambda: collections.defaultdict(list))
bykind=collections.defaultdict(lambda: collections.defaultdict(list))
for t in tasks:
    for c in CONDS:
        for s in [1,2]:
            txt=open(f"{OUT}/{t['id']}__{c}__{s}.txt",encoding="utf-8").read()
            iss=check.check_text(txt,"x",terms,markdown=True,check_space=(t['id']!='w-ui'))
            err=sum(i.level=="error" for i in iss); warn=sum(i.level=="warning" and i.rule.startswith("ai-") for i in iss)
            p=check.profile_text(txt,True)
            facts=sum(f in txt for f in t["facts"])/len(t["facts"])
            row=dict(err=err,aiwarn=warn,facts=facts,**{k:p.get(k,0) for k in ["connectives","pronouns","determiners","bei","light_verbs","de","sent_cv","han_chars"]})
            for k,v in row.items(): agg[c][k].append(v)
            if t["kind"] in ("translate","rewrite"):
                for k,v in row.items(): bykind[c][k].append(v)
def show(a,title):
    print(title)
    keys=list(next(iter(a.values())).keys())
    print("metric".ljust(12),*[c.rjust(8) for c in CONDS])
    for k in keys:
        print(k.ljust(12),*[f"{statistics.mean(a[c][k]):8.2f}" for c in CONDS])
show(agg,"== 全部題目")
show(bykind,"== 翻譯與改寫題")
