import sys, time, random
sys.path.insert(0, ".")
import pandas as pd
from audit_load import load, DISTRICTS, WINTER, SUMMER_ALL, ALLC, STAPLES, INFLOW, LAYERS, LAYER_P
from audit_model import make, solve, val
import pulp

P = load()
REF = P["reference_t"]
PROC = P["flows"]  # placeholder
from pathlib import Path
BASE = Path(__file__).resolve().parents[3]

# ---------- 1. Evaluate the builder saved 70 percent plan in my recourse ----------
df = pd.read_csv(BASE / "data" / "processed" / "plan_v4_robust_plan.csv")
plan = {"winter": {}, "summer": {}}
for _, r in df.iterrows():
    if r.kind == "winter":
        plan["winter"][(r.district, r.crop)] = float(r.area)
    else:
        plan["summer"][(r.district, r.crop, r.inflow)] = float(r.area)
print("builder plan floor_share", df.floor_share.iloc[0])
tot = 0.0
for s in P["scenarios"]:
    prob, v = make(P, floor=0.70, mip=True, fixed=plan, scen=s)
    st = solve(prob, gap=0.0005)
    if st != "Optimal":
        print(f"builder plan scenario {s}: {st} (floor 0.70 not attainable)")
        # max staple attainable
        prob2, v2 = make(P, objective="maxexp", mip=True, fixed=plan, scen=s)
        st2 = solve(prob2, gap=0.0)
        mx = val(v2["staple"][s]) if st2 == "Optimal" else None
        print(f"   max staple attainable {mx:,.1f} = {100*mx/REF:.2f} pct" if mx else "   max staple failed")
        continue
    rev = sum(P["price"][c][s[1]] * val(v["prod"][(d, c, s)]) for d in DISTRICTS for c in ALLC)
    cost = sum(P["cost"][c] * plan["winter"][(d, c)] for d in DISTRICTS for c in WINTER)
    cost += sum(P["cost"][c] * plan["summer"][(d, c, s[0])] for d in DISTRICTS for c in SUMMER_ALL)
    stap = val(v["staple"][s])
    tot += P["prob"][s] * (rev - cost)
    print(f"builder plan scenario {s}: margin {rev-cost:,.0f} staple {stap:,.0f} ({100*stap/REF:.2f} pct)")
print(f"builder plan expected margin under my recourse: {tot:,.1f} (builder reports 194,764,695,263)")

# ---------- 2. Expected value problem at true means, my own solve ----------
mean_price = {c: sum(LAYER_P[l] * P["price"][c][l] for l in LAYERS) for c in ALLC}
mean_yield = {c: {l: {d: sum(LAYER_P[ll] * P["yield"][c][ll][d] for ll in LAYERS) for d in DISTRICTS} for l in LAYERS} for c in ALLC}
mean_price_d = {c: {l: mean_price[c] for l in LAYERS} for c in ALLC}
true_bcm = sum(P["inflow"]["probs"][i] * P["inflow"]["budgets"][i] for i in INFLOW)
print(f"true mean budget {true_bcm:.4f} BCM; true mean prices { {c: round(mean_price[c],1) for c in ALLC} }")
tp = sum(P["physical"].values())
Pmean = dict(P)
Pmean["budget"] = {(d, i): true_bcm * 1e9 * P["physical"][d] / tp for d in DISTRICTS for i in INFLOW}
s0 = ("normal", "expected")
prob, v = make(Pmean, floor=0.70, mip=True, scen=s0, price=mean_price_d, yld=mean_yield)
st = solve(prob, gap=0.0005)
print(f"EV problem status {st} objective {val(prob.objective):,.1f}")
ev = {"winter": {k: val(x) for k, x in v["xw"].items()},
      "summer": {(d, c, i): val(v["xs"][(d, c, "normal")]) for d in DISTRICTS for c in SUMMER_ALL for i in INFLOW}}
fails = 0
for s in P["scenarios"]:
    prob2, v2 = make(P, objective="maxexp", mip=True, fixed=ev, scen=s)
    st2 = solve(prob2, gap=0.0)
    mx = val(v2["staple"][s])
    ok = mx >= 0.70 * REF - 1.0
    fails += (not ok)
    print(f"EV plan max staple {s}: {mx:,.1f} = {100*mx/REF:.2f} pct floor70 {'HOLDS' if ok else 'FAILS'}")
print(f"EV plan fails floor in {fails} of 12 scenarios (builder says 10)")

# ---------- 3. Robustness: replicate draws, solve a subset with my code ----------
rng = random.Random(20261114)
flows = P["flows"]
mf = float(flows.mean())
windows = flows.rolling(10).mean().dropna().tolist()
draws = []
for n in range(100):
    if n % 2 == 0:
        draws.append((float(rng.choice(flows.tolist())) / mf, "single"))
    else:
        draws.append((float(rng.choice(windows)) / mf, "window"))
target_t = 0.70 * REF
subset = list(range(10)) + [20, 40, 60, 80]
res = {}
for n in subset:
    ratio, kind = draws[n]
    Pm = dict(P)
    tot_b = 11.00 * ratio * 1e9
    Pm["budget"] = {(d, i): tot_b * P["physical"][d] / tp for d in DISTRICTS for i in INFLOW}
    price_e = {c: {l: P["price"][c]["expected"] for l in LAYERS} for c in ALLC}
    yld_e = {c: {l: P["yield"][c]["expected"] for l in LAYERS} for c in ALLC}
    prob3, v3 = make(Pm, objective="maxexp", mip=True, fixed=plan, scen=("normal", "expected"), price=price_e, yld=yld_e)
    st3 = solve(prob3, gap=0.0)
    stap = val(v3["staple"][("normal", "expected")])
    res[n] = stap
    print(f"sample {n}: ratio {ratio:.3f} {kind} my max staple {stap:,.0f} share {100*stap/REF:.2f} shortfall {max(0.0, target_t-stap):,.0f} status {st3}")
print("log printed comparisons: s0 8,873,195 (72.41), s1 8,837,765 (72.12), s2 7,682,570 (62.69), s3 8,873,195, s4 8,821,675 (71.99), s20 8,408,159 (68.61), s40 8,603,009 (70.20), s60 8,549,373 (69.77), s80 8,873,195")
