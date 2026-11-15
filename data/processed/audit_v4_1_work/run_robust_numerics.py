import json
import random
import sys
from pathlib import Path

import pandas as pd
import pulp

sys.path.insert(0, str(Path(__file__).parent))
import au

par = au.load()
out = {}

# ---------- Robustness rederivation ----------
plan, share = au.load_plan(au.PROC / "plan_v4_1_robust_plan.csv")
out["robust_plan_share"] = share
flows = par["flows"]
mean_flow = float(flows.mean())
windows = flows.rolling(10).mean().dropna().tolist()
rng = random.Random(20261114)
draws = []
for n in range(100):
    if n % 2 == 0:
        draws.append((float(rng.choice(flows.tolist())) / mean_flow, "single year"))
    else:
        draws.append((float(rng.choice(windows)) / mean_flow, "ten year window mean"))
saved = pd.read_csv(au.PROC / "robustness_samples_v4_1.csv")
check_idx = list(range(14)) + [50, 75, 95, 96, 98, 99]
res = {}
for n in check_idx:
    ratio, kind = draws[n]
    budget_total = au.ANCHOR * ratio * 1e9
    got = au.max_staple_plan(par, plan, bound="cell", budget_total=budget_total,
                             single=("normal", "expected"))
    val = got[("normal", "expected")]
    row = saved[saved["sample"] == n].iloc[0]
    res[n] = {"ratio_mine": ratio, "ratio_file": float(row["ratio"]),
              "kind_mine": kind, "kind_file": row["kind"],
              "staple_mine": val, "staple_file": float(row["max_staple_tonnes"]),
              "diff": (val - float(row["max_staple_tonnes"])) if val is not None else None}
    print("robust sample", n, kind, ratio, val, "file", float(row["max_staple_tonnes"]), flush=True)
out["robust_rederive"] = res

# Also: what the same samples give with the late planting frozen at the
# dry variant instead, on three samples, to show the convention matters
dry_plan = {"winter": plan["winter"],
            "summer": {(d, c, i): plan["summer"][(d, c, "dry")] for d in au.D for c in au.L_CROPS for i in au.INF}}
conv = {}
for n in (0, 2, 96):
    ratio, kind = draws[n]
    got = au.max_staple_plan(par, dry_plan, bound="cell", budget_total=au.ANCHOR * ratio * 1e9,
                             single=("normal", "expected"))
    conv[n] = got[("normal", "expected")]
out["robust_dry_variant_check"] = conv
print("dry variant check", conv, flush=True)

# ---------- Numerics claim 1: CBC tolerance 1e-9 ----------
num = {}
for lv in (70, 80):
    plan_lv, _ = au.load_plan(au.PROC / f"plan_v4_1_floor{lv}.csv")
    for s in [("dry", "low"), ("normal", "expected")]:
        for tol in (None, "1e-9"):
            prob, v = au.build(par, floor=lv / 100.0, fixed=plan_lv, single=s, bound="cell")
            st = au.solve(prob, tol=tol)
            num[f"floor{lv}_{s[0]}_{s[1]}_tol{tol}"] = st
        # staple maximisation at 1e-9 as well
        prob, v = au.build(par, fixed=plan_lv, single=s, bound="cell", objective="maxstaple_expected")
        st = au.solve(prob, tol="1e-9")
        num[f"floor{lv}_{s[0]}_{s[1]}_maxstaple_tol1e-9"] = st
        prob, v = au.build(par, fixed=plan_lv, single=s, bound="cell", objective="maxstaple_expected")
        st = au.solve(prob)
        num[f"floor{lv}_{s[0]}_{s[1]}_maxstaple_toldefault"] = st
    print("numerics tol floor", lv, "done", flush=True)
out["tolerance_tests"] = num

# ---------- Numerics claim 2: pool limit linkage bound ----------
plan80, _ = au.load_plan(au.PROC / "plan_v4_1_floor80.csv")
# (a) pool bound already shown to fail all 12 in run_clearance.py.
# (b) clip the two kinds of cells that sit above a pool limit down to
# the limit (changes of less than 0.005 hectares) and retry pool bound.
clipped = {"winter": {}, "summer": {}}
n_clip = 0
for (d, c), val in plan80["winter"].items():
    lim = par["land_limit"][d][au.POOL_OF[c]]
    if val > lim:
        n_clip += 1
        val = lim
    clipped["winter"][(d, c)] = val
for (d, c, i), val in plan80["summer"].items():
    lim = par["land_limit"][d][au.POOL_OF[c]]
    if val > lim:
        n_clip += 1
        val = lim
    clipped["summer"][(d, c, i)] = val
out["cells_clipped"] = n_clip
got = au.max_staple_plan(par, clipped, bound="pool", single=("dry", "low"))
out["clipped_pool_bound_dry_low"] = got[("dry", "low")]
print("clipped cells", n_clip, "pool bound dry_low max staple", got, flush=True)
# (c) pool bound on the historical baseline plan, whose cells sit
# strictly inside the pool limits
base_plan = {"winter": {(d, c): par["baseline"][c][d] for d in au.D for c in au.W_CROPS},
             "summer": {(d, c, i): par["baseline"][c][d] for d in au.D for c in au.L_CROPS for i in au.INF}}
prob, v = au.build(par, fixed=base_plan, single=("dry", "low"), bound="pool")
out["baseline_pool_bound_dry_low_status"] = au.solve(prob)
print("baseline pool bound status", out["baseline_pool_bound_dry_low_status"], flush=True)

Path(au.BASE / "data/processed/audit_v4_1_work/robust_numerics.json").write_text(json.dumps(out, indent=1, default=str))
print("done")
