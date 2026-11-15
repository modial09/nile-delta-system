"""Detail on the floor imposed replay of the saved floor 80 plan.

Prints the per scenario status of the recourse solve with the hard
floor imposed at the exact saved share, then repeats with the floor
eased by 1 tonne and by 100 tonnes, to test whether the failure is a
solver tolerance edge at an exactly binding constraint. Also prints
the clearance maximisation per scenario for the same plan, the
build own test, recomputed here.
Changes no existing file. Run with PYTHONDONTWRITEBYTECODE=1.
"""
import sys
from pathlib import Path

import pandas as pd
import pulp

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))
import allocation_model_v5 as M  # noqa: E402

PROC = ROOT / "data" / "processed"
par = M.load_all()
REF = par["reference_t"]

df = pd.read_csv(PROC / "plan_v5_floor80.csv")
plan = {"winter": {}, "summer": {}}
for _, r in df.iterrows():
    if r["kind"] == "winter":
        plan["winter"][(r["district"], r["crop"])] = float(r["area"])
    else:
        plan["summer"][(r["district"], r["crop"], r["inflow"])] = float(r["area"])

for share, label in ((0.80, "exact floor"), (0.80 - 1.0 / REF, "floor eased by 1 tonne"),
                     (0.80 - 100.0 / REF, "floor eased by 100 tonnes")):
    print(f"--- {label} (share {share:.10f})")
    for s in par["scenarios"]:
        prob, v = M.build(par, floor_share=share, fixed=plan, single_scenario=s)
        st = M.solve(prob, timelimit=300)
        extra = ""
        if st == "Optimal":
            staple = sum(float(pulp.value(v["prod"][(d, c, s)]))
                         for d in M.DISTRICTS for c in M.STAPLE_CROPS)
            extra = f"staple {staple:,.3f} vs floor {share * REF:,.3f}"
        print(f"  {M.skey(*s)}: {st} {extra}")

print("--- clearance maximisation per scenario (max staple, fixed plan)")
for s in par["scenarios"]:
    prob, v = M.build(par, fixed=plan, objective="maxstaple", single_scenario=s)
    st = M.solve(prob, timelimit=300)
    t = float(v["t"].value()) if st == "Optimal" else None
    print(f"  {M.skey(*s)}: {st} max staple {t:,.3f} headroom vs floor 80 "
          f"{t - 0.80 * REF:,.3f}" if t is not None else f"  {M.skey(*s)}: {st}")
print("DONE")
