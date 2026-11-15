"""Check 1, script E2: corrections to script E. Evaluates the saved plans
with their own floor held in the recourse, as the recovery record does,
and reruns the abandonment scan with tolerances scaled to the solver
feasibility tolerance."""
import importlib.util

import pandas as pd

ROOT = "/home/hatch/workspace/mit-projects/nile-delta-system"
spec = importlib.util.spec_from_file_location("m", ROOT + "/src/allocation_model_v4_1.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
par = m.load_all()
ref = par["reference_t"]


def load_plan(path):
    df = pd.read_csv(path)
    plan = {"winter": {}, "summer": {}}
    for _, r in df.iterrows():
        if r["kind"] == "winter":
            plan["winter"][(r["district"], r["crop"])] = float(r["area"])
        else:
            plan["summer"][(r["district"], r["crop"], r["inflow"])] = float(r["area"])
    return plan, float(df["floor_share"].iloc[0])


printed = {50: 297739198932, 80: 175143528384}
for pct in (50, 80):
    plan, share = load_plan(ROOT + f"/data/processed/plan_v4_1_floor{pct}.csv")
    ev = m.evaluate(par, plan, floor_share=share)
    print(f"floor {pct} with its floor held in recourse: all feasible {ev['all_feasible']} "
          f"| margin {ev['margin']:,.0f} | printed {printed[pct]:,} "
          f"| difference {ev['margin'] - printed[pct]:,.0f}")

plan, share = load_plan(ROOT + "/data/processed/plan_v4_1_floor80.csv")
ev0 = m.evaluate(par, plan)
print(f"\nfloor 80 plan under profit recourse with no floor held: margin "
      f"{ev0['margin']:,.0f} | worst scenario staple {ev0['staple_min']:,.0f} "
      f"({100*ev0['staple_min']/ref:.2f} percent, against its 80 percent floor)")

print("\n== abandonment scan with solver scale tolerances ==")
for s in (("dry", "low"), ("drought", "low")):
    prob, v = m.build(par, fixed=plan, single_scenario=s)
    st = m.solve(prob, timelimit=300)
    n_ab = n_kept = n_zero = 0
    bad = []
    for d in m.DISTRICTS:
        for c in m.ALL_CROPS:
            x = plan["winter"][(d, c)] if c in m.WINTER_CROPS else plan["summer"][(d, c, s[0])]
            a = float(v["kept"][(d, c, s)].value())
            w = float(v["wat"][(d, c, s)].value())
            q = float(v["prod"][(d, c, s)].value())
            duty = par["water_req"][c] / 1000.0
            if x <= 1e-9:
                n_zero += 1
                if a > 1e-4 or w > 1e-4 or q > 1e-4:
                    bad.append((d, c, "unplanted cell active", a, w, q))
            elif a <= 1e-9 * max(1.0, x):
                n_ab += 1
                if w > 1e-4 or q > 1e-4:
                    bad.append((d, c, "abandoned but water or output positive", w, q))
            else:
                n_kept += 1
                tol_w = 1e-6 * max(1.0, duty * a)
                if w < m.MIN_VIABLE_SHARE * duty * a - tol_w or w > duty * a + tol_w:
                    bad.append((d, c, "kept water outside its band", w, duty * a))
                if a > x + 1e-6 * max(1.0, x):
                    bad.append((d, c, "kept area above planted area", a, x))
    print(f"{m.skey(*s)}: status {st} | abandoned planted cells {n_ab} | kept {n_kept} "
          f"| unplanted {n_zero} | violations {len(bad)}")
    for b in bad[:6]:
        print("   ", b)
