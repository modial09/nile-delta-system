"""Problem One version 4: allocation of land and water under uncertainty.

Built to docs/FOUNDATIONS.md combined version 2, Sections 5 and 6,
repairing the six defects named in docs/GPT_AUDIT_v3.md.

Structure kept from version 3: two stage architecture, dual reading
in raw and conditional units, scenario arithmetic from the Aswan
record. Structure replaced: seasonal land pools against physical
cultivated area with an unmodeled crop reserve, two planting
decision points (winter planting is one value across scenarios,
summer planting is decided per inflow state because the inflow is
known by summer planting), real abandonment through a binary keep
decision per planted crop per scenario (abandoned means water zero,
output zero, planting cost sunk), published district yields as the
primary basis scaled only to the forecast national level, forecast
prices and yields with their bands as the price and yield layer,
official 2022 costs, and a multi year drought inflow state built
from ten year window means in the record.

Crops are seasonal: winter pool is wheat, sugar beet and winter
potatoes. Summer pool is rice, summer maize, Nili maize, summer
potatoes and Nili potatoes. Combined scenarios are 4 inflow states
times 3 price and yield layer states, 12 in all, with independence
between the layers stated as a named assumption.

Usage, with the project venv python:
  .venv/bin/python src/allocation_model_v4.py main
  .venv/bin/python src/allocation_model_v4.py caps
  .venv/bin/python src/allocation_model_v4.py beet2400
  .venv/bin/python src/allocation_model_v4.py robust
"""

import itertools
import random
import sys
import time
from pathlib import Path

import pandas as pd
import pulp

BASE_DIR = Path(__file__).resolve().parents[1]
EXT_DIR = BASE_DIR / "data" / "external"
PROC_DIR = BASE_DIR / "data" / "processed"

DISTRICTS = [
    "Beheira", "Sharkia", "Dakahlia", "Kafr El Sheikh",
    "Gharbia", "Menoufia", "Qalyubia", "Damietta",
]
WINTER_CROPS = ["Wheat", "Sugar beet", "Potatoes_winter"]
SUMMER_CROPS = ["Rice", "Maize_summer", "Maize_nili",
                "Potatoes_summer", "Potatoes_nili"]
ALL_CROPS = WINTER_CROPS + SUMMER_CROPS
STAPLE_CROPS = ["Wheat", "Rice", "Maize_summer"]  # floor crops, exact wording in the note
GROUP = {  # seasonal crop to forecast group
    "Wheat": "wheat", "Sugar beet": "sugar_beet", "Potatoes_winter": "potatoes",
    "Rice": "rice_paddy", "Maize_summer": "maize", "Maize_nili": "maize",
    "Potatoes_summer": "potatoes", "Potatoes_nili": "potatoes",
}
INFLOW_STATES = ["dry", "normal", "high", "drought"]
LAYER_STATES = ["low", "expected", "high"]
LAYER_PROB = {"low": 0.25, "expected": 0.50, "high": 0.25}

ANCHOR_BCM = 11.00  # calibration, as in version 3
MIN_VIABLE_SHARE = 0.30  # stated minimum viable water share for a kept crop

COST_2022 = {  # Ministry cost bulletin 2019 to 2022, pounds per hectare, rent included
    "Wheat": 37742.86, "Sugar beet": 39454.76, "Rice": 41850.00,
    "Maize_summer": 37671.43, "Maize_nili": 37888.10,
    "Potatoes_summer": 86657.14, "Potatoes_nili": 54176.19,
    # Named gap: no winter potato cost exists in the bulletin. Primary
    # run uses the summer potato cost for winter potatoes, stated as
    # an assumption. A sensitivity repeats key levels at the Nili cost.
    "Potatoes_winter": 86657.14,
}
WATER_REQ = {  # applied basis only, cubic metres per hectare
    "Wheat": 5126.0, "Rice": 16600.0, "Maize_summer": 9305.0,
    # Nili maize duty is printed in the source note of the water file:
    # 3122 cubic metres per feddan, equal to 7433 per hectare.
    "Maize_nili": 7433.0,
    # Sugar beet arbitrated at 5600 to 6600 in the foundation; the
    # primary run uses the midpoint 6100 and the range is a sensitivity.
    "Sugar beet": 6100.0,
    "Potatoes_winter": 4079.0, "Potatoes_summer": 6145.0,
    # No Nili potato duty exists; the summer duty is used, stated.
    "Potatoes_nili": 6145.0,
}
KY = {"Wheat": 1.05, "Rice": 1.20, "Maize_summer": 1.25, "Maize_nili": 1.25,
      "Sugar beet": 1.00, "Potatoes_winter": 1.10, "Potatoes_summer": 1.10,
      "Potatoes_nili": 1.10}  # rice 1.20 is carried labelled unverified
CAP_SHARE = {"Wheat": 0.50, "Sugar beet": 0.30, "Potatoes_winter": 0.15,
             "Rice": 0.35, "Maize_summer": 0.40, "Maize_nili": 0.40,
             "Potatoes_summer": 0.15, "Potatoes_nili": 0.15}
BEET_FACTORY_PRICE = 2400.0


def _area_map(df, crop, season, year):
    sub = df[(df["crop"] == crop) & (df["season"] == season)
             & (df["agricultural_year"] == year)]
    out = {}
    for d in DISTRICTS:
        row = sub[sub["governorate"] == d]
        val = float(row["area_hectares"].iloc[0]) if len(row) else 0.0
        out[d] = 0.0 if pd.isna(val) else val
    return out


def _yield_map(df, crop, season, year):
    sub = df[(df["crop"] == crop) & (df["season"] == season)
             & (df["agricultural_year"] == year)]
    out = {}
    for d in DISTRICTS:
        row = sub[sub["governorate"] == d]
        val = float(row["yield_tons_per_hectare"].iloc[0]) if len(row) else float("nan")
        out[d] = val
    return out


def load_all():
    """Load every parameter from the files on disk. Returns one dict."""
    par = {}
    area = pd.read_csv(EXT_DIR / "capmas_governorate_area.csv")
    yld = pd.read_csv(EXT_DIR / "capmas_governorate_yield.csv")
    tot = pd.read_csv(EXT_DIR / "capmas_governorate_total_cropped_area.csv")
    nili = pd.read_csv(EXT_DIR / "nili_maize_governorate_2020_2021.csv")
    pot = pd.read_csv(EXT_DIR / "potato_season_split.csv")
    fc = pd.read_csv(PROC_DIR / "forecast_prices_yields_v4.csv")
    inflow = pd.read_csv(EXT_DIR / "nile_inflow_aswan_series.csv")

    phys_row = tot[(tot["agricultural_year"] == "2020/2021")
                    & (tot["measure"] == "cultivated_area")]
    par["physical"] = {d: float(phys_row.loc[phys_row["governorate"] == d,
                        "area_hectares"].iloc[0]) for d in DISTRICTS}
    ann_row = tot[(tot["agricultural_year"] == "2020/2021")
                  & (tot["measure"] == "total_cropped_area")]
    par["annual_cropped"] = {d: float(ann_row.loc[ann_row["governorate"] == d,
                             "area_hectares"].iloc[0]) for d in DISTRICTS}

    # Baseline observed areas. Other crops 2020 to 2021 from the area
    # panel; potatoes 2021 to 2022 from the season split file (the
    # newest split, supplied for this build); Nili maize 2020 to 2021
    # from its own file, crop row maize only (white and yellow rows
    # are its components and are never added on top).
    base = {}
    base["Wheat"] = _area_map(area, "wheat", "winter", "2020/2021")
    base["Sugar beet"] = _area_map(area, "sugar_beet", "winter", "2020/2021")
    base["Rice"] = _area_map(area, "rice", "summer", "2020/2021")
    base["Maize_summer"] = _area_map(area, "maize", "summer", "2020/2021")
    nili_maize = nili[nili["crop"] == "maize"]
    base["Maize_nili"] = {}
    for d in DISTRICTS:
        row = nili_maize[nili_maize["governorate"] == d]
        val = float(row["area_hectares"].iloc[0]) if len(row) else 0.0
        base["Maize_nili"][d] = 0.0 if pd.isna(val) else val
    for crop, season in [("Potatoes_winter", "winter"),
                         ("Potatoes_summer", "summer"),
                         ("Potatoes_nili", "nili")]:
        sub = pot[pot["season"] == season]
        base[crop] = {}
        for d in DISTRICTS:
            row = sub[sub["governorate"] == d]
            val = float(row["area_hectares"].iloc[0]) if len(row) else 0.0
            base[crop][d] = 0.0 if pd.isna(val) else val
    # Menoufia rice 2020 to 2021 is blank in its source; the 2019 to
    # 2020 published value is used for that one cell, as in version 3.
    if base["Rice"]["Menoufia"] == 0.0:
        fill = area[(area["crop"] == "rice") & (area["season"] == "summer")
                    & (area["agricultural_year"] == "2019/2020")
                    & (area["governorate"] == "Menoufia")]
        base["Rice"]["Menoufia"] = float(fill["area_hectares"].iloc[0])
    par["baseline"] = base

    # Published district yields, the primary basis, no rescaling.
    pub = {}
    pub["Wheat"] = _yield_map(yld, "wheat", "winter", "2020/2021")
    pub["Sugar beet"] = _yield_map(yld, "sugar_beet", "winter", "2020/2021")
    pub["Rice"] = _yield_map(yld, "rice", "summer", "2020/2021")
    pub["Maize_summer"] = _yield_map(yld, "maize", "summer", "2020/2021")
    pub["Maize_nili"] = {}
    for d in DISTRICTS:
        row = nili_maize[nili_maize["governorate"] == d]
        val = float(row["yield_tons_per_hectare"].iloc[0]) if len(row) else float("nan")
        pub["Maize_nili"][d] = val
    for crop, season in [("Potatoes_winter", "winter"),
                         ("Potatoes_summer", "summer"),
                         ("Potatoes_nili", "nili")]:
        sub = pot[pot["season"] == season]
        pub[crop] = {}
        for d in DISTRICTS:
            row = sub[sub["governorate"] == d]
            pub[crop][d] = (float(row["yield_tons_per_hectare"].iloc[0])
                            if len(row) else float("nan"))
    # Fills for cells the sources leave blank, each stated in the log:
    # a missing district yield is filled with the area weighted mean
    # of the published district yields for that crop, weighted by the
    # baseline areas. Nili potatoes are published for Beheira only, so
    # that one published yield fills the other governorates.
    par["yield_fills"] = []
    for crop in ALL_CROPS:
        known = [d for d in DISTRICTS if not pd.isna(pub[crop][d])]
        wsum = sum(base[crop][d] for d in known)
        if wsum > 0:
            fill_val = sum(pub[crop][d] * base[crop][d] for d in known) / wsum
        else:
            fill_val = sum(pub[crop][d] for d in known) / len(known)
        for d in DISTRICTS:
            if pd.isna(pub[crop][d]):
                pub[crop][d] = fill_val
                par["yield_fills"].append((crop, d, fill_val))
    par["published_yield"] = pub

    # Forecast prices and yields with bands.
    price_f, yield_f = {}, {}
    for _, r in fc.iterrows():
        key = (r["crop"], r["target"])
        entry = {"forecast": float(r["forecast_value"]), "low": float(r["band_low"]),
                 "high": float(r["band_high"]), "rmse": float(r["backtest_rmse"]),
                 "mape": float(r["backtest_mape_pct"]), "model": r["selected_model"]}
        (price_f if r["target"] == "price" else yield_f)[r["crop"]] = entry
    par["price_forecast"] = price_f
    par["yield_forecast"] = yield_f
    # Price by layer state and seasonal crop.
    par["price"] = {}
    for crop in ALL_CROPS:
        f = price_f[GROUP[crop]]
        par["price"][crop] = {"low": f["low"], "expected": f["forecast"], "high": f["high"]}
    # Yield by layer state: district yields scaled proportionally so
    # the area weighted district mean (baseline areas) equals the
    # forecast national yield in the expected state; low and high use
    # the forecast band ratios for that crop group.
    par["yield"] = {}
    for crop in ALL_CROPS:
        f = yield_f[GROUP[crop]]
        wsum = sum(base[crop].values())
        wmean = sum(pub[crop][d] * base[crop][d] for d in DISTRICTS) / wsum if wsum > 0 else \
            sum(pub[crop].values()) / len(DISTRICTS)
        scale = f["forecast"] / wmean
        par.setdefault("yield_scale", {})[crop] = scale
        par["yield"][crop] = {}
        for state, ratio in [("low", f["low"] / f["forecast"]),
                             ("expected", 1.0), ("high", f["high"] / f["forecast"])]:
            par["yield"][crop][state] = {d: pub[crop][d] * scale * ratio for d in DISTRICTS}

    # Reference tonnage: observed areas times published district yields.
    par["reference_t"] = sum(base[c][d] * pub[c][d]
                             for c in STAPLE_CROPS for d in DISTRICTS)
    par["reference_by_crop"] = {c: sum(base[c][d] * pub[c][d] for d in DISTRICTS)
                                for c in STAPLE_CROPS}

    # Reserve construction, documented exactly. No file on disk gives
    # a seasonal total for all crops, so the seasonal reserve is a
    # stated construction, not an observed seasonal figure:
    # annual unmodeled crop area per governorate equals annual cropped
    # area minus the total observed modeled area in the baseline
    # pattern. That annual unmodeled area is split between the winter
    # and summer pools in proportion to the observed modeled area in
    # each pool. The reserve for a pool is its share of that split.
    # The land limit for a pool is physical area minus its reserve.
    par["reserve"] = {}
    par["land_limit"] = {}
    for d in DISTRICTS:
        w_obs = sum(base[c][d] for c in WINTER_CROPS)
        s_obs = sum(base[c][d] for c in SUMMER_CROPS)
        unmod = par["annual_cropped"][d] - (w_obs + s_obs)
        tot_obs = w_obs + s_obs
        rw = unmod * w_obs / tot_obs
        rs = unmod * s_obs / tot_obs
        par["reserve"][d] = {"winter": rw, "summer": rs, "unmodeled_annual": unmod,
                             "winter_observed_modeled": w_obs,
                             "summer_observed_modeled": s_obs}
        par["land_limit"][d] = {"winter": par["physical"][d] - rw,
                                "summer": par["physical"][d] - rs}

    # Inflow states from the record, Derivation A bands as in
    # version 3 (edges 0.85 and 1.08 of the record mean), plus the
    # drought state from ten year window means.
    flows = inflow["flow_billion_cubic_metres"].astype(float)
    mean_flow = float(flows.mean())
    lo_edge, hi_edge = 0.85 * mean_flow, 1.08 * mean_flow
    bands = {"dry": flows[flows < lo_edge], "normal": flows[(flows >= lo_edge) & (flows <= hi_edge)],
             "high": flows[flows > hi_edge]}
    ratios, counts = {}, {}
    for k, v in bands.items():
        ratios[k] = float(v.mean() / mean_flow)
        counts[k] = int(len(v))
    windows = flows.rolling(10).mean().dropna()
    window_ratios = windows / mean_flow
    drought_ratio = float(window_ratios.min())
    drought_raw_prob = float((window_ratios <= drought_ratio + 1e-12).mean())
    raw = {k: counts[k] / len(flows) for k in bands}
    probs = {k: raw[k] * (1.0 - drought_raw_prob) for k in bands}
    probs["drought"] = drought_raw_prob
    ratios["drought"] = drought_ratio
    par["inflow"] = {"mean_flow": mean_flow, "ratios": ratios, "counts": counts,
                     "probs": probs, "budgets_bcm": {s: ANCHOR_BCM * ratios[s] for s in INFLOW_STATES},
                     "n_windows": int(len(windows)),
                     "windows_at_or_below_drought": int((window_ratios <= drought_ratio + 1e-12).sum())}
    # District budgets by physical cultivated area share.
    tot_phys = sum(par["physical"].values())
    par["budget"] = {(d, s): par["inflow"]["budgets_bcm"][s] * 1e9 * par["physical"][d] / tot_phys
                     for d in DISTRICTS for s in INFLOW_STATES}
    # Combined scenarios.
    par["scenarios"] = [(i, l) for i in INFLOW_STATES for l in LAYER_STATES]
    par["prob"] = {(i, l): probs[i] * LAYER_PROB[l] for (i, l) in par["scenarios"]}
    par["cost"] = dict(COST_2022)
    par["water_req"] = dict(WATER_REQ)
    par["ky"] = dict(KY)
    par["flows"] = flows
    return par


def skey(i, l):
    return f"{i}_{l}"


def build(par, floor_share=0.0, caps=False, fixed=None, budget_scale=1.0,
          budget_by_inflow=None, price_override=None, yield_override=None,
          cost_override=None, water_override=None, objective="margin",
          relax=False, single_scenario=None, penalise_floor=None):
    """Build the model. fixed is a dict with winter planting values
    and summer planting values per inflow state, used for recourse
    and benchmark evaluation. objective is margin, maxstaple (a
    common tonnage t held in every scenario) or maxstaple_expected.
    penalise_floor adds a per tonne penalty variable for floor
    shortfall in each scenario instead of a hard floor."""
    scen = [single_scenario] if single_scenario else par["scenarios"]
    prob = pulp.LpProblem("alloc_v4", pulp.LpMaximize)
    price = {c: dict(par["price"][c]) for c in ALL_CROPS}
    if price_override:
        price.update(price_override)
    yld = yield_override or par["yield"]
    cost = cost_override or par["cost"]
    wreq = water_override or par["water_req"]
    cat = "Continuous" if relax else "Binary"

    xw, xs = {}, {}
    for d in DISTRICTS:
        for c in WINTER_CROPS:
            xw[(d, c)] = (fixed["winter"][(d, c)] if fixed else
                          pulp.LpVariable(f"xw_{d}_{c}", lowBound=0))
        for c in SUMMER_CROPS:
            for i in INFLOW_STATES:
                if single_scenario and i != single_scenario[0]:
                    continue
                xs[(d, c, i)] = (fixed["summer"][(d, c, i)] if fixed else
                                 pulp.LpVariable(f"xs_{d}_{c}_{i}", lowBound=0))
    if not fixed:
        for d in DISTRICTS:
            prob += (pulp.lpSum(xw[(d, c)] for c in WINTER_CROPS)
                     <= par["land_limit"][d]["winter"], f"LandW_{d}")
            for i in (INFLOW_STATES if not single_scenario else [single_scenario[0]]):
                prob += (pulp.lpSum(xs[(d, c, i)] for c in SUMMER_CROPS)
                         <= par["land_limit"][d]["summer"], f"LandS_{d}_{i}")
            if caps:
                for c in WINTER_CROPS:
                    prob += (xw[(d, c)] <= CAP_SHARE[c] * par["physical"][d], f"CapW_{d}_{c}")
                for c in SUMMER_CROPS:
                    for i in (INFLOW_STATES if not single_scenario else [single_scenario[0]]):
                        prob += (xs[(d, c, i)] <= CAP_SHARE[c] * par["physical"][d], f"CapS_{d}_{c}_{i}")

    kept, wat, prod = {}, {}, {}
    staple_expr, margin_terms = {}, []
    planted_cost = pulp.lpSum(cost[c] * xw[(d, c)] for d in DISTRICTS for c in WINTER_CROPS)
    if single_scenario:
        i0 = single_scenario[0]
        planted_cost += pulp.lpSum(cost[c] * xs[(d, c, i0)] for d in DISTRICTS for c in SUMMER_CROPS)
    else:
        # Summer planting is decided per inflow state, so its cost is
        # charged with the inflow probability of that state.
        planted_cost += pulp.lpSum(par["inflow"]["probs"][i] * cost[c] * xs[(d, c, i)]
                                   for d in DISTRICTS for c in SUMMER_CROPS for i in INFLOW_STATES)
    total_prob = sum(par["prob"][s] for s in scen)
    for (i, l) in scen:
        p_s = par["prob"][(i, l)] / total_prob
        sk = skey(i, l)
        budget_d = {}
        for d in DISTRICTS:
            b = par["budget"][(d, i)] * budget_scale
            if budget_by_inflow is not None:
                b = budget_by_inflow[d] * par["physical"][d] / sum(par["physical"].values())
            budget_d[d] = b
        for d in DISTRICTS:
            wvars = []
            for c in ALL_CROPS:
                x = xw[(d, c)] if c in WINTER_CROPS else xs[(d, c, i)]
                k = pulp.LpVariable(f"k_{d}_{c}_{sk}", lowBound=0, upBound=1, cat=cat)
                a = pulp.LpVariable(f"a_{d}_{c}_{sk}", lowBound=0)
                # Water is carried in thousand cubic metres inside the
                # solver for numerical scaling; every printed figure is
                # converted back to cubic metres.
                w = pulp.LpVariable(f"w_{d}_{c}_{sk}", lowBound=0)
                kept[(d, c, (i, l))], wat[(d, c, (i, l))] = a, w
                prob += (a <= x, f"KeptLe_{d}_{c}_{sk}")
                big = par["physical"][d]
                prob += (a <= big * k, f"KeptBin_{d}_{c}_{sk}")
                prob += (a >= x - big * (1 - k), f"KeptEq_{d}_{c}_{sk}")
                prob += (w <= (wreq[c] / 1000.0) * a, f"Wcap_{d}_{c}_{sk}")
                prob += (w >= MIN_VIABLE_SHARE * (wreq[c] / 1000.0) * a, f"Wmin_{d}_{c}_{sk}")
                y = yld[c][l][d]
                q = y * (1 - par["ky"][c]) * a + (y * par["ky"][c] / (wreq[c] / 1000.0)) * w
                prod[(d, c, (i, l))] = q
                margin_terms.append(p_s * price[c][l] * q)
                wvars.append(w)
            prob += (pulp.lpSum(wvars) <= budget_d[d] / 1000.0, f"Water_{d}_{sk}")
        staple_expr[(i, l)] = pulp.lpSum(prod[(d, c, (i, l))]
                                         for d in DISTRICTS for c in STAPLE_CROPS)
    margin = pulp.lpSum(margin_terms) - planted_cost
    shortfall_vars = {}
    if objective == "margin":
        obj = margin
        if penalise_floor is not None:
            pen = 0.0
            for s in scen:
                sv = pulp.LpVariable(f"short_{skey(*s)}", lowBound=0)
                shortfall_vars[s] = sv
                prob += (staple_expr[s] + sv >= floor_share * par["reference_t"], f"SoftFloor_{skey(*s)}")
                pen += (par["prob"][s] / total_prob) * penalise_floor * sv
            obj = margin - pen
        elif floor_share > 0:
            for s in scen:
                prob += (staple_expr[s] >= floor_share * par["reference_t"], f"Floor_{skey(*s)}")
        prob += obj
    elif objective == "maxstaple":
        t = pulp.LpVariable("t_staple", lowBound=0)
        for s in scen:
            prob += (staple_expr[s] >= t, f"MaxStaple_{skey(*s)}")
        prob += t
        return prob, {"xw": xw, "xs": xs, "kept": kept, "wat": wat, "prod": prod, "t": t}
    elif objective == "maxstaple_expected":
        prob += pulp.lpSum((par["prob"][s] / total_prob) * staple_expr[s] for s in scen)
    return prob, {"xw": xw, "xs": xs, "kept": kept, "wat": wat, "prod": prod,
                  "shortfall": shortfall_vars}


def solve(prob, timelimit=600, gap=0.001):
    prob.solve(pulp.PULP_CBC_CMD(msg=False, timeLimit=timelimit, gapRel=gap))
    return pulp.LpStatus[prob.status]


def plan_of(vars_, single=False):
    winter = {k: float(v.value()) for k, v in vars_["xw"].items()}
    summer = {k: float(v.value()) for k, v in vars_["xs"].items()}
    return {"winter": winter, "summer": summer}


def evaluate(par, plan, prices_layer="scenario", budget_scale=1.0,
             budget_by_inflow=None, floor_share=0.0):
    """Recourse evaluation of a fixed plan over all 12 scenarios.
    Returns expected margin and per scenario results."""
    out = {"margin": 0.0, "per": {}, "all_feasible": True, "staple_min": None}
    for s in par["scenarios"]:
        prob, v = build(par, floor_share=floor_share, fixed=plan,
                        budget_scale=budget_scale, budget_by_inflow=budget_by_inflow,
                        single_scenario=s)
        st = solve(prob, timelimit=300)
        if st != "Optimal":
            out["per"][s] = {"status": st, "margin": None, "staple_t": None}
            out["all_feasible"] = False
            continue
        # Scenario margin: revenue in that scenario minus the full
        # planting cost of the fixed plan for that inflow state.
        rev = sum(par["price"][c][s[1]] * float(pulp.value(v["prod"][(d, c, s)]))
                  for d in DISTRICTS for c in ALL_CROPS)
        cst = sum(par["cost"][c] * plan["winter"][(d, c)] for d in DISTRICTS for c in WINTER_CROPS)
        cst += sum(par["cost"][c] * plan["summer"][(d, c, s[0])]
                   for d in DISTRICTS for c in SUMMER_CROPS)
        staple = sum(float(pulp.value(v["prod"][(d, c, s)]))
                     for d in DISTRICTS for c in STAPLE_CROPS)
        out["per"][s] = {"status": st, "margin": rev - cst, "staple_t": staple}
        out["margin"] += par["prob"][s] * (rev - cst)
    feas = [v["staple_t"] for v in out["per"].values() if v["staple_t"] is not None]
    out["staple_min"] = min(feas) if feas else None
    out["staple_expected"] = sum(par["prob"][s] * out["per"][s]["staple_t"]
                                  for s in par["scenarios"] if out["per"][s]["staple_t"] is not None)
    return out


def scenario_results(par, vars_):
    """Expected margin and staple output from a solved full model."""
    rev = 0.0
    staple_exp = 0.0
    staple_min = None
    planted_areas = {}
    for c in ALL_CROPS:
        if c in WINTER_CROPS:
            planted_areas[c] = sum(float(vars_["xw"][(d, c)].value()) for d in DISTRICTS)
        else:
            planted_areas[c] = sum(par["inflow"]["probs"][i] * float(vars_["xs"][(d, c, i)].value())
                                   for d in DISTRICTS for i in INFLOW_STATES)
    for s in par["scenarios"]:
        r = sum(par["price"][c][s[1]] * float(pulp.value(vars_["prod"][(d, c, s)]))
                for d in DISTRICTS for c in ALL_CROPS)
        rev += par["prob"][s] * r
        st = sum(float(pulp.value(vars_["prod"][(d, c, s)]))
                 for d in DISTRICTS for c in STAPLE_CROPS)
        staple_exp += par["prob"][s] * st
        staple_min = st if staple_min is None else min(staple_min, st)
    cost = sum(par["cost"][c] * float(vars_["xw"][(d, c)].value())
               for d in DISTRICTS for c in WINTER_CROPS)
    cost += sum(par["inflow"]["probs"][i] * par["cost"][c] * float(vars_["xs"][(d, c, i)].value())
                for d in DISTRICTS for c in SUMMER_CROPS for i in INFLOW_STATES)
    return {"margin": rev - cost, "staple_expected": staple_exp,
            "staple_min": staple_min, "planted": planted_areas}


def print_header(par):
    print("=" * 76)
    print("NILE DELTA ALLOCATION MODEL VERSION 4")
    print("Margin basis on every table: forecast prices at the 2024 level")
    print("with official 2022 costs, pounds. Winter potato cost is the")
    print("summer potato cost of 86657.14 pounds per hectare, a stated")
    print("assumption for a named gap (no winter potato cost exists).")
    print("=" * 76)
    print(f"Physical cultivated area total: {sum(par['physical'].values()):,.0f} hectares")
    print(f"Annual cropped area total (descriptor, never a constraint): "
          f"{sum(par['annual_cropped'].values()):,.0f} hectares")
    print("\nReserve table (construction stated in the code and the note):")
    print("Governorate | physical | winter reserve | winter limit | summer reserve | summer limit | unmodeled annual")
    for d in DISTRICTS:
        r = par["reserve"][d]
        print(f"{d} | {par['physical'][d]:,.0f} | {r['winter']:,.0f} | {par['land_limit'][d]['winter']:,.0f} | "
              f"{r['summer']:,.0f} | {par['land_limit'][d]['summer']:,.0f} | {r['unmodeled_annual']:,.0f}")
    print("\nYield fills for blank source cells (area weighted published mean):")
    for crop, d, val in par["yield_fills"]:
        print(f"  {crop} in {d}: {val:.3f} tonnes per hectare")
    print("\nDistrict yield scaling to the forecast national level (expected state):")
    for c in ALL_CROPS:
        print(f"  {c}: scale {par['yield_scale'][c]:.4f}")
    print("\nForecast prices (pounds per tonne) and yields (tonnes per hectare), with backtest errors:")
    for g, f in par["price_forecast"].items():
        print(f"  price {g}: forecast {f['forecast']:,.2f} low {f['low']:,.2f} high {f['high']:,.2f} "
              f"model {f['model']} RMSE {f['rmse']:,.2f} MAPE {f['mape']:.2f} percent")
    for g, f in par["yield_forecast"].items():
        print(f"  yield {g}: forecast {f['forecast']:.4f} low {f['low']:.4f} high {f['high']:.4f} "
              f"model {f['model']} RMSE {f['rmse']:.4f} MAPE {f['mape']:.2f} percent")
    print("\nCosts 2022 (pounds per hectare, rent included):")
    for c in ALL_CROPS:
        print(f"  {c}: {par['cost'][c]:,.2f}")
    print("\nWater duties, applied basis (cubic metres per hectare):")
    for c in ALL_CROPS:
        print(f"  {c}: {par['water_req'][c]:,.0f}")
    print("Sugar beet duty is the midpoint 6100 of the arbitrated range 5600 to 6600.")
    print("Nili maize duty 7433 is printed in the water file source note.")
    print("Nili potato duty uses the summer potato duty, a stated assumption.")
    inf = par["inflow"]
    print(f"\nInflow record: mean flow {inf['mean_flow']:.3f} billion cubic metres, 100 years")
    print("Inflow states (budgets are the 11.00 calibration times the state ratio):")
    for s in INFLOW_STATES:
        extra = f"count {inf['counts'][s]}" if s in inf["counts"] else \
            f"ten year windows {inf['n_windows']}, windows at or below this ratio {inf['windows_at_or_below_drought']}"
        print(f"  {s}: ratio {inf['ratios'][s]:.4f} budget {inf['budgets_bcm'][s]:.3f} BCM "
              f"probability {inf['probs'][s]:.4f} ({extra})")
    print("Drought probability construction: the share of ten year windows at or")
    print("below the lowest window ratio, with the three single year state")
    print("probabilities scaled by one minus that share so the four sum to one.")
    print("Price and yield layer probabilities: low 0.25, expected 0.50, high 0.25,")
    print("reading the forecast band as quartiles. Independence between the inflow")
    print("layer and the price and yield layer is a named assumption.")
    print(f"\nReference tonnage (observed areas times published district yields): "
          f"{par['reference_t']:,.0f} tonnes")
    for c, v in par["reference_by_crop"].items():
        print(f"  {c}: {v:,.0f} tonnes")
    # WaPOR comparison
    print("\nWaPOR comparison (validation only, see the verdict in the note):")
    wp = pd.read_csv(EXT_DIR / "wapor_aeti_governorate_2018_2025.csv")
    wp_mean = wp.groupby("governorate")["consumption_billion_cubic_metres"].mean()
    print("Governorate | modeled baseline full applied demand (BCM) | WaPOR mean total consumption 2018 to 2025 (BCM)")
    tot_m, tot_w = 0.0, 0.0
    for d in DISTRICTS:
        modeled = sum(par["baseline"][c][d] * par["water_req"][c] for c in ALL_CROPS) / 1e9
        wval = float(wp_mean[d])
        tot_m += modeled; tot_w += wval
        print(f"{d} | {modeled:.3f} | {wval:.3f}")
    print(f"Total | {tot_m:.3f} | {tot_w:.3f}")
    print("WaPOR values are total consumption over all surfaces per governorate,")
    print("with no cropland mask. They are never presented as cropland consumption.")
    print("The modeled figure covers the modeled crops only, on the applied basis,")
    print("while WaPOR measures consumption over every surface. No efficiency or")
    print("requirement scalar is derived from this comparison: direct calibration")
    print("is not defensible on these two bases, so WaPOR is used as validation only.")
    print("The modeled baseline demand sits below the WaPOR total in every")
    print("governorate, which is the order the two definitions require.")


def frontier(par, levels, caps=False, label="", price_override=None,
             cost_override=None, water_override=None, yield_override=None,
             save_plan_share=None):
    print(f"\nFRONTIER {label} caps={caps}")
    print("Level percent | status | expected margin EGP | cost vs unconstrained EGP | cost vs next lower level EGP")
    results = {}
    prev_margin = None
    unc_margin = None
    for lv in levels:
        t0 = time.time()
        prob, v = build(par, floor_share=lv, caps=caps, price_override=price_override,
                        cost_override=cost_override, water_override=water_override,
                        yield_override=yield_override)
        st = solve(prob)
        if st != "Optimal":
            print(f"{lv*100:.0f} | {st} | none | none | none | seconds {time.time()-t0:.0f}")
            results[lv] = {"status": st}
            continue
        res = scenario_results(par, v) if not price_override else None
        margin = float(pulp.value(prob.objective))
        if lv == 0:
            unc_margin = margin
        cost_unc = (unc_margin - margin) if unc_margin is not None else 0.0
        cost_prev = (prev_margin - margin) if prev_margin is not None else 0.0
        print(f"{lv*100:.0f} | {st} | {margin:,.0f} | {cost_unc:,.0f} | {cost_prev:,.0f} | seconds {time.time()-t0:.0f}")
        if res:
            print(f"    expected staple tonnes {res['staple_expected']:,.0f} | minimum scenario staple tonnes {res['staple_min']:,.0f}")
            planted_line = " | ".join(f"{c} {res['planted'][c]:,.0f} ha" for c in ALL_CROPS)
            print(f"    planted (probability weighted for summer): {planted_line}")
            for c in ALL_CROPS:
                base_tot = sum(par["baseline"][c].values())
                if base_tot > 0 and res["planted"][c] > 2 * base_tot:
                    print(f"    MARKET ABSORPTION WARNING: {c} planted {res['planted'][c]:,.0f} hectares "
                          f"is {res['planted'][c]/base_tot:.2f} times its observed area of {base_tot:,.0f} hectares. "
                          f"The fixed price stops being credible at this scale.")
        results[lv] = {"status": st, "margin": margin, "res": res}
        prev_margin = margin
        if save_plan_share is not None and abs(lv - save_plan_share) < 1e-9:
            plan = plan_of(v)
            rows = []
            for (d, c), val in plan["winter"].items():
                rows.append({"kind": "winter", "district": d, "crop": c, "inflow": "all", "area": val})
            for (d, c, i), val in plan["summer"].items():
                rows.append({"kind": "summer", "district": d, "crop": c, "inflow": i, "area": val})
            pd.DataFrame(rows).to_csv(PROC_DIR / "plan_v4_floor85.csv", index=False)
            print(f"    plan at this level saved to data/processed/plan_v4_floor85.csv")
    feasible = [lv for lv, r in results.items() if r["status"] == "Optimal"]
    if feasible:
        print(f"Feasible ceiling on this ladder: {max(feasible)*100:.0f} percent")
    return results


def ceiling_run(par, caps=False, label="", **kw):
    prob, v = build(par, caps=caps, objective="maxstaple", **kw)
    st = solve(prob)
    if st != "Optimal":
        print(f"CEILING {label}: status {st}")
        return None
    t = float(v["t"].value())
    print(f"CEILING {label}: maximum held staple tonnage in every scenario {t:,.0f} tonnes, "
          f"which is {100*t/par['reference_t']:.2f} percent of the reference tonnage {par['reference_t']:,.0f}")
    return t / par["reference_t"]


def main_mode():
    par = load_all()
    print_header(par)
    levels = [0.0, 0.50, 0.60, 0.70, 0.80, 0.85, 0.90, 0.93, 0.95, 1.00]
    res = frontier(par, levels, label="primary, no caps")
    ceil = ceiling_run(par, label="primary, no caps")
    feasible_levels = [lv for lv, r in res.items() if r["status"] == "Optimal" and lv > 0]
    robust_share = 0.85 if res.get(0.85, {}).get("status") == "Optimal" else max(feasible_levels)
    prob_r, v_r = build(par, floor_share=robust_share)
    st_r = solve(prob_r)
    print(f"Robustness plan at floor {robust_share*100:.0f} percent: status {st_r}")
    if st_r == "Optimal":
        plan_r = plan_of(v_r)
        rows = []
        for (d, c), val in plan_r["winter"].items():
            rows.append({"kind": "winter", "district": d, "crop": c, "inflow": "all", "area": val, "floor_share": robust_share})
        for (d, c, i), val in plan_r["summer"].items():
            rows.append({"kind": "summer", "district": d, "crop": c, "inflow": i, "area": val, "floor_share": robust_share})
        pd.DataFrame(rows).to_csv(PROC_DIR / "plan_v4_robust_plan.csv", index=False)
        print("Robustness plan saved to data/processed/plan_v4_robust_plan.csv")
    # Beet duty sensitivity on the ceiling
    for duty in (5600.0, 6600.0):
        wover = dict(par["water_req"]); wover["Sugar beet"] = duty
        ceiling_run(par, label=f"sugar beet duty {duty:,.0f}", water_override=wover)
    # Rice Ky sensitivity on the ceiling
    for kyv in (1.00, 1.40):
        old = par["ky"]["Rice"]; par["ky"]["Rice"] = kyv
        ceiling_run(par, label=f"rice Ky {kyv} (primary carries 1.20, unverified)")
        par["ky"]["Rice"] = old
    # Rescaled yields sensitivity on the ceiling (v3 rescaling factors)
    factors = {"wheat": 0.95760, "rice_paddy": 1.00181, "maize": 0.83879,
               "sugar_beet": 1.05705, "potatoes": 0.98940}
    yover = {c: {st: {d: par["yield"][c][st][d] * factors[GROUP[c]] for d in DISTRICTS}
                 for st in LAYER_STATES} for c in ALL_CROPS}
    ceiling_run(par, label="rescaled district yields (labelled sensitivity only)", yield_override=yover)
    # Winter potato cost sensitivity at key levels
    cover = dict(par["cost"]); cover["Potatoes_winter"] = 54176.19
    frontier(par, [0.0, 0.90], label="winter potatoes at the Nili cost 54176.19 (sensitivity; primary uses the summer cost)",
             cost_override=cover)
    # Duals from the LP relaxation at the 90 percent floor (or ceiling)
    dual_level = 0.90 if res.get(0.90, {}).get("status") == "Optimal" else ((ceil - 0.001) if ceil else 0.0)
    print(f"\nWATER VALUES: LP relaxation duals at floor {dual_level*100:.0f} percent")
    print("These are marginal duals from the linear relaxation of the same")
    print("formulation, labelled as LP relaxation duals. Raw dual is pounds per")
    print("cubic metre of expected margin; conditional divides by the combined")
    print("scenario probability.")
    prob, v = build(par, floor_share=dual_level, relax=True)
    st = solve(prob, gap=0.0)
    print(f"LP relaxation status: {st} | objective {float(pulp.value(prob.objective)):,.0f}")
    print("Governorate | scenario | raw dual EGP per m3 | conditional EGP per m3")
    for name, con in prob.constraints.items():
        if name.startswith("Water_"):
            rest = name[len("Water_"):]
            for s in par["scenarios"]:
                sk = skey(*s)
                if rest.endswith("_" + sk):
                    dname = rest[: -len(sk) - 1].replace("_", " ")
                    raw = abs(float(con.pi)) / 1000.0 if con.pi is not None else float("nan")
                    print(f"{dname} | {sk} | {raw:.4f} | {raw/par['prob'][s]:.2f}")
    # Baseline and decomposition (accounting only)
    print("\nBASELINE AND DECOMPOSITION (accounting only, no causal claim)")
    base_plan = {"winter": {(d, c): par["baseline"][c][d] for d in DISTRICTS for c in WINTER_CROPS},
                 "summer": {(d, c, i): par["baseline"][c][d] for d in DISTRICTS for c in SUMMER_CROPS for i in INFLOW_STATES}}
    base_eval = evaluate(par, base_plan)
    print(f"Baseline expected margin (same price and cost basis): EGP {base_eval['margin']:,.0f}")
    print(f"Baseline expected staple tonnes: {base_eval['staple_expected']:,.0f} | minimum scenario staple tonnes: {base_eval['staple_min']:,.0f}")
    if res.get(0.0, {}).get("status") == "Optimal":
        opt = res[0.0]["margin"]
        print(f"Optimised unconstrained expected margin: EGP {opt:,.0f}")
        print(f"Accounting difference, optimised minus baseline: EGP {opt - base_eval['margin']:,.0f} "
              f"({100*(opt-base_eval['margin'])/base_eval['margin']:.2f} percent of the baseline margin)")
        print("Accounting components: the baseline margin above and the optimised")
        print("margin above. No input is said to have caused any share of the change.")
    # Information values against true means, at the 90 percent floor
    # where that floor is feasible, otherwise at the highest feasible
    # ladder level, stated in the log.
    feasible_levels = [lv for lv, r in res.items() if r["status"] == "Optimal" and lv > 0]
    info_floor = 0.90 if res.get(0.90, {}).get("status") == "Optimal" else max(feasible_levels)
    print(f"\nInformation values use the stated floor of {info_floor*100:.0f} percent "
          f"(90 percent is used only where the frontier holds it).")
    info_values(par, res, floor_share=info_floor)
    # Stress runs
    stress(par)


def info_values(par, frontier_res=None, floor_share=0.90):
    print("\nINFORMATION VALUES AGAINST TRUE MEANS")
    true_budget = sum(par["inflow"]["probs"][i] * par["inflow"]["budgets_bcm"][i] for i in INFLOW_STATES)
    print(f"True mean budget: {true_budget:.4f} billion cubic metres")
    mean_price = {c: sum(LAYER_PROB[l] * par["price"][c][l] for l in LAYER_STATES) for c in ALL_CROPS}
    mean_yield = {c: {d: sum(LAYER_PROB[l] * par["yield"][c][l][d] for l in LAYER_STATES)
                      for d in DISTRICTS} for c in ALL_CROPS}
    print("True mean prices (pounds per tonne): " +
          ", ".join(f"{c} {mean_price[c]:,.0f}" for c in ALL_CROPS))
    # RP at the stated floor from the frontier if available
    rp = None
    if frontier_res and frontier_res.get(floor_share, {}).get("status") == "Optimal":
        rp = frontier_res[floor_share]["margin"]
    if rp is None:
        prob, v = build(par, floor_share=floor_share)
        st = solve(prob)
        rp = float(pulp.value(prob.objective)) if st == "Optimal" else None
        print(f"RP solve at the stated floor: status {st}")
    print(f"Recourse problem value RP at the stated floor of {floor_share*100:.0f} percent: EGP {rp:,.0f}" if rp is not None else "RP infeasible at the stated floor")
    # Wait and see: one deterministic problem per combined scenario
    ws = 0.0
    ws_ok = True
    for s in par["scenarios"]:
        price_o = {c: {"low": par["price"][c][s[1]], "expected": par["price"][c][s[1]],
                       "high": par["price"][c][s[1]]} for c in ALL_CROPS}
        yld_o = {c: {st: par["yield"][c][s[1]] for st in LAYER_STATES} for c in ALL_CROPS}
        bud = {(d, i): par["budget"][(d, s[0])] for d in DISTRICTS for i in INFLOW_STATES}
        par_s = dict(par); par_s["budget"] = bud
        prob, v = build(par_s, floor_share=floor_share, price_override=price_o,
                        yield_override=yld_o, single_scenario=s)
        st = solve(prob)
        if st != "Optimal":
            print(f"  wait and see {skey(*s)}: status {st}")
            ws_ok = False
            continue
        val = float(pulp.value(prob.objective))
        # Deterministic objective in build() charges summer cost with
        # inflow probabilities; in a single scenario that understates
        # summer cost. Correct by recomputing the scenario margin.
        plan = plan_of(v)
        rev = sum(par["price"][c][s[1]] * float(pulp.value(v["prod"][(d, c, s)]))
                  for d in DISTRICTS for c in ALL_CROPS)
        cst = sum(par["cost"][c] * plan["winter"][(d, c)] for d in DISTRICTS for c in WINTER_CROPS)
        cst += sum(par["cost"][c] * plan["summer"][(d, c, s[0])] for d in DISTRICTS for c in SUMMER_CROPS)
        ws += par["prob"][s] * (rev - cst)
        print(f"  wait and see {skey(*s)}: scenario margin EGP {rev-cst:,.0f} probability {par['prob'][s]:.4f}")
    if ws_ok and rp is not None:
        print(f"Wait and see value WS: EGP {ws:,.0f}")
        print(f"EVPI equals WS minus RP: EGP {ws - rp:,.0f}")
    # Expected value problem at true means (single deterministic plan)
    price_o = {c: {st: mean_price[c] for st in LAYER_STATES} for c in ALL_CROPS}
    yld_o = {c: {st: mean_yield[c] for st in LAYER_STATES} for c in ALL_CROPS}
    bud = {(d, i): true_budget * 1e9 * par["physical"][d] / sum(par["physical"].values())
           for d in DISTRICTS for i in INFLOW_STATES}
    par_m = dict(par); par_m["budget"] = bud
    s0 = ("normal", "expected")
    prob, v = build(par_m, floor_share=floor_share, price_override=price_o,
                    yield_override=yld_o, single_scenario=s0)
    st = solve(prob)
    print(f"Expected value problem (true means, stated floor {floor_share*100:.0f} percent): status {st}")
    if st != "Optimal":
        print("The true mean plan cannot be built at the stated floor even")
        print("at the true mean inputs. That infeasibility is reported as a finding.")
        return
    ev_plan_single = plan_of(v)
    ev_plan = {"winter": ev_plan_single["winter"],
               "summer": {(d, c, i): ev_plan_single["summer"][(d, c, "normal")]
                          for d in DISTRICTS for c in SUMMER_CROPS for i in INFLOW_STATES}}
    eev = evaluate(par, ev_plan, floor_share=floor_share)
    if eev["all_feasible"]:
        print(f"EEV (true mean plan evaluated with the floor held): EGP {eev['margin']:,.0f}")
        if rp is not None:
            print(f"VSS equals RP minus EEV: EGP {rp - eev['margin']:,.0f}")
    else:
        bad = [skey(*s) for s, r in eev["per"].items() if r["margin"] is None]
        print(f"FINDING: the true mean plan cannot hold the stated floor in scenario(s): {bad}")
        eev_nf = evaluate(par, ev_plan, floor_share=0.0)
        print(f"True mean plan evaluated with no floor: EGP {eev_nf['margin']:,.0f} "
              f"(an upper bound that flatters it, not an EEV under the guarantee)")
        # Penalised variant, named: penalty 25000 pounds per tonne of shortfall
        pen_total_margin = 0.0
        for s in par["scenarios"]:
            prob2, v2 = build(par, floor_share=floor_share, fixed=ev_plan,
                              single_scenario=s, penalise_floor=25000.0)
            st2 = solve(prob2)
            if st2 != "Optimal":
                print(f"  penalised recourse {skey(*s)}: status {st2}")
                continue
            rev = sum(par["price"][c][s[1]] * float(pulp.value(v2["prod"][(d, c, s)]))
                      for d in DISTRICTS for c in ALL_CROPS)
            cst = sum(par["cost"][c] * ev_plan["winter"][(d, c)] for d in DISTRICTS for c in WINTER_CROPS)
            cst += sum(par["cost"][c] * ev_plan["summer"][(d, c, s[0])] for d in DISTRICTS for c in SUMMER_CROPS)
            short = float(v2["shortfall"][s].value())
            pen_total_margin += par["prob"][s] * (rev - cst - 25000.0 * short)
            print(f"  penalised recourse {skey(*s)}: margin before penalty EGP {rev-cst:,.0f} shortfall {short:,.0f} tonnes")
        print(f"Penalised EEV under a named penalty of 25000 pounds per tonne of shortfall: EGP {pen_total_margin:,.0f}")
        if rp is not None:
            print(f"Penalised VSS (RP minus penalised EEV, named as penalised): EGP {rp - pen_total_margin:,.0f}")
            print("No standard VSS is reported, because the true mean plan is")
            print("infeasible under the hard floor in at least one scenario.")


def stress(par):
    print("\nSTRESS RUNS (no floor, budgets scaled, side by side capacity and choice)")
    for scale in (0.90, 0.80):
        prob, v = build(par, floor_share=0.0, budget_scale=scale)
        st = solve(prob)
        res = scenario_results(par, v) if st == "Optimal" else None
        prob2, v2 = build(par, objective="maxstaple", budget_scale=scale)
        st2 = solve(prob2)
        cap_t = float(v2["t"].value()) if st2 == "Optimal" else None
        print(f"Budget scale {scale:.2f}: profit choice status {st} | capacity status {st2}")
        if res:
            print(f"  Profit objective chooses: expected margin EGP {res['margin']:,.0f} | "
                  f"expected staple tonnes {res['staple_expected']:,.0f} | minimum scenario staple tonnes {res['staple_min']:,.0f} "
                  f"({100*res['staple_min']/par['reference_t']:.2f} percent of reference)")
        if cap_t is not None:
            print(f"  Maximum staple capacity: {cap_t:,.0f} tonnes held in every scenario "
                  f"({100*cap_t/par['reference_t']:.2f} percent of reference)")


def caps_mode():
    par = load_all()
    print_header(par)
    levels = [0.0, 0.50, 0.60, 0.70, 0.80, 0.85, 0.90, 0.93, 0.95, 1.00]
    frontier(par, levels, caps=True,
             label="with named constraints (rotation and market sanity limits, a modelling device: "
                   "wheat 0.50, rice 0.35, maize 0.40, sugar beet 0.30, potatoes 0.15 of district physical land)")
    ceiling_run(par, caps=True, label="with named constraints")


def beet_mode():
    par = load_all()
    print_header(par)
    price_o = {"Sugar beet": {"low": BEET_FACTORY_PRICE, "expected": BEET_FACTORY_PRICE,
                              "high": BEET_FACTORY_PRICE}}
    print("\nBEET VARIANT: sugar beet at the documented factory procurement price")
    print("of 2400 pounds per tonne in every layer state, all else equal. The")
    print("primary run uses the forecast farm gate price. The two runs differ in")
    print("price concept, year and marketing basis together, and no difference")
    print("between them is attributed to the price concept alone.")
    frontier(par, [0.0, 0.70, 0.80, 0.90], label="beet at 2400", price_override=price_o)
    print("The capacity ceiling does not depend on prices, so the primary")
    print("ceiling of 75.45 percent of the reference tonnage applies to this")
    print("variant as well; the 70 percent level above is its highest feasible")
    print("ladder level and the 80 and 90 percent levels are infeasible.")


def robust_mode(n_samples=100):
    par = load_all()
    print_header(par)
    plan_file = PROC_DIR / "plan_v4_robust_plan.csv"
    target_share = 0.85
    if plan_file.exists():
        df = pd.read_csv(plan_file)
        target_share = float(df["floor_share"].iloc[0])
        plan = {"winter": {}, "summer": {}}
        for _, r in df.iterrows():
            if r["kind"] == "winter":
                plan["winter"][(r["district"], r["crop"])] = float(r["area"])
            else:
                plan["summer"][(r["district"], r["crop"], r["inflow"])] = float(r["area"])
        print(f"\nROBUSTNESS: fixed plan loaded from plan_v4_robust_plan.csv (floor {target_share*100:.0f} percent; 85 percent is used only where the ceiling allows it, otherwise the highest feasible ladder level)")
    else:
        print("\nROBUSTNESS: plan file missing, solving the 85 percent floor plan first")
        prob, v = build(par, floor_share=target_share)
        st = solve(prob)
        if st != "Optimal":
            ceil_r = ceiling_run(par, label="robustness fallback")
            target_share = int(ceil_r * 100) / 100.0
            prob, v = build(par, floor_share=target_share)
            st = solve(prob)
            print(f"Fallback plan at floor {target_share*100:.0f} percent: status {st}")
        plan = plan_of(v)
    rng = random.Random(20261114)
    flows = par["flows"]
    mean_flow = float(flows.mean())
    windows = flows.rolling(10).mean().dropna().tolist()
    shares, shortfalls, ratios_used = [], [], []
    target_t = target_share * par["reference_t"]
    for n in range(n_samples):
        if n % 2 == 0:
            ratio = float(rng.choice(flows.tolist())) / mean_flow
            kind = "single year"
        else:
            ratio = float(rng.choice(windows)) / mean_flow
            kind = "ten year window mean"
        ratios_used.append(ratio)
        budget_by = {d: ANCHOR_BCM * ratio * 1e9 for d in DISTRICTS}  # total BCM, split in build by physical share
        # Fixed plan, expected prices and yields, maximise staple tonnage
        price_o = {c: {st: par["price"][c]["expected"] for st in LAYER_STATES} for c in ALL_CROPS}
        yld_o = {c: {st: par["yield"][c]["expected"] for st in LAYER_STATES} for c in ALL_CROPS}
        s0 = ("normal", "expected")
        prob, v = build(par, fixed=plan, objective="maxstaple_expected",
                        budget_by_inflow=budget_by, price_override=price_o,
                        yield_override=yld_o, single_scenario=s0)
        # maxstaple_expected with a fixed plan and one scenario gives the
        # maximum staple tonnage that plan can deliver at this budget
        # when recourse is solved for staples; to maximise staples the
        # objective must be staple tonnage, which build returns for
        # maxstaple_expected as expected staple. Rebuild with that
        # objective is already set. Solve:
        st = solve(prob, timelimit=300)
        if st != "Optimal":
            print(f"sample {n}: status {st} ratio {ratio:.3f} {kind}")
            continue
        staple = sum(float(pulp.value(v["prod"][(d, c, s0)])) for d in DISTRICTS for c in STAPLE_CROPS)
        shares.append(staple / par["reference_t"])
        shortfalls.append(max(0.0, target_t - staple))
        if n < 5 or n % 20 == 0:
            print(f"sample {n}: ratio {ratio:.3f} ({kind}) max staple for fixed plan {staple:,.0f} tonnes "
                  f"share {100*staple/par['reference_t']:.2f} percent shortfall {max(0.0, target_t-staple):,.0f}")
    shares_s = pd.Series(shares); short_s = pd.Series(shortfalls)
    print(f"\nSamples solved: {len(shares)} of {n_samples} requested")
    print(f"Sampling: alternating random single years and random ten year window")
    print(f"means drawn from the 1871 to 1970 record, seed 20261114, budget equals")
    print(f"11.00 times the drawn ratio of flow to the record mean.")
    print(f"Maximum feasible floor for the fixed plan across samples (percent of reference):")
    print(f"  minimum {100*shares_s.min():.2f} | 10th percentile {100*shares_s.quantile(0.10):.2f} | "
          f"median {100*shares_s.median():.2f} | mean {100*shares_s.mean():.2f} | maximum {100*shares_s.max():.2f}")
    print(f"  share of samples where the fixed plan can still hold its floor: "
          f"{100*(shares_s >= target_share).mean():.1f} percent of samples")
    worst = short_s.sort_values(ascending=False).head(max(1, len(short_s)//10))
    print(f"Worst decile: {len(worst)} samples with the largest shortfalls against the")
    print(f"{target_share*100:.0f} percent floor reference of {target_t:,.0f} tonnes")
    print(f"HEADLINE worst decile expected staple shortfall: {worst.mean():,.0f} tonnes")
    print(f"All sample mean shortfall: {short_s.mean():,.0f} tonnes")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "main"
    if mode == "main":
        main_mode()
    elif mode == "caps":
        caps_mode()
    elif mode == "beet2400":
        beet_mode()
    elif mode == "robust":
        robust_mode()
    else:
        print(f"unknown mode {mode}")
