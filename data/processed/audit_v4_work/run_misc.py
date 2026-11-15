import sys
sys.path.insert(0, ".")
import pandas as pd
from pathlib import Path
from audit_load import load, DISTRICTS, WINTER, SUMMER_ALL, SUMMER_TRUE, NILI, ALLC, GROUP
from audit_model import make, solve, val

P = load()
REF = P["reference_t"]
BASE = Path(__file__).resolve().parents[3]

# Baseline evaluation, my recourse per scenario, no floor
base_plan = {"winter": {(d, c): P["baseline"][c][d] for d in DISTRICTS for c in WINTER},
             "summer": {(d, c, i): P["baseline"][c][d] for d in DISTRICTS for c in SUMMER_ALL for i in ["dry", "normal", "high", "drought"]}}
tot, sexp, smin = 0.0, 0.0, None
for s in P["scenarios"]:
    prob, v = make(P, floor=0.0, mip=True, fixed=base_plan, scen=s)
    st = solve(prob, gap=0.0)
    rev = sum(P["price"][c][s[1]] * val(v["prod"][(d, c, s)]) for d in DISTRICTS for c in ALLC)
    cost = sum(P["cost"][c] * base_plan["winter"][(d, c)] for d in DISTRICTS for c in WINTER)
    cost += sum(P["cost"][c] * base_plan["summer"][(d, c, s[0])] for d in DISTRICTS for c in SUMMER_ALL)
    stap = val(v["staple"][s])
    tot += P["prob"][s] * (rev - cost); sexp += P["prob"][s] * stap
    smin = stap if smin is None else min(smin, stap)
print(f"baseline my evaluation: margin {tot:,.1f} (builder 79,671,400,397) staple expected {sexp:,.1f} (builder 8,225,526) min {smin:,.1f} (builder 6,774,438)")

# Modeled baseline full applied demand
dem = sum(P["baseline"][c][d] * P["wreq"][c] for c in ALLC for d in DISTRICTS) / 1e9
print(f"modeled baseline full applied demand {dem:.3f} BCM (builder 16.398)")
wp = pd.read_csv(BASE / "data" / "external" / "wapor_aeti_governorate_2018_2025.csv")
wm = wp[wp.governorate.isin(DISTRICTS)].groupby("governorate").consumption_billion_cubic_metres.mean()
print(f"WaPOR 8 governorate mean total {wm.sum():.3f} BCM (builder 24.416); per gov modeled vs WaPOR:")
for d in DISTRICTS:
    md = sum(P["baseline"][c][d] * P["wreq"][c] for c in ALLC) / 1e9
    print(f"  {d}: modeled {md:.3f} WaPOR {wm[d]:.3f} below={md < wm[d]}")

# v3 rescaled yields sensitivity on ceiling (factors applied on top of v4 scaled yields, as builder did)
factors = {"wheat": 0.95760, "rice_paddy": 1.00181, "maize": 0.83879, "sugar_beet": 1.05705, "potatoes": 0.98940}
yover = {c: {l: {d: P["yield"][c][l][d] * factors[GROUP[c]] for d in DISTRICTS} for l in ["low", "expected", "high"]} for c in ALLC}
prob, v = make(P, objective="maxmin", mip=False, yld=yover)
st = solve(prob, gap=0.0)
print(f"rescaled sensitivity ceiling: {val(v['t']):,.1f} = {100*val(v['t'])/REF:.2f} pct (builder 8,531,954 = 69.62 pct)")

# Ceiling solution crop mix and binding scenario (LP)
prob, v = make(P, objective="maxmin", mip=False)
st = solve(prob, gap=0.0)
print("ceiling LP staple by scenario:")
for s in P["scenarios"]:
    print(f"  {s}: {val(v['staple'][s]):,.0f}")
print("ceiling LP planted (winter shared; summer by inflow):")
for c in ["Wheat", "Rice", "Maize_summer", "Sugar beet"]:
    if c in WINTER:
        print(f"  {c}: {sum(val(v['xw'][(d, c)]) for d in DISTRICTS):,.0f} ha")
    else:
        for i in ["dry", "normal", "high", "drought"]:
            print(f"  {c} [{i}]: {sum(val(v['xs'][(d, c, i)]) for d in DISTRICTS):,.0f} ha")

# Seasonal fit under the three pool construction
for d in DISTRICTS:
    w = sum(P["baseline"][c][d] for c in WINTER)
    s = sum(P["baseline"][c][d] for c in SUMMER_TRUE)
    n = sum(P["baseline"][c][d] for c in NILI)
    un = P["annual"][d] - (w + s + n); tot = w + s + n
    lw = P["physical"][d] - un * w / tot; ls = P["physical"][d] - un * s / tot; ln = P["physical"][d] - un * n / tot
    print(f"3pool fit {d}: winter slack {lw-w:,.0f} summer slack {ls-s:,.0f} nili slack {ln-n:,.0f}")

# Frontier arithmetic from the logs, to the pound
unc = 429588780373
for lv, m in [(0.50, 290166264371), (0.60, 243671396588), (0.70, 194764695263)]:
    print(f"frontier {lv}: cost vs unc {unc-m:,} cost vs prev check")
prev = unc
for lv, m in [(0.50, 290166264371), (0.60, 243671396588), (0.70, 194764695263)]:
    print(f"  level {lv} vs next lower {prev-m:,}")
    prev = m
print(f"penalised VSS subtraction: {194764695263-187415904232:,} (note prints 7,348,791,030)")
print(f"EVPI subtraction: {215387623690-194764695263:,} (note prints 20,622,928,427)")
print(f"baseline diff: {429588780373-79671400397:,} pct {100*(429588780373-79671400397)/79671400397:.2f} (note 349,917,379,976 and 439.20)")
print(f"robust floor reference: {0.70*REF:,.1f} (note 8,578,085)")
print(f"768 binaries check: {8*8*12}")
