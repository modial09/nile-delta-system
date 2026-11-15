import sys
sys.path.insert(0, ".")
import pulp
from audit_load import load, DISTRICTS, WINTER, SUMMER_ALL, ALLC, STAPLES, INFLOW, LAYERS, LAYER_P, MINV
from audit_model import make, solve, val

P = load()
REF = P["reference_t"]

# Wait and see: one deterministic floored problem per scenario, my code
ws = 0.0
for s in P["scenarios"]:
    price_o = {c: {l: P["price"][c][s[1]] for l in LAYERS} for c in ALLC}
    yld_o = {c: {l: P["yield"][c][s[1]] for l in LAYERS} for c in ALLC}
    Pm = dict(P)
    Pm["budget"] = {(d, i): P["budget"][(d, s[0])] for d in DISTRICTS for i in INFLOW}
    prob, v = make(Pm, floor=0.70, mip=True, scen=s, price=price_o, yld=yld_o)
    st = solve(prob, gap=0.0005)
    obj = val(prob.objective)
    ws += P["prob"][s] * obj
    print(f"WS {s}: {st} scenario margin {obj:,.0f} prob {P['prob'][s]:.4f}")
print(f"WS total {ws:,.1f} (builder 215,387,623,690) EVPI vs RP 194,764,695,263: {ws-194764695263:,.1f} (builder 20,622,928,427)")

# My EV plan (rebuilt as in run_ev_robust) evaluated with no floor and penalised
mean_price = {c: sum(LAYER_P[l] * P["price"][c][l] for l in LAYERS) for c in ALLC}
mean_yield = {c: {l: {d: sum(LAYER_P[ll] * P["yield"][c][ll][d] for ll in LAYERS) for d in DISTRICTS} for l in LAYERS} for c in ALLC}
mean_price_d = {c: {l: mean_price[c] for l in LAYERS} for c in ALLC}
true_bcm = sum(P["inflow"]["probs"][i] * P["inflow"]["budgets"][i] for i in INFLOW)
tp = sum(P["physical"].values())
Pmean = dict(P)
Pmean["budget"] = {(d, i): true_bcm * 1e9 * P["physical"][d] / tp for d in DISTRICTS for i in INFLOW}
prob, v = make(Pmean, floor=0.70, mip=True, scen=("normal", "expected"), price=mean_price_d, yld=mean_yield)
st = solve(prob, gap=0.0005)
ev = {"winter": {k: val(x) for k, x in v["xw"].items()},
      "summer": {(d, c, i): val(v["xs"][(d, c, "normal")]) for d in DISTRICTS for c in SUMMER_ALL for i in INFLOW}}
print(f"EV plan rebuilt, status {st}")

def recourse_pen(s, plan, penalty=None):
    prob = pulp.LpProblem("rp", pulp.LpMaximize)
    terms = []
    staple_terms = []
    for d in DISTRICTS:
        ws_ = []
        for c in ALLC:
            x = plan["winter"][(d, c)] if c in WINTER else plan["summer"][(d, c, s[0])]
            a = pulp.LpVariable(f"a_{d}_{c}", lowBound=0)
            w = pulp.LpVariable(f"w_{d}_{c}", lowBound=0)
            k = pulp.LpVariable(f"k_{d}_{c}", cat="Binary")
            big = max(x, 1.0)
            prob += a <= x
            prob += a <= big * k
            prob += a >= x - big * (1 - k)
            r = P["wreq"][c]
            prob += w <= r * a
            prob += w >= MINV * r * a
            y = P["yield"][c][s[1]][d]
            q = y * (1 - P["ky"][c]) * a + y * P["ky"][c] / r * w
            terms.append(P["price"][c][s[1]] * q)
            if c in STAPLES:
                staple_terms.append(q)
            ws_.append(w)
        prob += pulp.lpSum(ws_) <= P["budget"][(d, s[0])]
    cost = sum(P["cost"][c] * plan["winter"][(d, c)] for d in DISTRICTS for c in WINTER)
    cost += sum(P["cost"][c] * plan["summer"][(d, c, s[0])] for d in DISTRICTS for c in SUMMER_ALL)
    margin = pulp.lpSum(terms) - cost
    if penalty is None:
        prob += margin
        prob.solve(pulp.PULP_CBC_CMD(msg=False, timeLimit=600, gapRel=0.0))
        return float(pulp.value(prob.objective)), sum(float(pulp.value(q)) for q in staple_terms)
    sv = pulp.LpVariable("sv", lowBound=0)
    prob += pulp.lpSum(staple_terms) + sv >= 0.70 * REF
    prob += margin - penalty * sv
    prob.solve(pulp.PULP_CBC_CMD(msg=False, timeLimit=600, gapRel=0.0))
    return float(pulp.value(prob.objective)), float(sv.value())

nf_tot, pen_tot = 0.0, 0.0
for s in P["scenarios"]:
    m_nf, stap = recourse_pen(s, ev, penalty=None)
    m_pen, short = recourse_pen(s, ev, penalty=25000.0)
    nf_tot += P["prob"][s] * m_nf
    pen_tot += P["prob"][s] * m_pen
    print(f"EV eval {s}: no floor margin {m_nf:,.0f} staple {stap:,.0f} | penalised margin {m_pen:,.0f} shortfall {short:,.0f}")
print(f"EV plan no floor expected {nf_tot:,.1f} (builder 209,970,047,975, for their EV plan)")
print(f"EV plan penalised expected {pen_tot:,.1f} (builder 187,415,904,232) penalised VSS vs RP: {194764695263-pen_tot:,.1f} (builder 7,348,791,030)")
