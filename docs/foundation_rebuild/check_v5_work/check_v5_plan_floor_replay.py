"""Follow up to check_v5_plans.py Part 2.

Replays the saved floor 50 and floor 80 plans through the recourse
evaluation WITH the plan floor imposed, the same condition the
frontier solve optimised under. If the plan plus a floor holding
recourse reproduces the saved frontier margin, the Part 2 gap is
fully explained by the recourse freedom, not by a plan defect.
Changes no existing file. Run with PYTHONDONTWRITEBYTECODE=1.
"""
import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))
import allocation_model_v5 as M  # noqa: E402

PROC = ROOT / "data" / "processed"
par = M.load_all()
res = json.loads((PROC / "results_v5_main.json").read_text())


def load_plan(path):
    df = pd.read_csv(path)
    plan = {"winter": {}, "summer": {}}
    for _, r in df.iterrows():
        if r["kind"] == "winter":
            plan["winter"][(r["district"], r["crop"])] = float(r["area"])
        else:
            plan["summer"][(r["district"], r["crop"], r["inflow"])] = float(r["area"])
    return plan, float(df["floor_share"].iloc[0])


for pct in (50, 80):
    plan, share = load_plan(PROC / f"plan_v5_floor{pct}.csv")
    ev = M.evaluate(par, plan, floor_share=share)
    saved = res["frontier_primary"][f"{share:.2f}"]
    print(f"floor {pct}: all scenarios feasible with the floor imposed: "
          f"{ev['all_feasible']}")
    print(f"  expected margin under floor holding recourse: {ev['margin']:,.2f}")
    print(f"  saved frontier margin: {saved:,.2f}; difference: "
          f"{ev['margin'] - saved:,.2f}")
    print(f"  minimum scenario staple: {ev['staple_min']:,.3f} against floor "
          f"{share * par['reference_t']:,.3f}")
print("DONE")
