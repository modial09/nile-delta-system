"""Independent audit code for version 4.1. Written from the raw CSV
files and the stated specification only. This module never imports
the model under audit. Water is carried in cubic metres throughout
(the builder carries thousands of cubic metres). Binary linkage
bound for a plan being optimised: the pool land limit of the cell.
For a fixed plan under evaluation: the planted area of the cell
itself, unless a caller asks for another bound to test it.
"""
import copy
from pathlib import Path

import pandas as pd
import pulp

BASE = Path(__file__).resolve().parents[3]
EXT = BASE / "data" / "external"
PROC = BASE / "data" / "processed"

D = ["Beheira", "Sharkia", "Dakahlia", "Kafr El Sheikh",
     "Gharbia", "Menoufia", "Qalyubia", "Damietta"]
W_CROPS = ["Wheat", "Sugar beet", "Potatoes_winter"]
S_CROPS = ["Rice", "Maize_summer", "Potatoes_summer"]
N_CROPS = ["Maize_nili", "Potatoes_nili"]
L_CROPS = S_CROPS + N_CROPS
A_CROPS = W_CROPS + L_CROPS
POOLS = {"winter": W_CROPS, "summer": S_CROPS, "nili": N_CROPS}
POOL_OF = {c: p for p, cs in POOLS.items() for c in cs}
STAPLES = ["Wheat", "Rice", "Maize_summer"]
GROUP = {"Wheat": "wheat", "Sugar beet": "sugar_beet", "Potatoes_winter": "potatoes",
         "Rice": "rice_paddy", "Maize_summer": "maize", "Maize_nili": "maize",
         "Potatoes_summer": "potatoes", "Potatoes_nili": "potatoes"}
INF = ["dry", "normal", "high", "drought"]
LAY = ["low", "expected", "high"]
LPROB = {"low": 0.25, "expected": 0.50, "high": 0.25}
ANCHOR = 11.00
MIN_SHARE = 0.30
COST = {"Wheat": 37742.86, "Sugar beet": 39454.76, "Rice": 41850.00,
        "Maize_summer": 37671.43, "Maize_nili": 37888.10,
        "Potatoes_summer": 86657.14, "Potatoes_nili": 54176.19,
        "Potatoes_winter": 86657.14}
WREQ = {"Wheat": 5126.0, "Rice": 16600.0, "Maize_summer": 9305.0,
        "Maize_nili": 7433.0, "Sugar beet": 6100.0,
        "Potatoes_winter": 4079.0, "Potatoes_summer": 6145.0,
        "Potatoes_nili": 6145.0}
KY = {"Wheat": 1.05, "Rice": 1.20, "Maize_summer": 1.25, "Maize_nili": 1.25,
      "Sugar beet": 1.00, "Potatoes_winter": 1.10, "Potatoes_summer": 1.10,
      "Potatoes_nili": 1.10}
CAPS = {"Wheat": 0.50, "Sugar beet": 0.30, "Potatoes_winter": 0.15,
        "Rice": 0.35, "Maize_summer": 0.40, "Maize_nili": 0.40,
        "Potatoes_summer": 0.15, "Potatoes_nili": 0.15}


def _amap(df, crop, season, year, col):
    sub = df[(df["crop"] == crop) & (df["season"] == season)
             & (df["agricultural_year"] == year)]
    out = {}
    for d in D:
        row = sub[sub["governorate"] == d]
        v = float(row[col].iloc[0]) if len(row) else 0.0
        out[d] = 0.0 if pd.isna(v) else v
    return out


def _ymap(df, crop, season, year):
    sub = df[(df["crop"] == crop) & (df["season"] == season)
             & (df["agricultural_year"] == year)]
    out = {}
    for d in D:
        row = sub[sub["governorate"] == d]
        out[d] = float(row["yield_tons_per_hectare"].iloc[0]) if len(row) else float("nan")
    return out


def load():
    par = {}
    area = pd.read_csv(EXT / "capmas_governorate_area.csv")
    yldf = pd.read_csv(EXT / "capmas_governorate_yield.csv")
    tot = pd.read_csv(EXT / "capmas_governorate_total_cropped_area.csv")
    nili = pd.read_csv(EXT / "nili_maize_governorate_2020_2021.csv")
    pot = pd.read_csv(EXT / "potato_season_split.csv")
    fc = pd.read_csv(PROC / "forecast_prices_yields_v4.csv")
    inflow = pd.read_csv(EXT / "nile_inflow_aswan_series.csv")

    pr = tot[(tot["agricultural_year"] == "2020/2021") & (tot["measure"] == "cultivated_area")]
    par["physical"] = {d: float(pr.loc[pr["governorate"] == d, "area_hectares"].iloc[0]) for d in D}
    ar = tot[(tot["agricultural_year"] == "2020/2021") & (tot["measure"] == "total_cropped_area")]
    par["annual"] = {d: float(ar.loc[ar["governorate"] == d, "area_hectares"].iloc[0]) for d in D}

    base = {}
    base["Wheat"] = _amap(area, "wheat", "winter", "2020/2021", "area_hectares")
    base["Sugar beet"] = _amap(area, "sugar_beet", "winter", "2020/2021", "area_hectares")
    base["Rice"] = _amap(area, "rice", "summer", "2020/2021", "area_hectares")
    base["Maize_summer"] = _amap(area, "maize", "summer", "2020/2021", "area_hectares")
    nm = nili[nili["crop"] == "maize"]
    base["Maize_nili"] = {}
    pub = {}
    pub["Maize_nili"] = {}
    for d in D:
        row = nm[nm["governorate"] == d]
        v = float(row["area_hectares"].iloc[0]) if len(row) else 0.0
        base["Maize_nili"][d] = 0.0 if pd.isna(v) else v
        pub["Maize_nili"][d] = float(row["yield_tons_per_hectare"].iloc[0]) if len(row) else float("nan")
    for crop, season in [("Potatoes_winter", "winter"), ("Potatoes_summer", "summer"),
                         ("Potatoes_nili", "nili")]:
        sub = pot[pot["season"] == season]
        base[crop] = {}
        pub[crop] = {}
        for d in D:
            row = sub[sub["governorate"] == d]
            v = float(row["area_hectares"].iloc[0]) if len(row) else 0.0
            base[crop][d] = 0.0 if pd.isna(v) else v
            pub[crop][d] = float(row["yield_tons_per_hectare"].iloc[0]) if len(row) else float("nan")
    if base["Rice"]["Menoufia"] == 0.0:
        fill = area[(area["crop"] == "rice") & (area["season"] == "summer")
                    & (area["agricultural_year"] == "2019/2020")
                    & (area["governorate"] == "Menoufia")]
        base["Rice"]["Menoufia"] = float(fill["area_hectares"].iloc[0])
    par["baseline"] = base

    pub["Wheat"] = _ymap(yldf, "wheat", "winter", "2020/2021")
    pub["Sugar beet"] = _ymap(yldf, "sugar_beet", "winter", "2020/2021")
    pub["Rice"] = _ymap(yldf, "rice", "summer", "2020/2021")
    pub["Maize_summer"] = _ymap(yldf, "maize", "summer", "2020/2021")
    par["yield_fills"] = []
    for crop in A_CROPS:
        known = [d for d in D if not pd.isna(pub[crop][d])]
        wsum = sum(base[crop][d] for d in known)
        fv = (sum(pub[crop][d] * base[crop][d] for d in known) / wsum if wsum > 0
              else sum(pub[crop][d] for d in known) / len(known))
        for d in D:
            if pd.isna(pub[crop][d]):
                pub[crop][d] = fv
                par["yield_fills"].append((crop, d, fv))
    par["published"] = pub

    pf, yf = {}, {}
    for _, r in fc.iterrows():
        e = {"forecast": float(r["forecast_value"]), "low": float(r["band_low"]),
             "high": float(r["band_high"]), "rmse": float(r["backtest_rmse"]),
             "mape": float(r["backtest_mape_pct"]), "model": r["selected_model"]}
        (pf if r["target"] == "price" else yf)[r["crop"]] = e
    par["price_fc"], par["yield_fc"] = pf, yf
    par["price"] = {c: {"low": pf[GROUP[c]]["low"], "expected": pf[GROUP[c]]["forecast"],
                        "high": pf[GROUP[c]]["high"]} for c in A_CROPS}
    par["yield"] = {}
    for c in A_CROPS:
        f = yf[GROUP[c]]
        par["yield"][c] = {}
        for st, ratio in [("low", f["low"] / f["forecast"]), ("expected", 1.0),
                          ("high", f["high"] / f["forecast"])]:
            par["yield"][c][st] = {d: pub[c][d] * ratio for d in D}
    par["yield_scaled"] = {}
    par["yield_scale"] = {}
    for c in A_CROPS:
        f = yf[GROUP[c]]
        wsum = sum(base[c].values())
        wmean = (sum(pub[c][d] * base[c][d] for d in D) / wsum if wsum > 0
                 else sum(pub[c].values()) / len(D))
        sc = f["forecast"] / wmean
        par["yield_scale"][c] = sc
        par["yield_scaled"][c] = {}
        for st, ratio in [("low", f["low"] / f["forecast"]), ("expected", 1.0),
                          ("high", f["high"] / f["forecast"])]:
            par["yield_scaled"][c][st] = {d: pub[c][d] * sc * ratio for d in D}

    par["reference_t"] = sum(base[c][d] * pub[c][d] for c in STAPLES for d in D)
    par["reference_by_crop"] = {c: sum(base[c][d] * pub[c][d] for d in D) for c in STAPLES}

    # Reserve, capped construction as stated in the note, plus the
    # uncapped proportional variant kept alongside for the attack.
    par["reserve"] = {}
    par["land_limit"] = {}
    par["land_limit_uncapped"] = {}
    par["check"] = []
    for d in D:
        obs = {p: sum(base[c][d] for c in cs) for p, cs in POOLS.items()}
        unmod = par["annual"][d] - sum(obs.values())
        tot_obs = sum(obs.values())
        par["reserve"][d] = {}
        par["land_limit"][d] = {}
        par["land_limit_uncapped"][d] = {}
        for p in POOLS:
            prop = unmod * obs[p] / tot_obs if tot_obs > 0 else 0.0
            free = par["physical"][d] - obs[p]
            res = max(0.0, min(prop, free))
            par["reserve"][d][p] = {"obs": obs[p], "prop": prop, "reserve": res,
                                    "capped": res < prop - 1e-9, "free": free,
                                    "unmod_annual": unmod}
            par["land_limit"][d][p] = par["physical"][d] - res
            par["land_limit_uncapped"][d][p] = par["physical"][d] - prop
            par["check"].append({"d": d, "pool": p, "obs": obs[p],
                                 "limit": par["physical"][d] - res,
                                 "limit_uncapped": par["physical"][d] - prop})

    flows = inflow["flow_billion_cubic_metres"].astype(float)
    mean_flow = float(flows.mean())
    lo, hi = 0.85 * mean_flow, 1.08 * mean_flow
    bands = {"dry": flows[flows < lo], "normal": flows[(flows >= lo) & (flows <= hi)],
             "high": flows[flows > hi]}
    ratios = {k: float(v.mean() / mean_flow) for k, v in bands.items()}
    counts = {k: int(len(v)) for k, v in bands.items()}
    windows = flows.rolling(10).mean().dropna()
    wr = windows / mean_flow
    dratio = float(wr.min())
    dprob = float((wr <= dratio + 1e-12).mean())
    raw = {k: counts[k] / len(flows) for k in bands}
    probs = {k: raw[k] * (1.0 - dprob) for k in bands}
    probs["drought"] = dprob
    ratios["drought"] = dratio
    par["inflow"] = {"mean_flow": mean_flow, "ratios": ratios, "counts": counts,
                     "probs": probs,
                     "budgets_bcm": {s: ANCHOR * ratios[s] for s in INF},
                     "n_windows": int(len(windows)),
                     "n_at_below": int((wr <= dratio + 1e-12).sum())}
    tot_phys = sum(par["physical"].values())
    par["budget"] = {(d, s): par["inflow"]["budgets_bcm"][s] * 1e9 * par["physical"][d] / tot_phys
                     for d in D for s in INF}
    par["scenarios"] = [(i, l) for i in INF for l in LAY]
    par["prob"] = {(i, l): probs[i] * LPROB[l] for (i, l) in par["scenarios"]}
    par["cost"] = dict(COST)
    par["water_req"] = dict(WREQ)
    par["ky"] = dict(KY)
    par["flows"] = flows
    return par


def load_plan(path):
    df = pd.read_csv(path)
    plan = {"winter": {}, "summer": {}}
    share = float(df["floor_share"].iloc[0])
    for _, r in df.iterrows():
        if r["kind"] == "winter":
            plan["winter"][(r["district"], r["crop"])] = float(r["area"])
        else:
            plan["summer"][(r["district"], r["crop"], r["inflow"])] = float(r["area"])
    return plan, share


def build(par, floor=0.0, caps=False, fixed=None, budget_scale=1.0,
          budget_total=None, objective="margin", relax=False,
          single=None, penalise=None, bound="pool", min_share=MIN_SHARE,
          min_scenarios=None, land_limit=None):
    """My own formulation. Water in cubic metres. bound chooses the
    binary linkage bound for fixed plans: 'cell' planted area of the
    cell, 'pool' pool land limit, 'physical' district physical area.
    For plans being optimised the bound is the pool land limit."""
    scen = [single] if single else par["scenarios"]
    lim = land_limit or par["land_limit"]
    prob = pulp.LpProblem("audit", pulp.LpMaximize)
    cat = "Continuous" if relax else "Binary"
    xw, xs = {}, {}
    inflows = [single[0]] if single else INF
    for d in D:
        for c in W_CROPS:
            xw[(d, c)] = fixed["winter"][(d, c)] if fixed else pulp.LpVariable(f"xw_{d}_{c}", lowBound=0)
        for c in L_CROPS:
            for i in inflows:
                xs[(d, c, i)] = fixed["summer"][(d, c, i)] if fixed else pulp.LpVariable(f"xs_{d}_{c}_{i}", lowBound=0)
    if not fixed:
        for d in D:
            prob += pulp.lpSum(xw[(d, c)] for c in W_CROPS) <= lim[d]["winter"], f"LandW_{d}"
            for i in inflows:
                prob += pulp.lpSum(xs[(d, c, i)] for c in S_CROPS) <= lim[d]["summer"], f"LandS_{d}_{i}"
                prob += pulp.lpSum(xs[(d, c, i)] for c in N_CROPS) <= lim[d]["nili"], f"LandN_{d}_{i}"
            if caps:
                for c in W_CROPS:
                    prob += xw[(d, c)] <= CAPS[c] * par["physical"][d], f"CapW_{d}_{c}"
                for c in L_CROPS:
                    for i in inflows:
                        prob += xs[(d, c, i)] <= CAPS[c] * par["physical"][d], f"CapS_{d}_{c}_{i}"
    tot_phys = sum(par["physical"].values())
    kept, wat, prod = {}, {}, {}
    staple_expr, margin_terms = {}, []
    if single:
        pcost = pulp.lpSum(par["cost"][c] * xw[(d, c)] for d in D for c in W_CROPS)
        pcost += pulp.lpSum(par["cost"][c] * xs[(d, c, single[0])] for d in D for c in L_CROPS)
    else:
        pcost = pulp.lpSum(par["cost"][c] * xw[(d, c)] for d in D for c in W_CROPS)
        pcost += pulp.lpSum(par["inflow"]["probs"][i] * par["cost"][c] * xs[(d, c, i)]
                            for d in D for c in L_CROPS for i in INF)
    total_prob = sum(par["prob"][s] for s in scen)
    for (i, l) in scen:
        ps = par["prob"][(i, l)] / total_prob
        sk = f"{i}_{l}"
        for d in D:
            if budget_total is not None:
                bd = budget_total * par["physical"][d] / tot_phys
            else:
                bd = par["budget"][(d, i)] * budget_scale
            wvars = []
            for c in A_CROPS:
                x = xw[(d, c)] if c in W_CROPS else xs[(d, c, i)]
                k = pulp.LpVariable(f"k_{d}_{c}_{sk}", lowBound=0, upBound=1, cat=cat)
                a = pulp.LpVariable(f"a_{d}_{c}_{sk}", lowBound=0)
                w = pulp.LpVariable(f"w_{d}_{c}_{sk}", lowBound=0)
                kept[(d, c, (i, l))], wat[(d, c, (i, l))] = a, w
                prob += a <= x, f"KeptLe_{d}_{c}_{sk}"
                if fixed:
                    big = (float(x) if bound == "cell" else
                           lim[d][POOL_OF[c]] if bound == "pool" else par["physical"][d])
                else:
                    big = lim[d][POOL_OF[c]]
                prob += a <= big * k, f"KeptBin_{d}_{c}_{sk}"
                prob += a >= x - big * (1 - k), f"KeptEq_{d}_{c}_{sk}"
                prob += w <= par["water_req"][c] * a, f"Wcap_{d}_{c}_{sk}"
                if min_share:
                    prob += w >= min_share * par["water_req"][c] * a, f"Wmin_{d}_{c}_{sk}"
                y = par["yield"][c][l][d]
                q = y * (1 - par["ky"][c]) * a + (y * par["ky"][c] / par["water_req"][c]) * w
                prod[(d, c, (i, l))] = q
                margin_terms.append(ps * par["price"][c][l] * q)
                wvars.append(w)
            prob += pulp.lpSum(wvars) <= bd, f"Water_{d}_{sk}"
        staple_expr[(i, l)] = pulp.lpSum(prod[(d, c, (i, l))] for d in D for c in STAPLES)
    margin = pulp.lpSum(margin_terms) - pcost
    shortfall = {}
    if objective == "margin":
        obj = margin
        if penalise is not None:
            pen = 0.0
            for s in scen:
                sv = pulp.LpVariable(f"short_{s[0]}_{s[1]}", lowBound=0)
                shortfall[s] = sv
                prob += staple_expr[s] + sv >= floor * par["reference_t"], f"Soft_{s[0]}_{s[1]}"
                pen += (par["prob"][s] / total_prob) * penalise * sv
            obj = margin - pen
        elif floor > 0:
            for s in scen:
                prob += staple_expr[s] >= floor * par["reference_t"], f"Floor_{s[0]}_{s[1]}"
        prob += obj
    elif objective == "maxstaple":
        t = pulp.LpVariable("t_staple", lowBound=0)
        for s in (min_scenarios or scen):
            prob += staple_expr[s] >= t, f"MaxSt_{s[0]}_{s[1]}"
        prob += t
        return prob, {"xw": xw, "xs": xs, "kept": kept, "wat": wat, "prod": prod, "t": t}
    elif objective == "maxstaple_expected":
        prob += pulp.lpSum((par["prob"][s] / total_prob) * staple_expr[s] for s in scen)
    return prob, {"xw": xw, "xs": xs, "kept": kept, "wat": wat, "prod": prod,
                  "shortfall": shortfall, "staple_expr": staple_expr}


def solve(prob, timelimit=900, tol=None):
    opts = []
    if tol is not None:
        opts = [f"primalTolerance {tol}", f"dualTolerance {tol}"]
    prob.solve(pulp.PULP_CBC_CMD(msg=False, timeLimit=timelimit, gapRel=0.0, options=opts))
    return pulp.LpStatus[prob.status]


def plan_of(v):
    return {"winter": {k: float(x.value()) for k, x in v["xw"].items()},
            "summer": {k: float(x.value()) for k, x in v["xs"].items()}}


def scenario_margin_staple(par, v, s, plan):
    rev = sum(par["price"][c][s[1]] * float(pulp.value(v["prod"][(d, c, s)]))
              for d in D for c in A_CROPS)
    cst = sum(par["cost"][c] * plan["winter"][(d, c)] for d in D for c in W_CROPS)
    cst += sum(par["cost"][c] * plan["summer"][(d, c, s[0])] for d in D for c in L_CROPS)
    staple = sum(float(pulp.value(v["prod"][(d, c, s)])) for d in D for c in STAPLES)
    return rev - cst, staple


def evaluate_plan(par, plan, bound="cell"):
    """Margin maximising recourse of a fixed plan, scenario by scenario."""
    out = {}
    for s in par["scenarios"]:
        prob, v = build(par, fixed=plan, single=s, bound=bound)
        st = solve(prob, timelimit=300)
        if st != "Optimal":
            out[s] = {"status": st}
            continue
        m, stap = scenario_margin_staple(par, v, s, plan)
        out[s] = {"status": st, "margin": m, "staple": stap}
    return out


def max_staple_plan(par, plan, bound="cell", budget_total=None, single=None):
    """Staple maximising recourse of a fixed plan, scenario by scenario
    (or one named scenario). Returns dict scenario to max staple."""
    out = {}
    scen = [single] if single else par["scenarios"]
    for s in scen:
        prob, v = build(par, fixed=plan, single=s, bound=bound,
                        objective="maxstaple_expected", budget_total=budget_total)
        st = solve(prob, timelimit=300)
        if st != "Optimal":
            out[s] = None
            continue
        out[s] = sum(float(pulp.value(v["prod"][(d, c, s)])) for d in D for c in STAPLES)
    return out


def modified(par, **kw):
    p = copy.deepcopy(par)
    for k, v in kw.items():
        p[k] = v
    return p
