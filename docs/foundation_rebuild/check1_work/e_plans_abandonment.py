"""Check 1, script E: saved plan integrity and abandonment mechanics.
Reads the saved plan CSVs, checks pool limits against the model land
limits, replays each saved plan's own floor by staple maximising recourse,
reproduces a saved plan margin by evaluation, and inspects the keep,
water and production variables of a fixed plan solve cell by cell."""
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


print("== pool limit check on every saved plan ==")
for pct in (50, 60, 70, 75, 80):
    plan, share = load_plan(ROOT + f"/data/processed/plan_v4_1_floor{pct}.csv")
    worst = 0.0
    for d in m.DISTRICTS:
        s = sum(plan["winter"][(d, c)] for c in m.WINTER_CROPS)
        worst = max(worst, s - par["land_limit"][d]["winter"])
        for i in m.INFLOW_STATES:
            s = sum(plan["summer"][(d, c, i)] for c in m.SUMMER_CROPS)
            worst = max(worst, s - par["land_limit"][d]["summer"])
            s = sum(plan["summer"][(d, c, i)] for c in m.NILI_CROPS)
            worst = max(worst, s - par["land_limit"][d]["nili"])
    print(f"floor {pct}: largest pool excess over its limit {worst:.2e} hectares")

print("\n== saved plan margins by independent evaluation ==")
printed = {50: 297739198932, 60: 262520406731, 70: 223222240454,
           75: 202983384826, 80: 175143528384}
for pct in (50, 80):
    plan, share = load_plan(ROOT + f"/data/processed/plan_v4_1_floor{pct}.csv")
    ev = m.evaluate(par, plan)
    print(f"floor {pct}: evaluated margin {ev['margin']:,.0f} | printed {printed[pct]:,} "
          f"| difference {ev['margin'] - printed[pct]:,.0f}")

print("\n== saved plan floor replay by staple maximising recourse ==")
for pct in (70, 80):
    plan, share = load_plan(ROOT + f"/data/processed/plan_v4_1_floor{pct}.csv")
    floor_t = share * ref
    worst = None
    for s in par["scenarios"]:
        prob, v = m.build(par, fixed=plan, objective="maxstaple", single_scenario=s)
        st = m.solve(prob, timelimit=300)
        t = float(v["t"].value())
        if worst is None or t - floor_t < worst[1]:
            worst = (s, t - floor_t)
    print(f"floor {pct}: smallest headroom {worst[1]:+.3f} tonnes in {m.skey(*worst[0])} "
          f"(note prints +0.007 for the 80 plan and minus 0.015 for the 70 plan, "
          f"both in drought at the low layer)")

print("\n== abandonment mechanics, floor 80 plan ==")
plan, share = load_plan(ROOT + "/data/processed/plan_v4_1_floor80.csv")
for s in (("dry", "low"), ("drought", "low")):
    prob, v = m.build(par, fixed=plan, single_scenario=s)
    st = m.solve(prob, timelimit=300)
    n_ab = n_kept = 0
    bad = []
    for d in m.DISTRICTS:
        for c in m.ALL_CROPS:
            x = plan["winter"][(d, c)] if c in m.WINTER_CROPS else plan["summer"][(d, c, s[0])]
            a = float(v["kept"][(d, c, s)].value())
            w = float(v["wat"][(d, c, s)].value())
            q = float(v["prod"][(d, c, s)].value())
            duty = par["water_req"][c] / 1000.0
            y = par["yield"][c][s[1]][d]
            q_expect = y * (1 - par["ky"][c]) * a + (y * par["ky"][c] / duty) * w
            if abs(q - q_expect) > 1e-4 * max(1.0, abs(q)):
                bad.append((d, c, "production formula", q, q_expect))
            if x > 1e-9 and a <= 1e-9:
                n_ab += 1
                if w > 1e-6 or q > 1e-6:
                    bad.append((d, c, "abandoned but water or output positive", w, q))
            elif a > 1e-9:
                n_kept += 1
                if w < m.MIN_VIABLE_SHARE * duty * a - 1e-6 or w > duty * a + 1e-6:
                    bad.append((d, c, "kept water outside its band", w, duty * a))
                if a > x + 1e-6:
                    bad.append((d, c, "kept area above planted area", a, x))
    print(f"{m.skey(*s)}: status {st} | planted cells abandoned {n_ab} | kept {n_kept} "
          f"| violations {len(bad)}")
    for b in bad[:6]:
        print("   ", b)
