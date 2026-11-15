import sys
sys.path.insert(0, ".")
from audit_load import load, DISTRICTS, WINTER, SUMMER_ALL, ALLC
from audit_model import make, solve, val

P = load()
base_plan = {"winter": {(d, c): P["baseline"][c][d] for d in DISTRICTS for c in WINTER},
             "summer": {(d, c, i): P["baseline"][c][d] for d in DISTRICTS for c in SUMMER_ALL for i in ["dry", "normal", "high", "drought"]}}
for mip in (False, True):
    tot, sexp = 0.0, 0.0
    for s in P["scenarios"]:
        prob, v = make(P, floor=0.0, mip=mip, fixed=base_plan, scen=s)
        st = solve(prob, gap=0.0)
        rev = sum(P["price"][c][s[1]] * val(v["prod"][(d, c, s)]) for d in DISTRICTS for c in ALLC)
        cost = sum(P["cost"][c] * base_plan["winter"][(d, c)] for d in DISTRICTS for c in WINTER)
        cost += sum(P["cost"][c] * base_plan["summer"][(d, c, s[0])] for d in DISTRICTS for c in SUMMER_ALL)
        tot += P["prob"][s] * (rev - cost)
        sexp += P["prob"][s] * val(v["staple"][s])
        print(f"mip={mip} {s}: status {st} margin {rev-cost:,.0f} staple {val(v['staple'][s]):,.0f}")
    print(f"mip={mip} TOTAL margin {tot:,.1f} staple expected {sexp:,.1f}")
