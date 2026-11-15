"""Independent plan feasibility and cross solver checks for version 5.

Part 1 is pure arithmetic on the saved plan CSV files: pool sums per
district against the land limits from load_all, at full precision.
Part 2 replays each saved plan through the recourse evaluation and
compares the expected margin and the minimum scenario staple tonnage
with the unrounded frontier values in results_v5_main.json.
Part 3 solves the floor 80 percent problem and the ceiling problem
with HiGHS, a different solver from the CBC used by the build, and
compares objectives.
Changes no existing file. Run with PYTHONDONTWRITEBYTECODE=1.
"""
import json
import sys
from pathlib import Path

import pandas as pd
import pulp

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))
import allocation_model_v5 as M  # noqa: E402

PROC = ROOT / "data" / "processed"
par = M.load_all()
res = json.loads((PROC / "results_v5_main.json").read_text())
REF = par["reference_t"]


def load_plan(path):
    df = pd.read_csv(path)
    plan = {"winter": {}, "summer": {}}
    for _, r in df.iterrows():
        if r["kind"] == "winter":
            plan["winter"][(r["district"], r["crop"])] = float(r["area"])
        else:
            plan["summer"][(r["district"], r["crop"], r["inflow"])] = float(r["area"])
    return plan, float(df["floor_share"].iloc[0])


print("=" * 70)
print("Part 1. Pool sums of the saved plans against the land limits")
for pct in (50, 60, 70, 75, 80):
    plan, share = load_plan(PROC / f"plan_v5_floor{pct}.csv")
    worst_over = 0.0
    worst_cell = None
    for d in M.DISTRICTS:
        w = sum(plan["winter"][(d, c)] for c in M.WINTER_CROPS)
        over = w - par["land_limit"][d]["winter"]
        if over > worst_over:
            worst_over, worst_cell = over, (d, "winter", "all")
        for i in M.INFLOW_STATES:
            s = sum(plan["summer"][(d, c, i)] for c in M.SUMMER_CROPS)
            n = sum(plan["summer"][(d, c, i)] for c in M.NILI_CROPS)
            for pool, tot in (("summer", s), ("nili", n)):
                over = tot - par["land_limit"][d][pool]
                if over > worst_over:
                    worst_over, worst_cell = over, (d, pool, i)
    neg = min(min(plan["winter"].values()), min(plan["summer"].values()))
    print(f"  floor {pct}: file floor_share {share}; largest pool excess "
          f"{worst_over:.6f} ha at {worst_cell}; smallest area {neg:.6f} ha")

print("=" * 70)
print("Part 2. Recourse replay of each saved plan (no floor imposed)")
for pct in (50, 60, 70, 75, 80):
    plan, share = load_plan(PROC / f"plan_v5_floor{pct}.csv")
    ev = M.evaluate(par, plan, floor_share=0.0)
    floor_t = share * REF
    saved_margin = res["frontier_primary"][f"{share:.2f}"]
    print(f"  floor {pct}: all scenarios feasible {ev['all_feasible']}; "
          f"replayed expected margin {ev['margin']:,.2f} vs saved "
          f"{saved_margin:,.2f} (diff {ev['margin'] - saved_margin:,.2f}); "
          f"minimum scenario staple {ev['staple_min']:,.3f} vs floor "
          f"{floor_t:,.3f} (headroom {ev['staple_min'] - floor_t:,.3f} t)")

print("=" * 70)
print("Part 3. Cross solver replay with HiGHS")
prob, v = M.build(par, floor_share=0.80)
prob.solve(pulp.HiGHS(msg=False))
st = pulp.LpStatus[prob.status]
obj = float(pulp.value(prob.objective)) if st == "Optimal" else None
print(f"  floor 80 MIP under HiGHS: status {st}, objective "
      f"{obj:,.2f}" if obj else f"  floor 80 MIP under HiGHS: status {st}")
if obj:
    print(f"  saved CBC objective {res['frontier_primary']['0.80']:,.2f}; "
          f"difference {obj - res['frontier_primary']['0.80']:,.2f} "
          f"({100*(obj - res['frontier_primary']['0.80'])/res['frontier_primary']['0.80']:.5f} percent)")
prob2, v2 = M.build(par, objective="maxstaple")
prob2.solve(pulp.HiGHS(msg=False))
st2 = pulp.LpStatus[prob2.status]
if st2 == "Optimal":
    t = float(v2["t"].value())
    print(f"  ceiling under HiGHS: t {t:,.2f} tonnes, share {t/REF:.6f}; "
          f"saved share {res['ceiling_primary_share']:.6f}; "
          f"tonnage difference {t - res['ceiling_primary_share']*REF:,.2f}")
else:
    print(f"  ceiling under HiGHS: status {st2}")

print("=" * 70)
print("Part 4. Monotonicity spot checks by fresh CBC solves")
prob3, _ = M.build(par, floor_share=0.65)
st3 = M.solve(prob3)
m65 = float(pulp.value(prob3.objective)) if st3 == "Optimal" else None
print(f"  floor 65 (not on the printed ladder): status {st3}, margin "
      f"{m65:,.2f}" if m65 else f"  floor 65: status {st3}")
if m65:
    print(f"  lies between floor 60 {res['frontier_primary']['0.60']:,.2f} and "
          f"floor 70 {res['frontier_primary']['0.70']:,.2f}: "
          f"{res['frontier_primary']['0.70'] < m65 < res['frontier_primary']['0.60']}")
prob4, v4 = M.build(par, objective="maxstaple", budget_scale=1.05)
st4 = M.solve(prob4)
if st4 == "Optimal":
    t4 = float(v4["t"].value())
    print(f"  ceiling at budget scale 1.05: {t4:,.2f} tonnes; not below the "
          f"scale 1.00 ceiling {res['ceiling_primary_share']*REF:,.2f}: "
          f"{t4 >= res['ceiling_primary_share']*REF - 1.0}")
prob5, v5 = M.build(par, objective="maxstaple", budget_scale=0.95)
st5 = M.solve(prob5)
if st5 == "Optimal":
    t5 = float(v5["t"].value())
    print(f"  ceiling at budget scale 0.95: {t5:,.2f} tonnes; not above the "
          f"scale 1.00 ceiling: {t5 <= res['ceiling_primary_share']*REF + 1.0}")
print("DONE")
