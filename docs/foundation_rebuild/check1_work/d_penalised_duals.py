"""Check 1, script D: penalised stochastic optimum, monotonicity probes,
and the dual provenance test (CBC against HiGHS on the same relaxation)."""
import importlib.util

import pulp

ROOT = "/home/hatch/workspace/mit-projects/nile-delta-system"
spec = importlib.util.spec_from_file_location("m", ROOT + "/src/allocation_model_v4_1.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
par = m.load_all()
RP = 175143528384.0

print("== penalised stochastic problem at floor 0.80, penalty 25000 per tonne ==")
prob, v = m.build(par, floor_share=0.80, penalise_floor=25000.0)
st = m.solve(prob)
obj = float(pulp.value(prob.objective))
short = {s: float(v["shortfall"][s].value()) for s in par["scenarios"]}
print(f"status {st} | penalised optimum objective {obj:,.0f}")
print(f"hard floor RP printed: {RP:,.0f} | difference {obj - RP:,.0f}")
print("shortfalls by scenario:", {m.skey(*s): round(x) for s, x in short.items() if x > 0.5})
print(f"printed penalised VSS used RP as its stochastic side: {RP - 167535664790:,.0f}")
print(f"penalised VSS with the true penalised optimum: {obj - 167535664790:,.0f}")

print("\n== monotonicity probes ==")
prob, v = m.build(par, floor_share=0.65)
st = m.solve(prob)
print(f"margin at floor 0.65: status {st} objective {float(pulp.value(prob.objective)):,.0f} "
      f"(must sit between 262,520,406,731 at 0.60 and 223,222,240,454 at 0.70)")
prob, v = m.build(par, objective="maxstaple", budget_scale=0.95)
st = m.solve(prob)
print(f"ceiling at budget scale 0.95: status {st} t {float(v['t'].value()):,.0f} "
      f"(must sit between 9,049,077 at 0.90 and 9,833,867 at 1.00)")
prob, v = m.build(par, floor_share=0.0, budget_scale=0.95)
st = m.solve(prob)
print(f"unconstrained margin at budget scale 0.95: status {st} "
      f"objective {float(pulp.value(prob.objective)):,.0f} "
      f"(must sit between 375,091,832,795 at 0.90 and 403,078,762,407 at 1.00)")

print("\n== dual provenance at floor 0.8015 ==")
prob, v = m.build(par, floor_share=0.8015)
st = m.solve(prob)
mip_obj = float(pulp.value(prob.objective))
print(f"MIP margin at floor 0.8015 (CBC): status {st} objective {mip_obj:,.0f}")


def duals_of(prob):
    out = {}
    for name, con in prob.constraints.items():
        if name.startswith("Water_"):
            rest = name[len("Water_"):]
            for s in par["scenarios"]:
                sk = m.skey(*s)
                if rest.endswith("_" + sk):
                    dname = rest[: -len(sk) - 1].replace("_", " ")
                    raw = abs(float(con.pi)) / 1000.0 if con.pi is not None else float("nan")
                    out[(dname, s[0], s[1])] = raw / par["prob"][s]
    return out


prob, v = m.build(par, floor_share=0.8015, relax=True)
st = m.solve(prob, gap=0.0)
lp_cbc = float(pulp.value(prob.objective))
d_cbc = duals_of(prob)
print(f"LP relaxation (CBC): status {st} objective {lp_cbc:,.0f} "
      f"(run log prints 174,088,745,148) | LP minus MIP at same floor {lp_cbc - mip_obj:,.0f}")

prob2, v2 = m.build(par, floor_share=0.8015, relax=True)
prob2.solve(pulp.HiGHS(msg=False))
lp_highs = float(pulp.value(prob2.objective))
d_highs = duals_of(prob2)
print(f"LP relaxation (HiGHS): objective {lp_highs:,.0f} | difference from CBC {lp_highs - lp_cbc:,.0f}")
diffs = []
for k in d_cbc:
    if abs(d_cbc[k] - d_highs.get(k, 0.0)) > 0.01:
        diffs.append((k, d_cbc[k], d_highs.get(k, 0.0)))
print(f"dual cells differing between the two solvers by more than 0.01: {len(diffs)} of {len(d_cbc)}")
for k, a, b in diffs[:12]:
    print(f"  {k}: CBC {a:,.2f} | HiGHS {b:,.2f}")
key = ("Damietta", "normal", "expected")
print(f"Damietta normal expected: CBC {d_cbc.get(key):,.2f} | HiGHS {d_highs.get(key):,.2f} "
      f"(note quotes the printed solution range minimum as 19.17 and a second "
      f"optimal dual solution at 16.68)")
rng = [d_cbc[(d, "normal", "expected")] for d in m.DISTRICTS]
print(f"CBC normal expected range: {min(rng):.2f} to {max(rng):.2f} (note prints 19.17 to 53.54)")
