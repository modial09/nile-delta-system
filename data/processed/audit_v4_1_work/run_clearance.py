import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import au

par = au.load()
out = {}

for lv in (50, 60, 70, 75, 80):
    plan, share = au.load_plan(au.PROC / f"plan_v4_1_floor{lv}.csv")
    t0 = time.time()
    res = au.max_staple_plan(par, plan, bound="cell")
    floor_t = lv / 100.0 * par["reference_t"]
    heads = {f"{s[0]}_{s[1]}": (v - floor_t if v is not None else None) for s, v in res.items()}
    finite = [v for v in heads.values() if v is not None]
    out[f"floor{lv}_cell"] = {"floor_t": floor_t, "max_staple": {f"{s[0]}_{s[1]}": v for s, v in res.items()},
                              "headroom": heads, "min_headroom": min(finite) if finite else None,
                              "min_scenarios": [k for k, v in heads.items() if v is not None and abs(v - min(finite)) < 0.05],
                              "seconds": round(time.time() - t0, 1)}
    print(f"floor{lv}", out[f"floor{lv}_cell"]["min_headroom"], out[f"floor{lv}_cell"]["min_scenarios"], flush=True)

# Bound sensitivity on the 70 and 80 plans: physical area bound and pool limit bound
for lv in (70, 80):
    plan, share = au.load_plan(au.PROC / f"plan_v4_1_floor{lv}.csv")
    floor_t = lv / 100.0 * par["reference_t"]
    for bound in ("physical", "pool"):
        t0 = time.time()
        res = au.max_staple_plan(par, plan, bound=bound)
        heads = {f"{s[0]}_{s[1]}": (v - floor_t if v is not None else None) for s, v in res.items()}
        finite = [v for v in heads.values() if v is not None]
        out[f"floor{lv}_{bound}"] = {"headroom": heads,
                                     "min_headroom": min(finite) if finite else None,
                                     "n_failed": sum(1 for v in heads.values() if v is None),
                                     "seconds": round(time.time() - t0, 1)}
        print(f"floor{lv} bound={bound}", out[f"floor{lv}_{bound}"]["min_headroom"],
              "failed", out[f"floor{lv}_{bound}"]["n_failed"], flush=True)

Path(au.BASE / "data/processed/audit_v4_1_work/clearance.json").write_text(json.dumps(out, indent=1, default=str))
print("done")
