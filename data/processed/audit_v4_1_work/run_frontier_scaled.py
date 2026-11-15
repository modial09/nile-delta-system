import json, sys, time
from pathlib import Path
import pulp
sys.path.insert(0, str(Path(__file__).parent))
import au

# Variant of my formulation with water carried in thousands of cubic
# metres, as a scaling cross check. Production and water constraints
# are rescaled consistently; nothing else changes.
import types

def build_scaled(par, floor=0.0, caps=False):
    # rescale: define an edited par where water_req is divided by 1000
    # and budgets divided by 1000, and production uses w in 1000 m3.
    # au.build computes q = y*(1-Ky)*a + y*Ky/wreq * w, so dividing
    # wreq by 1000 while w is measured in 1000 m3 keeps q identical.
    p = au.modified(par)
    p["water_req"] = {c: v/1000.0 for c, v in par["water_req"].items()}
    p["budget"] = {k: v/1000.0 for k, v in par["budget"].items()}
    return au.build(p, floor=floor, caps=caps)

par = au.load()
out = {}
for label, fl, caps in [("primary_50_scaled", 0.50, False), ("primary_80_scaled", 0.80, False),
                        ("capped_75_scaled", 0.75, True)]:
    t0=time.time()
    prob, v = build_scaled(par, floor=fl, caps=caps)
    st = au.solve(prob)
    m = float(pulp.value(prob.objective)) if st=="Optimal" else None
    out[label]={"status":st,"margin":m,"seconds":round(time.time()-t0,1)}
    print(label, out[label], flush=True)
Path(au.BASE/"data/processed/audit_v4_1_work/frontier_scaled.json").write_text(json.dumps(out, indent=1))
