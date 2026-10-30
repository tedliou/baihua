import json, sys, glob, collections, math
E=sys.argv[1]; TF=sys.argv[2]; PAIRS=[tuple(p.split("-")) for p in sys.argv[3].split(",")]; JD=sys.argv[4]
tasks=json.load(open(TF,encoding="utf-8")); kind={t["id"]:t["kind"] for t in tasks}
def sign_p(w,l):
    n=w+l; k=min(w,l)
    if n==0: return 1.0
    return min(1.0, 2*sum(math.comb(n,i) for i in range(k+1))/2**n)
for x,y in PAIRS:
    res=collections.Counter(); bk=collections.defaultdict(collections.Counter); pos=collections.Counter()
    for t in tasks:
        for s in [1,2]:
            r1=json.load(open(f"{JD}/{t['id']}__{x}-{y}__{s}__xy.json"))["resolved"]
            r2=json.load(open(f"{JD}/{t['id']}__{x}-{y}__{s}__yx.json"))["resolved"]
            v = r1 if r1==r2 else "tie"
            res[v]+=1; bk[t["kind"]][v]+=1
    print(f"{x} vs {y}: {x} 勝 {res[x]}、{y} 勝 {res[y]}、平手 {res['tie']}，符號檢定 p={sign_p(res[x],res[y]):.3f}")
    for k,c in bk.items(): print(f"   {k:9s} {x} {c[x]} / {y} {c[y]} / tie {c['tie']}")
