import sys
sys.path.insert(0, ".")
import pulp
from audit_load import load, DISTRICTS, WINTER, SUMMER_ALL, ALLC, MINV
P = load()
base = {"winter": {(d, c): P["baseline"][c][d] for d in DISTRICTS for c in WINTER},
        "summer": {(d, c, i): P["baseline"][c][d] for d in DISTRICTS for c in SUMMER_ALL for i in ["dry", "normal", "high", "drought"]}}

def recourse(s, big_mode, wscale):
    """wscale: 1.0 water in m3, 1000.0 water in thousand m3 units."""
    prob = pulp.LpProblem("r", pulp.LpMaximize)
    terms = []
    staple = 0.0
    for d in DISTRICTS:
        ws = []
        for c in ALLC:
            x = base["winter"][(d, c)] if c in WINTER else base["summer"][(d, c, s[0])]
            a = pulp.LpVariable(f"a_{d}_{c}", lowBound=0)
            w = pulp.LpVariable(f"w_{d}_{c}", lowBound=0)
            k = pulp.LpVariable(f"k_{d}_{c}", cat="Binary")
            big = P["physical"][d] if big_mode == "physical" else max(x, 1.0)
            prob += a <= x
            prob += a <= big * k
            prob += a >= x - big * (1 - k)
            r = P["wreq"][c] / wscale
            prob += w <= r * a
            prob += w >= MINV * r * a
            y = P["yield"][c][s[1]][d]
            q = y * (1 - P["ky"][c]) * a + y * P["ky"][c] / r * w
            terms.append(P["price"][c][s[1]] * q)
            if c in ("Wheat", "Rice", "Maize_summer"):
                staple = staple + q
            ws.append(w)
        prob += pulp.lpSum(ws) <= P["budget"][(d, s[0])] / wscale
    cost = sum(P["cost"][c] * base["winter"][(d, c)] for d in DISTRICTS for c in WINTER)
    cost += sum(P["cost"][c] * base["summer"][(d, c, s[0])] for d in DISTRICTS for c in SUMMER_ALL)
    prob += pulp.lpSum(terms) - cost
    prob.solve(pulp.PULP_CBC_CMD(msg=False, timeLimit=600, gapRel=0.0))
    return pulp.LpStatus[prob.status], float(pulp.value(prob.objective))

for s in [("dry", "expected"), ("normal", "expected")]:
    for big_mode, wscale in [("physical", 1.0), ("physical", 1000.0), ("tight", 1.0), ("tight", 1000.0)]:
        st, obj = recourse(s, big_mode, wscale)
        print(f"{s} big={big_mode} wscale={wscale}: {st} margin {obj:,.1f}")
print("mine earlier MIP: dry_expected 47,116,475,768 ; normal_expected 64,254,553,588")
