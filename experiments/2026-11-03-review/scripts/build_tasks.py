import json, sys
from pathlib import Path
R = Path(__file__).resolve().parents[3]
out = Path(sys.argv[1])
def exp(f, i):
    for t in json.loads((R/f).read_text(encoding="utf-8")):
        if t["id"] == i: return {"id": i, "source": f"{f}#{i}", "kind": t.get("kind",""), "prompt": t["prompt"], "facts": t.get("facts", [])}
    raise SystemExit(i)
def bank(n):
    txt = (R/"eval-bank"/n/"prompt.md").read_text(encoding="utf-8")
    fm, body = txt.split("---", 2)[1:]
    return {"id": n, "source": f"eval-bank/{n}", "kind": "bank", "prompt": body.strip(), "facts": []}
S, H = "experiments/2026-10-30-syntax/", "experiments/2026-10-30-human/"
tasks = [
  exp(S+"tasks-set2.json", "h-write-article"),
  exp(S+"tasks-set2.json", "h-translate-guide"),
  exp(S+"tasks-set2.json", "h-rewrite-review"),
  exp(S+"tasks-set2.json", "h-polish-mixed"),
  exp(S+"tasks-set2.json", "h-write-report"),
  exp(H+"tasks-letters-discovery.json", "r8-w-email"),
  exp(H+"tasks-ui-discovery.json", "r11-permission"),
  exp(H+"tasks-personal.json", "r4-hike"),
  bank("mechanism-first-paragraph"),
  bank("wiki-claim-left-to-discover"),
]
out.write_text(json.dumps(tasks, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(tasks))
