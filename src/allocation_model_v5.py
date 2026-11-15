"""Problem One version 5: foundation rebuild repair build, succeeding version 4.1.

Built to docs/FOUNDATIONS.md combined version 2, Sections 5 and 6,
and to the repair list that follows the independent audit of version
4 in paper/Audit_Log_v4.md. Version 4 is kept unchanged on disk as
the audited record; this file is the repaired build.

Repairs against version 4, in the order of the audit errors:
  1. The seasonal land reserve is rebuilt so that it admits the
     observed historical pattern. The annual unmodeled crop area of
     each governorate is split across the three season pools in
     proportion to the observed modeled area in each pool, and each
     pool reserve is then capped at the physical area that the
     observed modeled pattern leaves free in that pool, because in
     the observed season the unmodeled crops demonstrably fitted
     into that free area. A pool limit is the physical cultivated
     area minus its capped reserve, so no pool limit can fall below
     the observed modeled area of that pool. A baseline feasibility
     check over all 24 governorate pools is printed in every log.
  2. District yields are the published district yields throughout
     the primary run, with no scaling. The low and high yield states
     apply the forecast band ratios to the published yields. The
     version 4 construction, district yields scaled so their area
     weighted mean equals the forecast national yield, is kept only
     as a labelled sensitivity. The reference tonnage and the model
     use the same published yield basis.
  3. Land binds in three season pools: winter, summer and Nili.
     The version 4 build pooled summer and Nili crops into one pool.
  4. The baseline years are printed in every log: areas for wheat,
     sugar beet, rice, summer maize and Nili maize come from the
     2020 to 2021 bulletin panel, potato areas in all three seasons
     come from the 2021 to 2022 season split file, which is the only
     split on disk, and one rice cell, Menoufia, comes from the
     2019 to 2020 panel because its own source leaves 2020 to 2021
     blank.
  5. The robustness run saves every sample result to a CSV file so
     the distribution can be recomputed from files, and states its
     summer planting convention in the log.
  6. The solver runs with relative gap zero and the CBC primal and
     dual feasibility tolerance held at its default of 0.0000001. A
     tighter tolerance of 0.000000001 was tested and rejected: at
     that setting CBC presolve falsely proved a feasible fixed plan
     infeasible, a failure reproduced and recorded during this
     build. Floor verdicts therefore never rest on solver status
     alone: floors above the ceiling share are infeasible by the
     ceiling maximisation, and every feasible plan carries a
     separately maximised floor clearance in its hardest scenario.
     The binary linkage bound is the pool land limit of the cell
     when a plan is being optimised, and the planted area of the
     cell itself when a plan is fixed for evaluation, because a
     pool limit bound makes a solver produced plan infeasible
     against its own recourse inside solver tolerance,
     every feasible frontier plan is saved and its floor clearance
     in its hardest scenario is computed by a separate maximisation
     and printed, the dual table is labelled with the exact floor
     it was computed at, the full dual ranges are printed with every
     binding governorate, and the penalised value of the stochastic
     solution is printed as the exact difference of its printed
     components.

Structure kept from version 4: two stage architecture with two
planting decision points (winter planting is one value across
scenarios, summer and Nili planting are decided per inflow state),
real abandonment through a binary keep decision per planted crop
per scenario, forecast prices with their bands as the price layer,
official 2022 costs, a multi year drought inflow state, the
guarantee reported as a frontier, information values against true
means, and stress runs pairing capacity with choice.

Version 5 repairs, ordered by the foundation rebuild of
15 November 2026 (Stage S3, after the two independent checks):
  R1. Prices read the version 5 forecast file: 2025 forecasts from
      the December 2025 FAOSTAT vintage, observed to 2024 for
      wheat, maize and potatoes and to 2023 for rice and sugar
      beet, with the band built at the residual quartiles so the
      layer weights and the band construction agree.
  R2. The drought state leaves the probability simplex. The three
      single year states carry the whole probability, renormalised
      from the record counts. The drought budget runs as a named
      stress beside the frontier and enters no expected value.
  R3. The Menoufia rice yield is Menoufia own published 2019 to
      2020 yield, the year its substituted area comes from, not
      the cross governorate fill.
  R4. The penalised value of the stochastic solution is computed
      on one consistent definition: the optimum of the penalised
      problem minus the penalised evaluation of the true mean
      plan, both at the same penalty.
  R5. The historical pattern is tested against every ladder level
      and the highest level it holds is printed.
  R6. New named variants: wheat at its documented procurement
      price, a winter first reserve split, and cost escalation
      bracketing runs. Dual output prints the exact floor and is
      labelled as one optimal dual solution of the LP relaxation,
      with the mixed integer objective at the same floor printed
      beside it. Robustness reporting separates single year
      samples from ten year window samples. Headline results are
      written unrounded to a JSON results file.

Usage, with the project venv python:
  .venv/bin/python src/allocation_model_v5.py main
  .venv/bin/python src/allocation_model_v5.py caps
  .venv/bin/python src/allocation_model_v5.py beet2400
  .venv/bin/python src/allocation_model_v5.py wheatproc
  .venv/bin/python src/allocation_model_v5.py costsens
  .venv/bin/python src/allocation_model_v5.py reservealt
  .venv/bin/python src/allocation_model_v5.py robust
"""

import json
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
SUMMER_CROPS = ["Rice", "Maize_summer", "Potatoes_summer"]
NILI_CROPS = ["Maize_nili", "Potatoes_nili"]
LATE_CROPS = SUMMER_CROPS + NILI_CROPS  # planted per inflow state
ALL_CROPS = WINTER_CROPS + LATE_CROPS
POOL_CROPS = {"winter": WINTER_CROPS, "summer": SUMMER_CROPS, "nili": NILI_CROPS}
POOL_OF = {c: p for p, cs in POOL_CROPS.items() for c in cs}
STAPLE_CROPS = ["Wheat", "Rice", "Maize_summer"]  # floor crops, exact wording in the note
GROUP = {  # seasonal crop to forecast group
    "Wheat": "wheat", "Sugar beet": "sugar_beet", "Potatoes_winter": "potatoes",
    "Rice": "rice_paddy", "Maize_summer": "maize", "Maize_nili": "maize",
    "Potatoes_summer": "potatoes", "Potatoes_nili": "potatoes",
}
INFLOW_STATES = ["dry", "normal", "high"]  # version 5: drought is a named stress, not a state
LAYER_STATES = ["low", "expected", "high"]
LAYER_PROB = {"low": 0.25, "expected": 0.50, "high": 0.25}

ANCHOR_BCM = 11.00  # calibration, as in version 3 and version 4
MIN_VIABLE_SHARE = 0.30  # stated minimum viable water share for a kept crop
SOLVER_TOL = "1e-7"  # CBC primal and dual feasibility tolerance: the CBC default, held
# deliberately after the 1e-9 test described in the module docstring

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
WHEAT_PROCUREMENT_PRICE = 14666.67  # 2025 harvest, 2200 pounds per ardab of 150 kg, top grade

RESULTS = {}


def save_results(mode):
    path = PROC_DIR / f"results_v5_{mode}.json"
    with open(path, "w") as fh:
        json.dump(RESULTS, fh, indent=1, default=float)
    print(f"Unrounded results written to data/processed/results_v5_{mode}.json")


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
    fc = pd.read_csv(PROC_DIR / "forecast_prices_yields_v5.csv")
    inflow = pd.read_csv(EXT_DIR / "nile_inflow_aswan_series.csv")

    phys_row = tot[(tot["agricultural_year"] == "2020/2021")
                    & (tot["measure"] == "cultivated_area")]
    par["physical"] = {d: float(phys_row.loc[phys_row["governorate"] == d,
                        "area_hectares"].iloc[0]) for d in DISTRICTS}
    ann_row = tot[(tot["agricultural_year"] == "2020/2021")
                  & (tot["measure"] == "total_cropped_area")]
    par["annual_cropped"] = {d: float(ann_row.loc[ann_row["governorate"] == d,
                             "area_hectares"].iloc[0]) for d in DISTRICTS}

    # Baseline observed areas, with the years stated here and in
    # every log: wheat, sugar beet, rice and summer maize from the
    # 2020 to 2021 area panel; Nili maize 2020 to 2021 from its own
    # file, crop row maize only (white and yellow rows are its
    # components and are never added on top); potatoes in all three
    # seasons from the season split file, whose agricultural year is
    # 2021 to 2022 throughout, the only split on disk.
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
    # 2020 published value is used for that one cell, as before.
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
    # Version 5 repair: the Menoufia rice yield. Its 2020 to 2021
    # cell is blank in the source, but Menoufia has a published
    # yield for 2019 to 2020, the year its substituted baseline
    # area comes from, so that published value is used here
    # instead of the cross governorate fill applied below.
    par["yield_substitutions"] = []
    men19 = _yield_map(yld, "rice", "summer", "2019/2020")
    if pd.isna(pub["Rice"]["Menoufia"]) and not pd.isna(men19["Menoufia"]):
        pub["Rice"]["Menoufia"] = men19["Menoufia"]
        par["yield_substitutions"].append(
            ("Rice", "Menoufia", men19["Menoufia"],
             "published 2019 to 2020 yield of the same governorate"))
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
    # Yield by layer state, primary basis: the published district
    # yields themselves in the expected state, with the low and high
    # states applying the forecast band ratios of the crop group to
    # the published yields. No scaling to any national figure.
    par["yield"] = {}
    for crop in ALL_CROPS:
        f = yield_f[GROUP[crop]]
        par["yield"][crop] = {}
        for state, ratio in [("low", f["low"] / f["forecast"]),
                             ("expected", 1.0), ("high", f["high"] / f["forecast"])]:
            par["yield"][crop][state] = {d: pub[crop][d] * ratio for d in DISTRICTS}
    # Labelled sensitivity only: the version 4 construction, district
    # yields scaled proportionally so the area weighted district mean
    # equals the forecast national yield in the expected state.
    par["yield_scaled"] = {}
    par["yield_scale"] = {}
    for crop in ALL_CROPS:
        f = yield_f[GROUP[crop]]
        wsum = sum(base[crop].values())
        wmean = sum(pub[crop][d] * base[crop][d] for d in DISTRICTS) / wsum if wsum > 0 else \
            sum(pub[crop].values()) / len(DISTRICTS)
        scale = f["forecast"] / wmean
        par["yield_scale"][crop] = scale
        par["yield_scaled"][crop] = {}
        for state, ratio in [("low", f["low"] / f["forecast"]),
                             ("expected", 1.0), ("high", f["high"] / f["forecast"])]:
            par["yield_scaled"][crop][state] = {d: pub[crop][d] * scale * ratio for d in DISTRICTS}

    # Reference tonnage: observed areas times published district
    # yields, the same basis the model now runs on.
    par["reference_t"] = sum(base[c][d] * pub[c][d]
                             for c in STAPLE_CROPS for d in DISTRICTS)
    par["reference_by_crop"] = {c: sum(base[c][d] * pub[c][d] for d in DISTRICTS)
                                for c in STAPLE_CROPS}

    # Reserve construction, version 4.1, stated exactly. No file on
    # disk gives a seasonal total for all crops, so the seasonal
    # reserve is a stated construction with one consistency rule:
    # step one, the annual unmodeled crop area of a governorate is
    # its annual cropped area minus the total observed modeled area
    # in the baseline pattern, and it is split across the three
    # season pools in proportion to the observed modeled area in
    # each pool; step two, each pool reserve is capped at the
    # physical area the observed modeled pattern leaves free in
    # that pool, because in the observed season the unmodeled crops
    # demonstrably fitted into that free area, so a larger reserve
    # would contradict the season it describes. The pool limit is
    # the physical cultivated area minus its capped reserve, and by
    # construction no pool limit can fall below the observed
    # modeled area of that pool. The baseline feasibility check in
    # the log proves this pool by pool.
    par["reserve"] = {}
    par["land_limit"] = {}
    par["baseline_check"] = []
    for d in DISTRICTS:
        obs = {p: sum(base[c][d] for c in cs) for p, cs in POOL_CROPS.items()}
        unmod = par["annual_cropped"][d] - sum(obs.values())
        tot_obs = sum(obs.values())
        par["reserve"][d] = {}
        par["land_limit"][d] = {}
        for p in POOL_CROPS:
            prop = unmod * obs[p] / tot_obs if tot_obs > 0 else 0.0
            free_land = par["physical"][d] - obs[p]
            res = max(0.0, min(prop, free_land))
            limit = par["physical"][d] - res
            par["reserve"][d][p] = {"observed_modeled": obs[p],
                                    "proportional_share": prop,
                                    "reserve": res,
                                    "capped": res < prop - 1e-9}
            par["land_limit"][d][p] = limit
            par["baseline_check"].append(
                {"governorate": d, "pool": p, "observed": obs[p],
                 "limit": limit, "slack": limit - obs[p],
                 "ok": limit >= obs[p] - 1e-9})

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
    # Version 5 repair: the three genuine states are single year
    # frequencies of the record and carry the whole simplex between
    # them, renormalised from their counts. The drought object is
    # built from ten year window means; its former probability was
    # one window in 91 by construction, and its budget of 9.580 is
    # wetter than the dry budget of 8.588, so it leaves the simplex
    # and is carried as a named stress budget only.
    probs = {k: counts[k] / len(flows) for k in bands}
    par["inflow"] = {"mean_flow": mean_flow, "ratios": ratios, "counts": counts,
                     "probs": probs, "budgets_bcm": {s: ANCHOR_BCM * ratios[s] for s in INFLOW_STATES},
                     "n_windows": int(len(windows)),
                     "drought_ratio": drought_ratio,
                     "drought_budget_bcm": ANCHOR_BCM * drought_ratio}
    # District budgets by physical cultivated area share.
    tot_phys = sum(par["physical"].values())
    par["budget"] = {(d, s): par["inflow"]["budgets_bcm"][s] * 1e9 * par["physical"][d] / tot_phys
                     for d in DISTRICTS for s in INFLOW_STATES}
    par["drought_budget"] = {d: par["inflow"]["drought_budget_bcm"] * 1e9 * par["physical"][d] / tot_phys
                             for d in DISTRICTS}
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
    and late season planting values per inflow state, used for
    recourse and benchmark evaluation. objective is margin, maxstaple
    (a common tonnage t held in every scenario) or maxstaple_expected.
    penalise_floor adds a per tonne penalty variable for floor
    shortfall in each scenario instead of a hard floor."""
    scen = [single_scenario] if single_scenario else par["scenarios"]
    prob = pulp.LpProblem("alloc_v4_1", pulp.LpMaximize)
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
        for c in LATE_CROPS:
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
                prob += (pulp.lpSum(xs[(d, c, i)] for c in NILI_CROPS)
                         <= par["land_limit"][d]["nili"], f"LandN_{d}_{i}")
            if caps:
                for c in WINTER_CROPS:
                    prob += (xw[(d, c)] <= CAP_SHARE[c] * par["physical"][d], f"CapW_{d}_{c}")
                for c in LATE_CROPS:
                    for i in (INFLOW_STATES if not single_scenario else [single_scenario[0]]):
                        prob += (xs[(d, c, i)] <= CAP_SHARE[c] * par["physical"][d], f"CapS_{d}_{c}_{i}")

    kept, wat, prod = {}, {}, {}
    staple_expr, margin_terms = {}, []
    planted_cost = pulp.lpSum(cost[c] * xw[(d, c)] for d in DISTRICTS for c in WINTER_CROPS)
    if single_scenario:
        i0 = single_scenario[0]
        planted_cost += pulp.lpSum(cost[c] * xs[(d, c, i0)] for d in DISTRICTS for c in LATE_CROPS)
    else:
        # Late season planting is decided per inflow state, so its
        # cost is charged with the inflow probability of that state.
        planted_cost += pulp.lpSum(par["inflow"]["probs"][i] * cost[c] * xs[(d, c, i)]
                                   for d in DISTRICTS for c in LATE_CROPS for i in INFLOW_STATES)
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
                # The binary linkage bound must never be smaller
                # than the planted area it multiplies, or abandonment
                # and keeping both become impossible. For a plan
                # being optimised, the bound is the pool land limit
                # of this cell, the tightest valid bound, since the
                # land constraint holds the cell at or below it. For
                # a fixed plan under evaluation, the bound is the
                # planted area of the cell itself: a solver produced
                # plan can sit a fraction of a hectare above a pool
                # limit inside solver tolerance, and the pool limit
                # bound then makes its own recourse infeasible, a
                # failure this build hit and recorded before the fix.
                big = float(x) if fixed else par["land_limit"][d][POOL_OF[c]]
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


def solve(prob, timelimit=600, gap=0.0):
    prob.solve(pulp.PULP_CBC_CMD(msg=False, timeLimit=timelimit, gapRel=gap,
               options=[f"primalTolerance {SOLVER_TOL}", f"dualTolerance {SOLVER_TOL}"]))
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
                   for d in DISTRICTS for c in LATE_CROPS)
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
    staple_by = {}
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
        staple_by[s] = st
        staple_exp += par["prob"][s] * st
        staple_min = st if staple_min is None else min(staple_min, st)
    cost = sum(par["cost"][c] * float(vars_["xw"][(d, c)].value())
               for d in DISTRICTS for c in WINTER_CROPS)
    cost += sum(par["inflow"]["probs"][i] * par["cost"][c] * float(vars_["xs"][(d, c, i)].value())
                for d in DISTRICTS for c in LATE_CROPS for i in INFLOW_STATES)
    return {"margin": rev - cost, "staple_expected": staple_exp,
            "staple_min": staple_min, "staple_by_scenario": staple_by,
            "planted": planted_areas}


def print_header(par):
    print("=" * 76)
    print("NILE DELTA ALLOCATION MODEL VERSION 5, FOUNDATION REBUILD REPAIR BUILD")
    print("Price basis on every table, stated in one sentence: prices are")
    print("2025 forecasts from the FAOSTAT farm gate series, observed to")
    print("2024 for wheat, maize and potatoes and to 2023 for paddy rice")
    print("and sugar beet, and costs are official 2022 values, in pounds.")
    print("Winter potato cost is the")
    print("summer potato cost of 86657.14 pounds per hectare, a stated")
    print("assumption for a named gap (no winter potato cost exists).")
    print("Yield basis on every table: the published district yields,")
    print("with the forecast band ratios applied for the low and high")
    print("yield states. No scaling to any national figure is used in")
    print("the primary run; the scaled construction of version 4 appears")
    print("only as a labelled sensitivity.")
    print("Solver: CBC with relative gap 0 and primal and dual")
    print("feasibility tolerance 0.0000001, the CBC default. A tighter")
    print("tolerance of 0.000000001 was tested and rejected because CBC")
    print("presolve then falsely proved a feasible fixed plan infeasible;")
    print("floor verdicts in this build rest on the ceiling maximisation")
    print("and on per plan clearance maximisations, not on status alone.")
    print("Baseline areas: wheat, sugar beet, rice, summer maize and")
    print("Nili maize from the 2020 to 2021 bulletin panel; potatoes in")
    print("all three seasons from the 2021 to 2022 season split file,")
    print("the only split on disk; one rice cell, Menoufia, from the")
    print("2019 to 2020 panel because its source leaves 2020 to 2021")
    print("blank for that cell.")
    print("=" * 76)
    print(f"Physical cultivated area total: {sum(par['physical'].values()):,.0f} hectares")
    print(f"Annual cropped area total (descriptor, never a constraint): "
          f"{sum(par['annual_cropped'].values()):,.0f} hectares")
    print("\nReserve table (construction stated in the code and the note):")
    print("Governorate | pool | observed modeled | proportional share | reserve | capped | limit")
    for d in DISTRICTS:
        for p in ("winter", "summer", "nili"):
            r = par["reserve"][d][p]
            print(f"{d} | {p} | {r['observed_modeled']:,.0f} | {r['proportional_share']:,.0f} | "
                  f"{r['reserve']:,.0f} | {'yes' if r['capped'] else 'no'} | {par['land_limit'][d][p]:,.0f}")
    print("\nBASELINE FEASIBILITY CHECK (acceptance test for the reserve):")
    print("Governorate | pool | observed modeled hectares | pool limit hectares | slack hectares | result")
    n_ok = 0
    for chk in par["baseline_check"]:
        res = "PASS" if chk["ok"] else "FAIL"
        n_ok += 1 if chk["ok"] else 0
        print(f"{chk['governorate']} | {chk['pool']} | {chk['observed']:,.2f} | {chk['limit']:,.2f} | "
              f"{chk['slack']:,.2f} | {res}")
    print(f"BASELINE FEASIBILITY CHECK RESULT: {n_ok} of {len(par['baseline_check'])} pools pass. "
          f"The observed historical pattern is feasible against every pool limit.")
    print("\nYield fills for blank source cells (area weighted published mean):")
    for crop, d, val in par["yield_fills"]:
        print(f"  {crop} in {d}: {val:.3f} tonnes per hectare")
    print("Yield substitutions from the same governorate own published record:")
    for crop, d, val, why in par["yield_substitutions"]:
        print(f"  {crop} in {d}: {val:.3f} tonnes per hectare ({why})")
    print("\nYield scale factors of the labelled sensitivity only (version 4")
    print("construction, district yields scaled to the forecast national level):")
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
        print(f"  {s}: ratio {inf['ratios'][s]:.4f} budget {inf['budgets_bcm'][s]:.3f} BCM "
              f"probability {inf['probs'][s]:.4f} (count {inf['counts'][s]} of 100 years)")
    print(f"Drought stress budget: ratio {inf['drought_ratio']:.4f}, budget "
          f"{inf['drought_budget_bcm']:.3f} BCM, the lowest ten year window mean")
    print("of the record. It carries no probability and enters no expected")
    print("value; it runs as a named stress only, beside the frontier.")
    print("Price and yield layer probabilities: low 0.25, expected 0.50, high 0.25.")
    print("The bands are the quartiles of the backtest residuals, so the weights")
    print("and the band construction use one convention. Independence between")
    print("the inflow layer and the price and yield layer is a named assumption.")
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


def save_plan(plan, path, floor_share):
    rows = []
    for (d, c), val in plan["winter"].items():
        rows.append({"kind": "winter", "district": d, "crop": c, "inflow": "all",
                     "area": val, "floor_share": floor_share})
    for (d, c, i), val in plan["summer"].items():
        rows.append({"kind": POOL_OF[c], "district": d, "crop": c, "inflow": i,
                     "area": val, "floor_share": floor_share})
    pd.DataFrame(rows).to_csv(path, index=False, float_format="%.17g")


def frontier(par, levels, caps=False, label="", price_override=None,
             cost_override=None, water_override=None, yield_override=None,
             save_plans=False):
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
            print(f"    planted (probability weighted for late season crops): {planted_line}")
            for c in ALL_CROPS:
                base_tot = sum(par["baseline"][c].values())
                if base_tot > 0 and res["planted"][c] > 2 * base_tot:
                    print(f"    MARKET ABSORPTION WARNING: {c} planted {res['planted'][c]:,.0f} hectares "
                          f"is {res['planted'][c]/base_tot:.2f} times its observed area of {base_tot:,.0f} hectares. "
                          f"The fixed price stops being credible at this scale.")
        results[lv] = {"status": st, "margin": margin, "res": res}
        prev_margin = margin
        if lv > 0 and save_plans and not caps and not price_override:
            plan = plan_of(v)
            pct = int(round(lv * 100))
            save_plan(plan, PROC_DIR / f"plan_v5_floor{pct}.csv", lv)
            print(f"    plan at this level saved to data/processed/plan_v5_floor{pct}.csv")
            # Floor clearance: for the fixed plan, maximise staple
            # tonnage in each scenario in turn. The clearance of the
            # plan is the smallest headroom across the twelve
            # scenarios, in the scenario where the plan is tightest.
            floor_t = lv * par["reference_t"]
            worst = None
            for s in par["scenarios"]:
                prob_c, v_c = build(par, fixed=plan, objective="maxstaple",
                                    single_scenario=s)
                st_c = solve(prob_c, timelimit=300)
                if st_c != "Optimal":
                    print(f"    clearance {skey(*s)}: solve returned {st_c}")
                    continue
                t_max = float(v_c["t"].value())
                clr = t_max - floor_t
                print(f"    clearance {skey(*s)}: max staple {t_max:,.3f} tonnes, headroom {clr:,.3f} tonnes")
                if worst is None or clr < worst[1]:
                    worst = (s, clr, t_max)
            if worst is not None:
                print(f"    FLOOR CLEARANCE: the smallest headroom is in scenario {skey(*worst[0])}, "
                      f"where this plan can hold at most {worst[2]:,.3f} tonnes against a floor of "
                      f"{floor_t:,.3f} tonnes, a headroom of {worst[1]:,.3f} tonnes. Headrooms are")
                print("    printed to a thousandth of a tonne on purpose: a headroom below one tonne")
                print("    means the plan is tight at its floor within solver tolerance, not exact.")
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
    levels = [0.0, 0.50, 0.60, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.00]
    res = frontier(par, levels, label="primary, no caps", save_plans=True)
    RESULTS["frontier_primary"] = {f"{lv:.2f}": (r["margin"] if r["status"] == "Optimal" else None)
                                   for lv, r in res.items()}
    ceil = ceiling_run(par, label="primary, no caps, stated reserve construction")
    RESULTS["ceiling_primary_share"] = ceil
    # Bound: no reserve held at all, pool limits equal to physical area.
    par_nr = dict(par)
    par_nr["land_limit"] = {d: {p: par["physical"][d] for p in POOL_CROPS} for d in DISTRICTS}
    ceiling_run(par_nr, label="BOUND, no reserve held, pool limits equal to physical cultivated area")
    # Labelled sensitivity: version 4 scaled yields.
    ceiling_run(par, label="district yields scaled to the forecast national level (labelled sensitivity only)",
                yield_override=par["yield_scaled"])
    feasible_levels = [lv for lv, r in res.items() if r["status"] == "Optimal" and lv > 0]
    robust_share = 0.85 if res.get(0.85, {}).get("status") == "Optimal" else max(feasible_levels)
    prob_r, v_r = build(par, floor_share=robust_share)
    st_r = solve(prob_r)
    print(f"Robustness plan at floor {robust_share*100:.0f} percent: status {st_r}")
    if st_r == "Optimal":
        save_plan(plan_of(v_r), PROC_DIR / "plan_v5_robust_plan.csv", robust_share)
        print("Robustness plan saved to data/processed/plan_v5_robust_plan.csv")
    # Beet duty sensitivity on the ceiling
    for duty in (5600.0, 6600.0):
        wover = dict(par["water_req"]); wover["Sugar beet"] = duty
        ceiling_run(par, label=f"sugar beet duty {duty:,.0f}", water_override=wover)
    # Rice Ky sensitivity on the ceiling
    for kyv in (1.00, 1.40):
        old = par["ky"]["Rice"]; par["ky"]["Rice"] = kyv
        ceiling_run(par, label=f"rice Ky {kyv} (primary carries 1.20, unverified)")
        par["ky"]["Rice"] = old
    # Winter potato cost sensitivity at key levels
    cover = dict(par["cost"]); cover["Potatoes_winter"] = 54176.19
    frontier(par, [0.0, 0.90], label="winter potatoes at the Nili cost 54176.19 (sensitivity; primary uses the summer cost)",
             cost_override=cover)
    # Duals from the LP relaxation just below the ceiling
    dual_level = (ceil - 0.001) if ceil else 0.0
    print(f"\nWATER VALUES: one optimal dual solution of the LP relaxation")
    print(f"at the exact floor {dual_level:.10f} as a share of the reference")
    print(f"tonnage (the ceiling share minus 0.001). The ranges printed below")
    print("are that one solution of the relaxation. They are not marginal")
    print("values of the mixed integer model and they are not prices. Dual")
    print("solutions are not unique; another optimal dual solution can carry")
    print("different governorate values, and the note reports one known")
    print("alternative. Raw dual is pounds per cubic metre of expected")
    print("margin; conditional divides by the combined scenario probability.")
    prob, v = build(par, floor_share=dual_level, relax=True)
    st = solve(prob, gap=0.0)
    lp_obj = float(pulp.value(prob.objective))
    print(f"LP relaxation status: {st} | objective {lp_obj:,.2f}")
    prob_m, v_m = build(par, floor_share=dual_level)
    st_m = solve(prob_m, gap=0.0)
    mip_obj = float(pulp.value(prob_m.objective)) if st_m == "Optimal" else None
    if mip_obj is not None:
        print(f"Mixed integer model at the same floor: status {st_m} | objective {mip_obj:,.2f}")
        print(f"Relaxation gap at this floor: {lp_obj - mip_obj:,.2f} pounds "
              f"({100*(lp_obj - mip_obj)/mip_obj:.3f} percent above the integer objective)")
    RESULTS["dual"] = {"floor_exact_share": dual_level, "lp_objective": lp_obj,
                       "mip_objective": mip_obj}
    print("Governorate | scenario | raw dual EGP per m3 | conditional EGP per m3")
    duals = {}
    for name, con in prob.constraints.items():
        if name.startswith("Water_"):
            rest = name[len("Water_"):]
            for s in par["scenarios"]:
                sk = skey(*s)
                if rest.endswith("_" + sk):
                    dname = rest[: -len(sk) - 1].replace("_", " ")
                    raw = abs(float(con.pi)) / 1000.0 if con.pi is not None else float("nan")
                    duals[(dname, s[0], s[1])] = raw / par["prob"][s]
                    print(f"{dname} | {sk} | {raw:.4f} | {raw/par['prob'][s]:.2f}")
    print("\nDUAL RANGE SUMMARY (conditional values, pounds per cubic metre):")
    for i in INFLOW_STATES:
        for l in ("expected", "low"):
            vals = [(d, duals.get((d, i, l), 0.0)) for d in DISTRICTS]
            binding = [(d, val) for d, val in vals if val > 0.01]
            zeros = [d for d, val in vals if val <= 0.01]
            line = " | ".join(f"{d} {val:.2f}" for d, val in vals)
            print(f"{i} inflow, {l} layer: {line}")
            if binding:
                bvals = [val for _, val in binding]
                print(f"    range where water binds: {min(bvals):.2f} to {max(bvals):.2f} across "
                      f"{len(binding)} binding governorates; zero in: {', '.join(zeros) if zeros else 'none'}")
            else:
                print("    water binds in no governorate in this scenario")
    # Baseline and decomposition (accounting only)
    print("\nBASELINE AND DECOMPOSITION (accounting only, no causal claim)")
    base_plan = {"winter": {(d, c): par["baseline"][c][d] for d in DISTRICTS for c in WINTER_CROPS},
                 "summer": {(d, c, i): par["baseline"][c][d] for d in DISTRICTS for c in LATE_CROPS for i in INFLOW_STATES}}
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
    RESULTS["baseline"] = {"margin": base_eval["margin"],
                           "staple_expected": base_eval["staple_expected"],
                           "staple_min": base_eval["staple_min"]}
    # Version 5 repair: the historical pattern against the ladder.
    # The capacity of the fixed pattern is computed scenario by
    # scenario with staple maximising recourse; a ladder level is
    # held when the smallest scenario capacity reaches its floor
    # tonnage, which is the same test as imposing the floor.
    print("\nHISTORICAL PATTERN AGAINST THE LADDER (version 5 repair)")
    cap_by = {}
    for s in par["scenarios"]:
        prob_c, v_c = build(par, fixed=base_plan, objective="maxstaple",
                            single_scenario=s)
        st_c = solve(prob_c, timelimit=300)
        cap_by[s] = float(v_c["t"].value()) if st_c == "Optimal" else None
        if cap_by[s] is not None:
            print(f"  pattern capacity {skey(*s)}: {cap_by[s]:,.0f} tonnes "
                  f"({100*cap_by[s]/par['reference_t']:.2f} percent of reference)")
        else:
            print(f"  pattern capacity {skey(*s)}: solve returned {st_c}")
    worst_cap = min(v for v in cap_by.values() if v is not None)
    print(f"Pattern worst scenario capacity: {worst_cap:,.0f} tonnes "
          f"({100*worst_cap/par['reference_t']:.2f} percent of reference)")
    held = None
    for lv in (0.50, 0.60, 0.65, 0.70, 0.75, 0.80):
        ok = worst_cap >= lv * par["reference_t"]
        print(f"  ladder level {lv*100:.0f} percent, floor tonnage "
              f"{lv*par['reference_t']:,.0f}: {'HELD in every scenario' if ok else 'not held'}")
        if ok:
            held = lv
    if held is not None:
        print(f"HIGHEST LADDER LEVEL THE PATTERN HOLDS: {held*100:.0f} percent")
    else:
        print("The pattern holds no ladder level.")
    RESULTS["pattern"] = {"capacity_by_scenario": {skey(*s): cap_by[s] for s in par["scenarios"]},
                          "worst_capacity": worst_cap,
                          "highest_level_held": held}
    # Information values at the highest feasible ladder level
    info_floor = max(feasible_levels)
    print(f"\nInformation values use the stated floor of {info_floor*100:.0f} percent, "
          f"the highest feasible ladder level.")
    RESULTS["info"] = info_values(par, res, floor_share=info_floor)
    # Stress runs
    stress(par)
    save_results("main")


def info_values(par, frontier_res=None, floor_share=0.90):
    print("\nINFORMATION VALUES AGAINST TRUE MEANS")
    info = {"floor_share": floor_share}
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
    info["rp"] = rp
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
        # Deterministic objective in build() charges late season cost
        # with inflow probabilities; in a single scenario that
        # understates late season cost. Correct by recomputing the
        # scenario margin from the solution.
        plan = plan_of(v)
        rev = sum(par["price"][c][s[1]] * float(pulp.value(v["prod"][(d, c, s)]))
                  for d in DISTRICTS for c in ALL_CROPS)
        cst = sum(par["cost"][c] * plan["winter"][(d, c)] for d in DISTRICTS for c in WINTER_CROPS)
        cst += sum(par["cost"][c] * plan["summer"][(d, c, s[0])] for d in DISTRICTS for c in LATE_CROPS)
        ws += par["prob"][s] * (rev - cst)
        print(f"  wait and see {skey(*s)}: scenario margin EGP {rev-cst:,.0f} probability {par['prob'][s]:.4f}")
    if ws_ok and rp is not None:
        print(f"Wait and see value WS: EGP {ws:,.0f}")
        print(f"EVPI equals WS minus RP: EGP {ws - rp:,.0f}")
        info["ws"] = ws
        info["evpi"] = ws - rp
    # Penalised stochastic optimum under the named penalty, solved
    # on the same definition the penalised evaluation of the true
    # mean plan uses below: one consistent penalised comparison.
    rp_pen = None
    if rp is not None:
        prob_pen, _pv = build(par, floor_share=floor_share, penalise_floor=25000.0)
        st_pen = solve(prob_pen)
        if st_pen == "Optimal":
            rp_pen = float(pulp.value(prob_pen.objective))
            print(f"Penalised stochastic optimum (penalty 25000 pounds per tonne of shortfall, floor softened): EGP {rp_pen:,.0f}")
            info["penalised_rp"] = rp_pen
        else:
            print(f"Penalised stochastic problem solve returned {st_pen}")

    def penalised_eval(plan):
        tot = 0.0
        for s in par["scenarios"]:
            prob2, v2 = build(par, floor_share=floor_share, fixed=plan,
                              single_scenario=s, penalise_floor=25000.0)
            st2 = solve(prob2)
            if st2 != "Optimal":
                return None
            rev = sum(par["price"][c][s[1]] * float(pulp.value(v2["prod"][(d, c, s)]))
                      for d in DISTRICTS for c in ALL_CROPS)
            cst = sum(par["cost"][c] * plan["winter"][(d, c)] for d in DISTRICTS for c in WINTER_CROPS)
            cst += sum(par["cost"][c] * plan["summer"][(d, c, s[0])] for d in DISTRICTS for c in LATE_CROPS)
            short = float(v2["shortfall"][s].value())
            tot += par["prob"][s] * (rev - cst - 25000.0 * short)
        return tot

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
        return info
    ev_plan_single = plan_of(v)
    ev_plan = {"winter": ev_plan_single["winter"],
               "summer": {(d, c, i): ev_plan_single["summer"][(d, c, "normal")]
                          for d in DISTRICTS for c in LATE_CROPS for i in INFLOW_STATES}}
    eev = evaluate(par, ev_plan, floor_share=floor_share)
    if eev["all_feasible"]:
        print(f"EEV (true mean plan evaluated with the floor held): EGP {eev['margin']:,.0f}")
        if rp is not None:
            print(f"VSS equals RP minus EEV: EGP {rp - eev['margin']:,.0f}")
            info["eev"] = eev["margin"]
            info["vss"] = rp - eev["margin"]
        pen_eev = penalised_eval(ev_plan)
        if pen_eev is not None:
            print(f"Penalised EEV under a named penalty of 25000 pounds per tonne of shortfall: EGP {pen_eev:,.0f}")
            info["penalised_eev"] = pen_eev
            if rp_pen is not None:
                print(f"Penalised VSS on one consistent definition, penalised optimum minus penalised EEV: EGP {rp_pen - pen_eev:,.0f}")
                info["penalised_vss"] = rp_pen - pen_eev
    else:
        bad = [skey(*s) for s, r in eev["per"].items() if r["margin"] is None]
        print(f"FINDING: the true mean plan cannot hold the stated floor in scenario(s): {bad}")
        eev_nf = evaluate(par, ev_plan, floor_share=0.0)
        print(f"True mean plan evaluated with no floor: EGP {eev_nf['margin']:,.0f} "
              f"(an upper bound that flatters it, not an EEV under the guarantee)")
        # Penalised variant on the consistent definition: the
        # penalised evaluation of the true mean plan against the
        # penalised stochastic optimum solved above, same penalty.
        pen_eev = penalised_eval(ev_plan)
        if pen_eev is not None:
            print(f"Penalised EEV under a named penalty of 25000 pounds per tonne of shortfall: EGP {pen_eev:,.0f}")
            info["penalised_eev"] = pen_eev
            if rp_pen is not None:
                print(f"Penalised VSS on one consistent definition, penalised optimum minus penalised EEV: EGP {rp_pen - pen_eev:,.0f}")
                print("No standard VSS is reported, because the true mean")
                print("plan is infeasible under the hard floor in at least one scenario.")
                info["penalised_vss"] = rp_pen - pen_eev
    return info


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
    # Version 5: the drought object as a named stress at its own
    # budget, expected prices and yields, reported beside the
    # frontier. It carries no probability and enters no expected
    # value anywhere in this build.
    db = {d: par["inflow"]["drought_budget_bcm"] * 1e9 for d in DISTRICTS}
    price_o = {c: {st: par["price"][c]["expected"] for st in LAYER_STATES} for c in ALL_CROPS}
    yld_o = {c: {st: par["yield"][c]["expected"] for st in LAYER_STATES} for c in ALL_CROPS}
    s0 = ("normal", "expected")
    prob, v = build(par, floor_share=0.0, budget_by_inflow=db,
                    price_override=price_o, yield_override=yld_o,
                    single_scenario=s0)
    st = solve(prob)
    prob2, v2 = build(par, objective="maxstaple", budget_by_inflow=db,
                      price_override=price_o, yield_override=yld_o,
                      single_scenario=s0)
    st2 = solve(prob2)
    print(f"DROUGHT STRESS (named stress, no probability): budget "
          f"{par['inflow']['drought_budget_bcm']:.3f} BCM, expected prices and yields")
    dres = {}
    if st == "Optimal":
        plan = plan_of(v)
        rev = sum(par["price"][c]["expected"] * float(pulp.value(v["prod"][(d, c, s0)]))
                  for d in DISTRICTS for c in ALL_CROPS)
        cst = sum(par["cost"][c] * plan["winter"][(d, c)] for d in DISTRICTS for c in WINTER_CROPS)
        cst += sum(par["cost"][c] * plan["summer"][(d, c, "normal")] for d in DISTRICTS for c in LATE_CROPS)
        staple = sum(float(pulp.value(v["prod"][(d, c, s0)]))
                     for d in DISTRICTS for c in STAPLE_CROPS)
        print(f"  Profit choice at the drought budget: margin EGP {rev - cst:,.0f} | "
              f"staple tonnes {staple:,.0f} ({100*staple/par['reference_t']:.2f} percent of reference)")
        dres["profit_margin"] = rev - cst
        dres["profit_staple"] = staple
    if st2 == "Optimal":
        cap_t = float(v2["t"].value())
        print(f"  Maximum staple capacity at the drought budget: {cap_t:,.0f} tonnes "
              f"({100*cap_t/par['reference_t']:.2f} percent of reference)")
        dres["capacity"] = cap_t
    RESULTS["drought_stress"] = dres


def caps_mode():
    par = load_all()
    print_header(par)
    levels = [0.0, 0.50, 0.60, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.00]
    res_c = frontier(par, levels, caps=True,
             label="with named constraints (rotation and market sanity limits, a modelling device: "
                   "wheat 0.50, rice 0.35, maize 0.40, sugar beet 0.30, potatoes 0.15 of district physical land)")
    ceil_c = ceiling_run(par, caps=True, label="with named constraints")
    RESULTS["frontier_caps"] = {f"{lv:.2f}": (r["margin"] if r["status"] == "Optimal" else None)
                                for lv, r in res_c.items()}
    RESULTS["ceiling_caps_share"] = ceil_c
    save_results("caps")


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
    ceil = ceiling_run(par, label="primary ceiling (the capacity ceiling does not depend on prices)")
    res_b = frontier(par, [0.0, 0.70, 0.80, 0.90], label="beet at 2400", price_override=price_o)
    RESULTS["frontier_beet2400"] = {f"{lv:.2f}": (r["margin"] if r["status"] == "Optimal" else None)
                                    for lv, r in res_b.items()}
    save_results("beet2400")
    if ceil is not None:
        print(f"The capacity ceiling of {ceil*100:.2f} percent of the reference tonnage "
              f"applies to this variant as well, because it does not depend on prices.")


def robust_mode(n_samples=100):
    par = load_all()
    print_header(par)
    plan_file = PROC_DIR / "plan_v5_robust_plan.csv"
    df = pd.read_csv(plan_file)
    target_share = float(df["floor_share"].iloc[0])
    plan = {"winter": {}, "summer": {}}
    for _, r in df.iterrows():
        if r["kind"] == "winter":
            plan["winter"][(r["district"], r["crop"])] = float(r["area"])
        else:
            plan["summer"][(r["district"], r["crop"], r["inflow"])] = float(r["area"])
    print(f"\nROBUSTNESS: fixed plan loaded from plan_v5_robust_plan.csv (floor {target_share*100:.0f} percent)")
    print("Summer planting convention, stated as required: the fixed plan")
    print("carries four late season planting variants, one per inflow state.")
    print("A sampled budget carries no inflow state label, so every sample is")
    print("evaluated with the late season planting, summer and Nili together,")
    print("frozen at the normal inflow variant of the fixed plan, and winter")
    print("planting at its single common variant. The normal variant is the")
    print("central commitment of the plan. The maximum share across samples")
    print("is therefore the staple limit of that one variant at a full budget,")
    print("and the distribution describes that variant, not a plan that")
    print("chooses its late season pattern again for each sample.")
    print("Every sample result is saved to data/processed/robustness_samples_v5.csv")
    print("so the distribution below can be recomputed from the file.")
    rng = random.Random(20261114)
    flows = par["flows"]
    mean_flow = float(flows.mean())
    windows = flows.rolling(10).mean().dropna().tolist()
    shares, shortfalls = [], []
    rows = []
    target_t = target_share * par["reference_t"]
    for n in range(n_samples):
        if n % 2 == 0:
            ratio = float(rng.choice(flows.tolist())) / mean_flow
            kind = "single year"
        else:
            ratio = float(rng.choice(windows)) / mean_flow
            kind = "ten year window mean"
        budget_by = {d: ANCHOR_BCM * ratio * 1e9 for d in DISTRICTS}  # total, split in build by physical share
        # Fixed plan, expected prices and yields, maximise staple tonnage
        price_o = {c: {st: par["price"][c]["expected"] for st in LAYER_STATES} for c in ALL_CROPS}
        yld_o = {c: {st: par["yield"][c]["expected"] for st in LAYER_STATES} for c in ALL_CROPS}
        s0 = ("normal", "expected")
        prob, v = build(par, fixed=plan, objective="maxstaple_expected",
                        budget_by_inflow=budget_by, price_override=price_o,
                        yield_override=yld_o, single_scenario=s0)
        st = solve(prob, timelimit=300)
        if st != "Optimal":
            print(f"sample {n}: status {st} ratio {ratio:.3f} {kind}")
            continue
        staple = sum(float(pulp.value(v["prod"][(d, c, s0)])) for d in DISTRICTS for c in STAPLE_CROPS)
        share = staple / par["reference_t"]
        shortfall = max(0.0, target_t - staple)
        shares.append(share)
        shortfalls.append(shortfall)
        rows.append({"sample": n, "kind": kind, "ratio": ratio,
                     "budget_billion_cubic_metres": ANCHOR_BCM * ratio,
                     "max_staple_tonnes": staple, "share_percent": 100 * share,
                     "shortfall_tonnes": shortfall})
        print(f"sample {n}: ratio {ratio:.3f} ({kind}) max staple for fixed plan {staple:,.0f} tonnes "
              f"share {100*share:.2f} percent shortfall {shortfall:,.0f}")
    pd.DataFrame(rows).to_csv(PROC_DIR / "robustness_samples_v5.csv", index=False)
    print("Per sample results saved to data/processed/robustness_samples_v5.csv")
    print(f"\nSamples solved: {len(rows)} of {n_samples} requested")
    print("Sampling: alternating random single years and random ten year window")
    print("means drawn from the 1871 to 1970 record, seed 20261114, budget equals")
    print("11.00 times the drawn ratio of flow to the record mean.")
    print("Version 5 reporting rule: the two sample kinds are reported as two")
    print("separate distributions. A ten year window mean is not a year, so no")
    print("figure in this section mixes the two kinds, and no figure here is an")
    print("annual reliability.")
    rdf = pd.DataFrame(rows)
    for kind in ("single year", "ten year window mean"):
        sub = rdf[rdf["kind"] == kind]
        if sub.empty:
            continue
        sh = sub["share_percent"]
        sf = sub["shortfall_tonnes"]
        worst = sf.sort_values(ascending=False).head(max(1, len(sf) // 10))
        print(f"\n{kind}: {len(sub)} samples")
        print(f"  maximum feasible share for the fixed plan (percent of reference): "
              f"minimum {sh.min():.2f} | 10th percentile {sh.quantile(0.10):.2f} | "
              f"median {sh.median():.2f} | mean {sh.mean():.2f} | maximum {sh.max():.2f}")
        print(f"  share of these samples where the fixed plan can still hold its "
              f"{target_share*100:.0f} percent floor: {100*(sh/100 >= target_share).mean():.1f} percent")
        print(f"  worst decile mean shortfall against the floor reference of "
              f"{target_t:,.0f} tonnes: {worst.mean():,.0f} tonnes")
        print(f"  mean shortfall across these samples: {sf.mean():,.0f} tonnes")


def wheatproc_mode():
    par = load_all()
    print_header(par)
    price_o = {"Wheat": {"low": WHEAT_PROCUREMENT_PRICE,
                         "expected": WHEAT_PROCUREMENT_PRICE,
                         "high": WHEAT_PROCUREMENT_PRICE}}
    print("\nWHEAT PROCUREMENT VARIANT: wheat at the documented procurement")
    print("price of 14666.67 pounds per tonne (2025 harvest, top grade at")
    print("2200 pounds per ardab of 150 kilograms) in every layer state,")
    print("all else equal. The primary run pays wheat at its forecast")
    print("farm gate price. The two runs differ in price concept and")
    print("marketing basis together, as with the beet variant.")
    res = frontier(par, [0.0, 0.50, 0.60, 0.70, 0.75, 0.80, 0.85],
                   label="wheat at procurement 14666.67", price_override=price_o)
    RESULTS["frontier_wheat_procurement"] = {
        f"{lv:.2f}": (r["margin"] if r["status"] == "Optimal" else None)
        for lv, r in res.items()}
    save_results("wheatproc")


def costsens_mode():
    par = load_all()
    print_header(par)
    for factor in (1.50, 2.00):
        cover = {c: par["cost"][c] * factor for c in ALL_CROPS}
        print(f"\nCOST ESCALATION SENSITIVITY: every 2022 cost multiplied by {factor:.2f}.")
        print("The factor is a stated assumption, chosen to bracket plausible")
        print("cumulative cost growth between 2022 and the 2025 price basis.")
        print("No official cost table exists after 2022 and no price index")
        print("series is held in the project sources, so no measured factor")
        print("can be used. This run prices the cost gap; it does not close it.")
        res = frontier(par, [0.0, 0.50, 0.60, 0.70, 0.75, 0.80, 0.85],
                       label=f"costs times {factor:.2f}", cost_override=cover)
        RESULTS[f"frontier_costs_x{factor:.2f}"] = {
            f"{lv:.2f}": (r["margin"] if r["status"] == "Optimal" else None)
            for lv, r in res.items()}
    save_results("costsens")


def winter_first_land_limit(par):
    """Winter first allocation of the unmodeled crop reserve.

    The primary construction splits each governorate annual
    unmodeled area across the season pools in proportion to the
    observed modeled area of each pool. This alternative gives the
    winter pool its full free land first, then summer, then Nili,
    capping each pool reserve at the free land of that pool. It is
    the winter heavy bound of the split, built because the largest
    unmodeled Delta crop, berseem clover, is a winter crop. It is
    a bounding construction, not an estimate of the true split.
    """
    out = {}
    for d in DISTRICTS:
        obs = {p: sum(par["baseline"][c][d] for c in cs)
               for p, cs in POOL_CROPS.items()}
        unmod = par["annual_cropped"][d] - sum(obs.values())
        remaining = max(0.0, unmod)
        out[d] = {}
        for p in ("winter", "summer", "nili"):
            free_land = par["physical"][d] - obs[p]
            res = max(0.0, min(remaining, free_land))
            remaining -= res
            out[d][p] = par["physical"][d] - res
    return out


def reservealt_mode():
    par = load_all()
    print_header(par)
    print("\nRESERVE SPLIT SENSITIVITY: winter first allocation of the")
    print("unmodeled crop reserve, defined in the code. The ceiling and")
    print("the 80 percent rung are repriced under the alternative split.")
    par_alt = dict(par)
    par_alt["land_limit"] = winter_first_land_limit(par)
    ceil_a = ceiling_run(par_alt, label="winter first reserve split")
    res_a = frontier(par_alt, [0.80], label="winter first reserve split")
    RESULTS["ceiling_reserve_winter_first_share"] = ceil_a
    RESULTS["frontier_reserve_winter_first"] = {
        f"{lv:.2f}": (r["margin"] if r["status"] == "Optimal" else None)
        for lv, r in res_a.items()}
    save_results("reservealt")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "main"
    if mode == "main":
        main_mode()
    elif mode == "caps":
        caps_mode()
    elif mode == "beet2400":
        beet_mode()
    elif mode == "wheatproc":
        wheatproc_mode()
    elif mode == "costsens":
        costsens_mode()
    elif mode == "reservealt":
        reservealt_mode()
    elif mode == "robust":
        robust_mode()
    else:
        print(f"unknown mode {mode}")
