"""Check 1, script C: the baseline contradiction. Evaluates the historical
pattern three ways: profit recourse delivery (the evaluate function the
build itself uses), staple maximising recourse per scenario (the capacity
reading the build uses for its own floored plans), and the hard floor test
(the pattern fixed, the floor imposed, feasibility read scenario by
scenario)."""
import importlib.util

ROOT = "/home/hatch/workspace/mit-projects/nile-delta-system"
spec = importlib.util.spec_from_file_location("m", ROOT + "/src/allocation_model_v4_1.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
par = m.load_all()
ref = par["reference_t"]

base_plan = {"winter": {(d, c): par["baseline"][c][d] for d in m.DISTRICTS for c in m.WINTER_CROPS},
             "summer": {(d, c, i): par["baseline"][c][d] for d in m.DISTRICTS
                        for c in m.LATE_CROPS for i in m.INFLOW_STATES}}

ev = m.evaluate(par, base_plan)
print(f"margin recourse: expected margin {ev['margin']:,.0f}")
print(f"margin recourse: expected staple {ev['staple_expected']:,.0f} "
      f"({100*ev['staple_expected']/ref:.2f} percent)")
print(f"margin recourse: minimum scenario staple {ev['staple_min']:,.0f} "
      f"({100*ev['staple_min']/ref:.2f} percent)")
for s in par["scenarios"]:
    st = ev["per"][s]["staple_t"]
    print(f"  {m.skey(*s)}: {st:,.0f} tonnes ({100*st/ref:.2f} percent)")

print("\nstaple maximising recourse per scenario (capacity of the fixed pattern):")
worst = None
for s in par["scenarios"]:
    prob, v = m.build(par, fixed=base_plan, objective="maxstaple", single_scenario=s)
    st = m.solve(prob, timelimit=300)
    t = float(v["t"].value()) if st == "Optimal" else None
    print(f"  {m.skey(*s)}: status {st} max staple {t:,.0f} ({100*t/ref:.2f} percent)")
    if t is not None and (worst is None or t < worst[1]):
        worst = (s, t)
print(f"worst scenario capacity: {worst[1]:,.0f} tonnes ({100*worst[1]/ref:.2f} percent) "
      f"in {m.skey(*worst[0])}")

for f in (0.50, 0.60, 0.65, 0.70):
    evf = m.evaluate(par, base_plan, floor_share=f)
    print(f"hard floor {f*100:.0f} percent imposed on the fixed pattern: "
          f"all 12 scenarios feasible = {evf['all_feasible']}")
