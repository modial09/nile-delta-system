import json
import sys
import time
from pathlib import Path

import pulp

sys.path.insert(0, str(Path(__file__).parent))
import au

par = au.load()
out = {}

def margin_run(p, label, floor, caps=False):
    t0 = time.time()
    prob, v = au.build(p, floor=floor, caps=caps)
    st = au.solve(prob)
    if st != "Optimal":
        out[label] = {"status": st, "seconds": round(time.time() - t0, 1)}
        print(label, out[label], flush=True)
        return None
    m = float(pulp.value(prob.objective))
    planted = {}
    for c in au.A_CROPS:
        if c in au.W_CROPS:
            planted[c] = sum(float(v["xw"][(d, c)].value()) for d in au.D)
        else:
            planted[c] = sum(par["inflow"]["probs"][i] * float(v["xs"][(d, c, i)].value())
                             for d in au.D for i in au.INF)
    staple_min = None
    staple_exp = 0.0
    for s in par["scenarios"]:
        sv = sum(float(pulp.value(v["prod"][(d, c, s)])) for d in au.D for c in au.STAPLES)
        staple_exp += par["prob"][s] * sv
        staple_min = sv if staple_min is None else min(staple_min, sv)
    out[label] = {"status": st, "margin": m, "planted": planted,
                  "staple_min": staple_min, "staple_expected": staple_exp,
                  "seconds": round(time.time() - t0, 1)}
    print(label, {k: out[label][k] for k in ("status", "margin", "seconds")}, flush=True)
    return m

for lv in (0.0, 0.50, 0.60, 0.70, 0.75, 0.80):
    margin_run(par, f"primary_{int(lv*100)}", lv)
for lv in (0.85,):
    margin_run(par, f"primary_{int(lv*100)}", lv)
for lv in (0.0, 0.75):
    margin_run(par, f"capped_{int(lv*100)}", lv, caps=True)

# Beet variant at 2400 in every layer
price_o = dict(par["price"])
price_o["Sugar beet"] = {"low": 2400.0, "expected": 2400.0, "high": 2400.0}
par_beet = au.modified(par, price=price_o)
for lv in (0.0, 0.70, 0.80):
    margin_run(par_beet, f"beet2400_{int(lv*100)}", lv)

# Winter potato cost sensitivity, unconstrained
cost_o = dict(par["cost"]); cost_o["Potatoes_winter"] = 54176.19
margin_run(au.modified(par, cost=cost_o), "winterpot_nilicost_0", 0.0)

Path(au.BASE / "data/processed/audit_v4_1_work/frontier.json").write_text(json.dumps(out, indent=1, default=str))
print("done")
