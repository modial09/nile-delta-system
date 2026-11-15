"""Check 1, script E3: per scenario diagnosis of the saved plans under
their own hard floor: status of the floored single scenario solve and
the staple maximising headroom in every scenario."""
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


for pct in (50, 80):
    plan, share = load_plan(ROOT + f"/data/processed/plan_v4_1_floor{pct}.csv")
    floor_t = share * ref
    print(f"== floor {pct} plan, floor tonnage {floor_t:,.1f} ==")
    for s in par["scenarios"]:
        prob, v = m.build(par, fixed=plan, objective="maxstaple", single_scenario=s)
        st = m.solve(prob, timelimit=300)
        t = float(v["t"].value()) if st == "Optimal" else float("nan")
        prob2, v2 = m.build(par, fixed=plan, floor_share=share, single_scenario=s)
        st2 = m.solve(prob2, timelimit=300)
        print(f"  {m.skey(*s)}: max staple {t:,.3f} headroom {t - floor_t:+.3f} t "
              f"| hard floor solve status {st2}")
