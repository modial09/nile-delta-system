"""Problem One version 6: the repair build decided on 16 November 2026.

Version 5 stays on disk unchanged as the verified record. This file
carries the six locked repairs and nothing else is redesigned:

  1. The guarantee floor is restated in wheat cover. The floor binds
     on wheat tonnage alone, and every level is a share of national
     wheat consumption of 20.6 million tonnes (USDA FAS Cairo,
     Grain and Feed Update EG2026-0013, September 2026, marketing
     year 2025/26). Months of stock is the same number in a second
     unit: wheat tonnage divided by one twelfth of consumption.
     The mixed aggregate tonnage of version 5 is retired as the
     headline unit and is still tracked in the outputs.
  2. Water keeps the 11.00 billion cubic metre calibration anchor,
     narrated everywhere as a built anchor, split across
     governorates by physical land share. District supply can be
     replaced by user supplied figures (see load_user_supply).
     The ladders are also solved at anchors scaled to 0.90 and 0.80.
  3. Scenarios are rebuilt on how the river is run now. A scenario
     water state is a starting Lake Nasser storage state (low,
     normal, high) crossed with an inflow year type (dry, normal,
     high). The budget follows one stated release rule: the
     authority aims at the anchor, storage covers part of a dry
     shortfall or absorbs part of a wet surplus, and the release
     factor is bounded between 0.70 and 1.05 of the anchor. The
     1871 to 1970 flow frequencies are retired as probability
     weights; the inflow ratios of that record survive only as the
     definitions of the three year types. Scenario weights are
     stated planning weights, and the distributionally robust runs
     exist because the weights are a stance, not a measurement.
  4. Rice area is bounded by the state decree: 1,074,200 feddans,
     451,164 hectares, Ministerial Resolution No. 543 of the
     Ministry of Water Resources and Irrigation, confirmed for
     2025/26 by OECD (2026). The decree binds in every run mode.
  5. Berseem is a winter crop competing with wheat, on the ministry
     data filed in data/external/v6_berseem_parameters.csv. Its
     price is a stated feed value construction: 0.125 times the
     maize price of the same layer, from standard feed table values
     for total digestible nutrients. It is not a measured price.
  6. Costs sit on one year, 2025. Wheat carries the Agricultural
     Research Center budget for 2024/25, 34,468 pounds per feddan
     including rent. Every other crop carries its official 2022
     cost moved to 2025 by the Egypt consumer price path of the
     workbook Egypt_Pakistan_Farm_Costs.xlsx (index 119.834237 in
     2022 to 234.759958 in 2025, a factor of 1.959093). The guessed
     multipliers of version 5 survive only as a sensitivity.

Methods added in this build, each in its simplest correct form:
distributionally robust optimisation over a finite ambiguity set of
scenario weight vectors (mode dro), conditional value at risk of
the margin reported beside every frontier rung (in the frontier
output itself), and the break even sensitivity and the Monte Carlo
and backtest runs in src/methods_v6.py.

Usage, with the project venv python:
  .venv/bin/python src/allocation_model_v6.py main
  .venv/bin/python src/allocation_model_v6.py caps
  .venv/bin/python src/allocation_model_v6.py scaled
  .venv/bin/python src/allocation_model_v6.py dro
  .venv/bin/python src/allocation_model_v6.py reservealt
  .venv/bin/python src/allocation_model_v6.py usersupply
"""

import json
import sys
import time
from pathlib import Path

import pandas as pd
import pulp

from user_template_v6 import TEMPLATE_PATH, read_user_template

BASE_DIR = Path(__file__).resolve().parents[1]
EXT_DIR = BASE_DIR / "data" / "external"
PROC_DIR = BASE_DIR / "data" / "processed"

DISTRICTS = [
    "Beheira", "Sharkia", "Dakahlia", "Kafr El Sheikh",
    "Gharbia", "Menoufia", "Qalyubia", "Damietta",
]
WINTER_CROPS = ["Wheat", "Sugar beet", "Potatoes_winter", "Berseem"]
SUMMER_CROPS = ["Rice", "Maize_summer", "Potatoes_summer"]
NILI_CROPS = ["Maize_nili", "Potatoes_nili"]
LATE_CROPS = SUMMER_CROPS + NILI_CROPS
ALL_CROPS = WINTER_CROPS + LATE_CROPS
POOL_CROPS = {"winter": WINTER_CROPS, "summer": SUMMER_CROPS, "nili": NILI_CROPS}
POOL_OF = {c: p for p, cs in POOL_CROPS.items() for c in cs}
FLOOR_CROP = "Wheat"
TRACKED_STAPLES = ["Wheat", "Rice", "Maize_summer"]
GROUP = {
    "Wheat": "wheat", "Sugar beet": "sugar_beet", "Potatoes_winter": "potatoes",
    "Rice": "rice_paddy", "Maize_summer": "maize", "Maize_nili": "maize",
    "Potatoes_summer": "potatoes", "Potatoes_nili": "potatoes",
    "Berseem": "berseem",
}

# The wheat cover basis. Consumption is national; the model grows
# wheat in the eight study governorates only, so a cover level reads
# as: the study area alone guarantees this share of what Egypt eats.
WHEAT_CONSUMPTION_T = 20_600_000.0
MONTHLY_CONSUMPTION_T = WHEAT_CONSUMPTION_T / 12.0

# The rice decree, hectares. See data/external/v6_facts.csv.
RICE_DECREE_HA = 451_164.0

ANCHOR_BCM = 11.00  # built calibration anchor, as in versions 3 to 5
MIN_VIABLE_SHARE = 0.30
SOLVER_TOL = "1e-7"

# Scenario design. Storage states and inflow year types.
STORAGE_STATES = ["low", "normal", "high"]
INFLOW_TYPES = ["dry", "normal", "high"]
WATER_STATES = [(s, i) for s in STORAGE_STATES for i in INFLOW_TYPES]
# Stated planning weights, not measured frequencies. Storage is
# weighted in equal thirds because the planner does not choose the
# starting storage. Inflow weights centre the normal year.
STORAGE_W = {"low": 1.0 / 3.0, "normal": 1.0 / 3.0, "high": 1.0 / 3.0}
INFLOW_W = {"dry": 0.30, "normal": 0.45, "high": 0.25}
LAYER_STATES = ["low", "expected", "high"]
LAYER_PROB = {"low": 0.25, "expected": 0.50, "high": 0.25}
# The stated release rule. Release factor equals the inflow ratio
# plus a storage adjustment, bounded to the stated band. A high
# storage start covers part of a dry shortfall; a low storage start
# holds release back so the lake can rebuild.
STORAGE_ADJ = {"low": -0.04, "normal": 0.02, "high": 0.10}
RELEASE_MIN, RELEASE_MAX = 0.70, 1.05

# Costs on the 2025 basis, pounds per hectare, rent included.
CPI_FACTOR_2022_2025 = 234.75995837953556 / 119.83423702899654
FEDDAN_HA = 0.42
WHEAT_COST_2025 = 34468.0 / FEDDAN_HA  # ARC budget 2024/25 per feddan
COST_2022 = {  # Ministry cost bulletin, pounds per hectare, as version 5
    "Sugar beet": 39454.76, "Rice": 41850.00,
    "Maize_summer": 37671.43, "Maize_nili": 37888.10,
    "Potatoes_summer": 86657.14, "Potatoes_nili": 54176.19,
    "Potatoes_winter": 86657.14,  # named gap: the summer cost, as version 5
    "Berseem": 9792.0 / FEDDAN_HA,  # ministry bulletin 2021 to 2022
}
COST_2025 = {c: v * CPI_FACTOR_2022_2025 for c, v in COST_2022.items()}
COST_2025["Wheat"] = WHEAT_COST_2025

WATER_REQ = {  # applied basis, cubic metres per hectare, as version 5
    "Wheat": 5126.0, "Rice": 16600.0, "Maize_summer": 9305.0,
    "Maize_nili": 7433.0, "Sugar beet": 6100.0,
    "Potatoes_winter": 4079.0, "Potatoes_summer": 6145.0,
    "Potatoes_nili": 6145.0,
    "Berseem": 6971.0,  # 2928 cubic metres per feddan, EJAE 2018
}
KY = {"Wheat": 1.05, "Rice": 1.20, "Maize_summer": 1.25, "Maize_nili": 1.25,
      "Sugar beet": 1.00, "Potatoes_winter": 1.10, "Potatoes_summer": 1.10,
      "Potatoes_nili": 1.10, "Berseem": 1.00}  # berseem 1.00 is a stated assumption
CAP_SHARE = {"Wheat": 0.50, "Sugar beet": 0.30, "Potatoes_winter": 0.15,
             "Rice": 0.35, "Maize_summer": 0.40, "Maize_nili": 0.40,
             "Potatoes_summer": 0.15, "Potatoes_nili": 0.15,
             "Berseem": 0.30}
BERSEEM_FEED_RATIO = 0.125  # stated feed value construction, see docstring
BERSEEM_YIELD_T_HA = 28.637 / FEDDAN_HA  # fresh tonnes per hectare
BERSEEM_DELTA_SHARE = 0.6824
BERSEEM_NATIONAL_FEDDAN = 1_253_666.0

RESULTS = {}


def save_results(mode):
    path = PROC_DIR / f"results_v6_{mode}.json"
    with open(path, "w") as fh:
        json.dump(RESULTS, fh, indent=1, default=float)
    print(f"Unrounded results written to data/processed/results_v6_{mode}.json")


def wkey(w):
    return f"{w[0]}_{w[1]}"


def skey(w, l):
    return f"{w[0]}_{w[1]}_{l}"


def cover_of(wheat_t):
    return wheat_t / WHEAT_CONSUMPTION_T


def months_of(wheat_t):
    return wheat_t / MONTHLY_CONSUMPTION_T


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


def load_user_supply():
    """User supplied district supply at the anchor, if a filled file
    exists at data/processed/user_district_supply.csv with columns
    governorate and user_supply_billion_cubic_metres. Returns a dict
    of district totals in cubic metres, or None. This is the design
    point the persona review asked for: district water is sensitive
    and unpublished, so the model accepts the figures of the user
    who holds them and stores nothing itself."""
    path = PROC_DIR / "user_district_supply.csv"
    if not path.exists():
        return None
    df = pd.read_csv(path)
    out = {}
    for d in DISTRICTS:
        row = df[df["governorate"] == d]
        if len(row) and not pd.isna(row["user_supply_billion_cubic_metres"].iloc[0]):
            out[d] = float(row["user_supply_billion_cubic_metres"].iloc[0]) * 1e9
    return out if len(out) == len(DISTRICTS) else None


def load_all(user_supply=None, user_template_path=TEMPLATE_PATH):
    """Load every parameter from the files on disk. Returns one dict.
    user_supply, when given, is a dict of district supply totals in
    cubic metres at the reference water state (normal storage,
    normal inflow); scenario budgets scale it by the release factor
    ratio of each state to the reference state. The decision maker
    template at user_template_path is read at this loading edge only
    when the file is present; a missing file changes nothing."""
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
    tot_phys = sum(par["physical"].values())

    # Baseline observed areas, years as in version 5, plus berseem:
    # the study area total is the 2024/25 national area times the
    # Delta share of 2021, split by physical land share. Both steps
    # are stated constructions; no district berseem area is published
    # in the sources held.
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
    if base["Rice"]["Menoufia"] == 0.0:
        fill = area[(area["crop"] == "rice") & (area["season"] == "summer")
                    & (area["agricultural_year"] == "2019/2020")
                    & (area["governorate"] == "Menoufia")]
        base["Rice"]["Menoufia"] = float(fill["area_hectares"].iloc[0])
    berseem_total_ha = BERSEEM_NATIONAL_FEDDAN * BERSEEM_DELTA_SHARE * FEDDAN_HA
    base["Berseem"] = {d: berseem_total_ha * par["physical"][d] / tot_phys
                       for d in DISTRICTS}
    par["baseline"] = base
    par["berseem_total_ha"] = berseem_total_ha

    # Published district yields, as version 5, plus berseem at its
    # national mean fresh yield in every district.
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
    pub["Berseem"] = {d: BERSEEM_YIELD_T_HA for d in DISTRICTS}
    par["yield_substitutions"] = []
    men19 = _yield_map(yld, "rice", "summer", "2019/2020")
    if pd.isna(pub["Rice"]["Menoufia"]) and not pd.isna(men19["Menoufia"]):
        pub["Rice"]["Menoufia"] = men19["Menoufia"]
        par["yield_substitutions"].append(
            ("Rice", "Menoufia", men19["Menoufia"],
             "published 2019 to 2020 yield of the same governorate"))
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

    # Forecast prices and yields with bands, from the version 5
    # forecasting run, unchanged. Berseem has no forecast of its own:
    # its price is the feed value construction on the maize price of
    # the same layer, and its yield does not vary by layer.
    price_f, yield_f = {}, {}
    for _, r in fc.iterrows():
        key = (r["crop"], r["target"])
        entry = {"forecast": float(r["forecast_value"]), "low": float(r["band_low"]),
                 "high": float(r["band_high"]), "rmse": float(r["backtest_rmse"]),
                 "mape": float(r["backtest_mape_pct"]), "model": r["selected_model"]}
        (price_f if r["target"] == "price" else yield_f)[r["crop"]] = entry
    par["price_forecast"] = price_f
    par["yield_forecast"] = yield_f
    par["price"] = {}
    for crop in ALL_CROPS:
        if crop == "Berseem":
            mf = price_f["maize"]
            par["price"][crop] = {"low": BERSEEM_FEED_RATIO * mf["low"],
                                  "expected": BERSEEM_FEED_RATIO * mf["forecast"],
                                  "high": BERSEEM_FEED_RATIO * mf["high"]}
        else:
            f = price_f[GROUP[crop]]
            par["price"][crop] = {"low": f["low"], "expected": f["forecast"], "high": f["high"]}
    par["yield"] = {}
    for crop in ALL_CROPS:
        par["yield"][crop] = {}
        if crop == "Berseem":
            for state in LAYER_STATES:
                par["yield"][crop][state] = {d: pub[crop][d] for d in DISTRICTS}
            continue
        f = yield_f[GROUP[crop]]
        for state, ratio in [("low", f["low"] / f["forecast"]),
                             ("expected", 1.0), ("high", f["high"] / f["forecast"])]:
            par["yield"][crop][state] = {d: pub[crop][d] * ratio for d in DISTRICTS}

    # Reference tonnages on the published basis, tracked for the
    # record. The floor no longer uses them; wheat cover does.
    par["reference_by_crop"] = {c: sum(base[c][d] * pub[c][d] for d in DISTRICTS)
                                for c in TRACKED_STAPLES}
    par["reference_t"] = sum(par["reference_by_crop"].values())
    par["pattern_wheat_t"] = par["reference_by_crop"]["Wheat"]

    # Reserve construction, exactly the version 4.1 construction
    # carried by version 5, now with berseem inside the modeled
    # winter pool, so the reserve shrinks by the berseem area the
    # model now carries itself.
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

    # Inflow year types from the record, Derivation A bands as in
    # version 3 (edges 0.85 and 1.08 of the record mean). In version
    # 6 the record supplies the year type definitions only. No
    # frequency of the record is used as a probability anywhere.
    flows = inflow["flow_billion_cubic_metres"].astype(float)
    mean_flow = float(flows.mean())
    lo_edge, hi_edge = 0.85 * mean_flow, 1.08 * mean_flow
    bands = {"dry": flows[flows < lo_edge],
             "normal": flows[(flows >= lo_edge) & (flows <= hi_edge)],
             "high": flows[flows > hi_edge]}
    ratios = {k: float(v.mean() / mean_flow) for k, v in bands.items()}
    # The stated release rule turns a year type and a storage start
    # into a budget factor on the anchor.
    factors = {}
    for s in STORAGE_STATES:
        for i in INFLOW_TYPES:
            f = ratios[i] + STORAGE_ADJ[s]
            factors[(s, i)] = min(RELEASE_MAX, max(RELEASE_MIN, f))
    par["inflow"] = {"mean_flow": mean_flow, "ratios": ratios,
                     "release_factors": factors,
                     "budgets_bcm": {w: ANCHOR_BCM * factors[w] for w in WATER_STATES}}
    ref_factor = factors[("normal", "normal")]
    # Decision maker template, read at this loading edge only. When
    # the file is absent, template stays None and every district
    # follows the exact default path below.
    template = None
    template_provenance = []
    if user_template_path is not None:
        default_water_bcm = {d: ANCHOR_BCM * ref_factor * par["physical"][d] / tot_phys
                             for d in DISTRICTS}
        template = read_user_template(user_template_path, default_water_bcm)
        if template is not None:
            template_provenance = list(template["water_provenance"])
    par["budget"] = {}
    for d in DISTRICTS:
        for w in WATER_STATES:
            if user_supply is not None:
                par["budget"][(d, w)] = user_supply[d] * factors[w] / ref_factor
            elif template is not None and d in template["water_filled_districts"]:
                par["budget"][(d, w)] = template["water_m3"][d] * factors[w] / ref_factor
            else:
                par["budget"][(d, w)] = (ANCHOR_BCM * factors[w] * 1e9
                                         * par["physical"][d] / tot_phys)
    par["user_supply"] = user_supply
    par["scenarios"] = [(w, l) for w in WATER_STATES for l in LAYER_STATES]
    par["prob"] = {(w, l): STORAGE_W[w[0]] * INFLOW_W[w[1]] * LAYER_PROB[l]
                   for (w, l) in par["scenarios"]}
    par["cost"] = dict(COST_2025)
    # Template crop prices and costs are applied here, at the
    # loading edge, after the public defaults exist. A filled cell
    # replaces only its named input; a blank cell keeps the default.
    if template is not None:
        for c in ALL_CROPS:
            raw_price = template["price_expected"].get(c)
            if raw_price is None:
                template_provenance.append(
                    f"Price for {c}: public default expected price "
                    f"{par['price'][c]['expected']:,.2f} pounds per tonne. "
                    "The cell was blank.")
            else:
                ratio = raw_price / par["price"][c]["expected"]
                par["price"][c] = {layer: value * ratio
                                    for layer, value in par["price"][c].items()}
                template_provenance.append(
                    f"Price for {c}: user expected price {raw_price:,.2f} pounds "
                    f"per tonne. The low and high bands moved by the same ratio "
                    f"of {ratio:.4f}.")
            raw_cost = template["cost"].get(c)
            if raw_cost is None:
                template_provenance.append(
                    f"Cost for {c}: public default cost "
                    f"{par['cost'][c]:,.2f} pounds per hectare. The cell was blank.")
            else:
                par["cost"][c] = raw_cost
                template_provenance.append(
                    f"Cost for {c}: user cost {raw_cost:,.2f} pounds per hectare.")
        par["user_input_path"] = template["path"]
    else:
        par["user_input_path"] = None
    par["user_input_provenance"] = template_provenance
    par["user_input"] = template
    par["water_req"] = dict(WATER_REQ)
    par["ky"] = dict(KY)
    par["flows"] = flows
    return par


def build(par, floor_cover=0.0, caps=False, fixed=None, budget_scale=1.0,
          price_override=None, yield_override=None, cost_override=None,
          water_override=None, objective="margin", relax=False,
          single_scenario=None, penalise_cover=None, dro_sets=None,
          budget_override=None):
    """Build the version 6 model. floor_cover is a share of national
    wheat consumption. fixed is a plan dict with winter planting and
    late planting per water state. dro_sets, when given, is a list of
    scenario weight dicts and the objective becomes the worst case
    expected margin over the set (distributionally robust form)."""
    scen = [single_scenario] if single_scenario else par["scenarios"]
    water_states = sorted({s[0] for s in scen}, key=lambda w: WATER_STATES.index(w))
    prob = pulp.LpProblem("alloc_v6", pulp.LpMaximize)
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
            for w in water_states:
                xs[(d, c, w)] = (fixed["summer"][(d, c, w)] if fixed else
                                 pulp.LpVariable(f"xs_{d}_{c}_{wkey(w)}", lowBound=0))
    if not fixed:
        for d in DISTRICTS:
            prob += (pulp.lpSum(xw[(d, c)] for c in WINTER_CROPS)
                     <= par["land_limit"][d]["winter"], f"LandW_{d}")
            for w in water_states:
                prob += (pulp.lpSum(xs[(d, c, w)] for c in SUMMER_CROPS)
                         <= par["land_limit"][d]["summer"], f"LandS_{d}_{wkey(w)}")
                prob += (pulp.lpSum(xs[(d, c, w)] for c in NILI_CROPS)
                         <= par["land_limit"][d]["nili"], f"LandN_{d}_{wkey(w)}")
            if caps:
                for c in WINTER_CROPS:
                    prob += (xw[(d, c)] <= CAP_SHARE[c] * par["physical"][d], f"CapW_{d}_{c}")
                for c in LATE_CROPS:
                    for w in water_states:
                        prob += (xs[(d, c, w)] <= CAP_SHARE[c] * par["physical"][d],
                                 f"CapS_{d}_{c}_{wkey(w)}")
        # The rice decree binds planted rice area in every water
        # state variant, in every mode, capped or not.
        for w in water_states:
            prob += (pulp.lpSum(xs[(d, "Rice", w)] for d in DISTRICTS)
                     <= RICE_DECREE_HA, f"RiceDecree_{wkey(w)}")

    kept, wat, prod = {}, {}, {}
    wheat_expr, margin_scen = {}, {}
    winter_cost = pulp.lpSum(cost[c] * xw[(d, c)] for d in DISTRICTS for c in WINTER_CROPS)
    late_cost = {w: pulp.lpSum(cost[c] * xs[(d, c, w)]
                               for d in DISTRICTS for c in LATE_CROPS)
                 for w in water_states}
    total_prob = sum(par["prob"][s] for s in scen)
    for (w, l) in scen:
        sk = skey(w, l)
        rev_terms = []
        for d in DISTRICTS:
            budget_d = (budget_override[(d, w)] if budget_override is not None
                        else par["budget"][(d, w)] * budget_scale)
            wvars = []
            for c in ALL_CROPS:
                x = xw[(d, c)] if c in WINTER_CROPS else xs[(d, c, w)]
                k = pulp.LpVariable(f"k_{d}_{c}_{sk}", lowBound=0, upBound=1, cat=cat)
                a = pulp.LpVariable(f"a_{d}_{c}_{sk}", lowBound=0)
                wv = pulp.LpVariable(f"w_{d}_{c}_{sk}", lowBound=0)
                kept[(d, c, (w, l))], wat[(d, c, (w, l))] = a, wv
                prob += (a <= x, f"KeptLe_{d}_{c}_{sk}")
                big = float(x) if fixed else par["land_limit"][d][POOL_OF[c]]
                prob += (a <= big * k, f"KeptBin_{d}_{c}_{sk}")
                prob += (a >= x - big * (1 - k), f"KeptEq_{d}_{c}_{sk}")
                prob += (wv <= (wreq[c] / 1000.0) * a, f"Wcap_{d}_{c}_{sk}")
                prob += (wv >= MIN_VIABLE_SHARE * (wreq[c] / 1000.0) * a, f"Wmin_{d}_{c}_{sk}")
                y = yld[c][l][d]
                q = y * (1 - par["ky"][c]) * a + (y * par["ky"][c] / (wreq[c] / 1000.0)) * wv
                prod[(d, c, (w, l))] = q
                rev_terms.append(price[c][l] * q)
                wvars.append(wv)
            prob += (pulp.lpSum(wvars) <= budget_d / 1000.0, f"Water_{d}_{sk}")
        wheat_expr[(w, l)] = pulp.lpSum(prod[(d, "Wheat", (w, l))] for d in DISTRICTS)
        margin_scen[(w, l)] = pulp.lpSum(rev_terms) - winter_cost - late_cost[w]
    margin = pulp.lpSum((par["prob"][s] / total_prob) * margin_scen[s] for s in scen)
    floor_t = floor_cover * WHEAT_CONSUMPTION_T
    shortfall_vars = {}
    if objective == "margin":
        if dro_sets is not None:
            z = pulp.LpVariable("z_worst_case", lowBound=None)
            for j, wset in enumerate(dro_sets):
                prob += (z <= pulp.lpSum(wset[s] * margin_scen[s] for s in scen),
                         f"DRO_{j}")
            obj = z
        else:
            obj = margin
        if penalise_cover is not None:
            pen = 0.0
            for s in scen:
                sv = pulp.LpVariable(f"short_{skey(*s)}", lowBound=0)
                shortfall_vars[s] = sv
                prob += (wheat_expr[s] + sv >= floor_t, f"SoftFloor_{skey(*s)}")
                pen += (par["prob"][s] / total_prob) * penalise_cover * sv
            obj = obj - pen
        elif floor_cover > 0:
            for s in scen:
                prob += (wheat_expr[s] >= floor_t, f"Floor_{skey(*s)}")
        prob += obj
    elif objective == "maxstaple":
        t = pulp.LpVariable("t_wheat", lowBound=0)
        for s in scen:
            prob += (wheat_expr[s] >= t, f"MaxWheat_{skey(*s)}")
        prob += t
        return prob, {"xw": xw, "xs": xs, "kept": kept, "wat": wat, "prod": prod, "t": t}
    elif objective == "maxwheat_expected":
        prob += pulp.lpSum((par["prob"][s] / total_prob) * wheat_expr[s] for s in scen)
    return prob, {"xw": xw, "xs": xs, "kept": kept, "wat": wat, "prod": prod,
                  "margin_scen": margin_scen, "shortfall": shortfall_vars}


def solve(prob, timelimit=900, gap=0.0):
    prob.solve(pulp.PULP_CBC_CMD(msg=False, timeLimit=timelimit, gapRel=gap,
               options=[f"primalTolerance {SOLVER_TOL}", f"dualTolerance {SOLVER_TOL}"]))
    return pulp.LpStatus[prob.status]


def plan_of(vars_):
    winter = {k: float(v.value()) for k, v in vars_["xw"].items()}
    summer = {k: float(v.value()) for k, v in vars_["xs"].items()}
    return {"winter": winter, "summer": summer}


def save_plan(plan, path, floor_cover):
    rows = []
    for (d, c), val in plan["winter"].items():
        rows.append({"kind": "winter", "district": d, "crop": c, "water_state": "all",
                     "area": val, "floor_cover": floor_cover})
    for (d, c, w), val in plan["summer"].items():
        rows.append({"kind": POOL_OF[c], "district": d, "crop": c,
                     "water_state": wkey(w), "area": val, "floor_cover": floor_cover})
    pd.DataFrame(rows).to_csv(path, index=False, float_format="%.17g")


def load_plan(path):
    df = pd.read_csv(path)
    plan = {"winter": {}, "summer": {}}
    for _, r in df.iterrows():
        if r["kind"] == "winter":
            plan["winter"][(r["district"], r["crop"])] = float(r["area"])
        else:
            s, i = r["water_state"].split("_")
            plan["summer"][(r["district"], r["crop"], (s, i))] = float(r["area"])
    return plan, float(df["floor_cover"].iloc[0])


def scenario_results(par, vars_):
    """Expected and per scenario results from a solved full model."""
    rev_s, wheat_s, staple_s = {}, {}, {}
    planted = {}
    water_prob = {w: STORAGE_W[w[0]] * INFLOW_W[w[1]] for w in WATER_STATES}
    for c in ALL_CROPS:
        if c in WINTER_CROPS:
            planted[c] = sum(float(vars_["xw"][(d, c)].value()) for d in DISTRICTS)
        else:
            planted[c] = sum(water_prob[w] * float(vars_["xs"][(d, c, w)].value())
                             for d in DISTRICTS for w in WATER_STATES)
    winter_cost = sum(par["cost"][c] * float(vars_["xw"][(d, c)].value())
                      for d in DISTRICTS for c in WINTER_CROPS)
    late_cost = {w: sum(par["cost"][c] * float(vars_["xs"][(d, c, w)].value())
                        for d in DISTRICTS for c in LATE_CROPS) for w in WATER_STATES}
    for s in par["scenarios"]:
        rev_s[s] = sum(par["price"][c][s[1]] * float(pulp.value(vars_["prod"][(d, c, s)]))
                       for d in DISTRICTS for c in ALL_CROPS)
        wheat_s[s] = sum(float(pulp.value(vars_["prod"][(d, "Wheat", s)]))
                         for d in DISTRICTS)
        staple_s[s] = sum(float(pulp.value(vars_["prod"][(d, c, s)]))
                          for d in DISTRICTS for c in TRACKED_STAPLES)
    margin_s = {s: rev_s[s] - winter_cost - late_cost[s[0]] for s in par["scenarios"]}
    exp_margin = sum(par["prob"][s] * margin_s[s] for s in par["scenarios"])
    return {"margin": exp_margin, "margin_by_scenario": margin_s,
            "wheat_expected": sum(par["prob"][s] * wheat_s[s] for s in par["scenarios"]),
            "wheat_min": min(wheat_s.values()), "wheat_by_scenario": wheat_s,
            "staple_expected": sum(par["prob"][s] * staple_s[s] for s in par["scenarios"]),
            "planted": planted}


def cvar_of(margin_by_scenario, probs, alpha=0.25):
    """Conditional value at risk of the margin: the probability
    weighted mean of the worst alpha share of scenarios."""
    items = sorted(margin_by_scenario.items(), key=lambda kv: kv[1])
    acc, total = 0.0, 0.0
    for s, m in items:
        take = min(probs[s], alpha - acc)
        if take <= 0:
            break
        total += take * m
        acc += take
    return total / alpha


def evaluate(par, plan, budget_scale=1.0, budget_override=None):
    """Recourse evaluation of a fixed plan over all 27 scenarios,
    margin seeking, no floor imposed. Returns per scenario margin
    and wheat tonnage."""
    out = {"margin": 0.0, "per": {}, "all_feasible": True, "wheat_min": None}
    for s in par["scenarios"]:
        prob, v = build(par, fixed=plan, budget_scale=budget_scale,
                        budget_override=budget_override, single_scenario=s)
        st = solve(prob, timelimit=300)
        if st != "Optimal":
            out["per"][s] = {"status": st, "margin": None, "wheat_t": None}
            out["all_feasible"] = False
            continue
        rev = sum(par["price"][c][s[1]] * float(pulp.value(v["prod"][(d, c, s)]))
                  for d in DISTRICTS for c in ALL_CROPS)
        cst = sum(par["cost"][c] * plan["winter"][(d, c)] for d in DISTRICTS for c in WINTER_CROPS)
        cst += sum(par["cost"][c] * plan["summer"][(d, c, s[0])]
                   for d in DISTRICTS for c in LATE_CROPS)
        wheat = sum(float(pulp.value(v["prod"][(d, "Wheat", s)])) for d in DISTRICTS)
        out["per"][s] = {"status": st, "margin": rev - cst, "wheat_t": wheat}
        out["margin"] += par["prob"][s] * (rev - cst)
    feas = [v["wheat_t"] for v in out["per"].values() if v["wheat_t"] is not None]
    out["wheat_min"] = min(feas) if feas else None
    out["wheat_expected"] = sum(par["prob"][s] * out["per"][s]["wheat_t"]
                                for s in par["scenarios"] if out["per"][s]["wheat_t"] is not None)
    return out


def print_header(par):
    print("=" * 76)
    print("NILE DELTA ALLOCATION MODEL VERSION 6, REPAIR BUILD OF 16 NOVEMBER 2026")
    print("Basis, stated in full: prices are 2025 forecasts from the FAOSTAT")
    print("farm gate series (the version 5 forecasting run, unchanged). Costs")
    print("are on the same year: wheat at the Agricultural Research Center")
    print("budget for 2024/25 of 34,468 pounds per feddan including rent;")
    print("every other crop at its official 2022 cost moved to 2025 by the")
    print(f"consumer price factor {CPI_FACTOR_2022_2025:.6f} (index 119.834237 in")
    print("2022 to 234.759958 in 2025, World Bank via the workbook). Berseem")
    print("cost is its 2021 to 2022 ministry budget on the same bridge.")
    print("The guarantee floor binds on wheat tonnage alone. Levels are")
    print("shares of national wheat consumption of 20,600,000 tonnes")
    print("(USDA FAS Cairo, EG2026-0013, September 2026). Months of stock")
    print("is wheat tonnage divided by one twelfth of that consumption.")
    print("Water budgets scale from the built calibration anchor of 11.00")
    print("billion cubic metres, which no source publishes, split across")
    print("governorates by physical land share. Scenario weights are stated")
    print("planning weights, not measured frequencies.")
    print("=" * 76)
    print(f"Physical cultivated area total: {sum(par['physical'].values()):,.0f} hectares")
    n_ok = sum(1 for chk in par['baseline_check'] if chk['ok'])
    print(f"BASELINE FEASIBILITY CHECK: {n_ok} of {len(par['baseline_check'])} pools pass.")
    if par.get("user_input_provenance"):
        print("\nDECISION MAKER INPUT TEMPLATE: which cells came from the user "
              "and which from the public defaults")
        print(f"  Template file: {par['user_input_path']}")
        for line in par["user_input_provenance"]:
            print(f"  {line}")
    print("\nYield fills for blank source cells (area weighted published mean):")
    for crop, d, val in par["yield_fills"]:
        print(f"  {crop} in {d}: {val:.3f} tonnes per hectare")
    for crop, d, val, why in par["yield_substitutions"]:
        print(f"  {crop} in {d}: {val:.3f} tonnes per hectare ({why})")
    print("\nCosts on the 2025 basis (pounds per hectare, rent included):")
    for c in ALL_CROPS:
        print(f"  {c}: {par['cost'][c]:,.2f}")
    print("\nBerseem: study area baseline "
          f"{par['berseem_total_ha']:,.0f} hectares (construction stated in the code), "
          f"yield {BERSEEM_YIELD_T_HA:.3f} tonnes per hectare fresh, "
          f"price {par['price']['Berseem']['expected']:,.2f} pounds per tonne "
          f"(feed value construction, 0.125 times the maize price).")
    base_rice = sum(par["baseline"]["Rice"].values())
    print(f"\nBaseline rice area: {base_rice:,.0f} hectares against the decree "
          f"bound of {RICE_DECREE_HA:,.0f} hectares "
          f"({'inside' if base_rice <= RICE_DECREE_HA else 'ABOVE'} the decree).")
    print("\nWater states: storage start, inflow year type, inflow ratio, "
          "release factor, budget at the anchor (BCM), planning weight")
    for w in WATER_STATES:
        wt = STORAGE_W[w[0]] * INFLOW_W[w[1]]
        print(f"  {w[0]} storage, {w[1]} inflow: ratio {par['inflow']['ratios'][w[1]]:.4f} "
              f"factor {par['inflow']['release_factors'][w]:.4f} "
              f"budget {par['inflow']['budgets_bcm'][w]:.3f} weight {wt:.4f}")
    print(f"\nPattern wheat on the published basis: {par['pattern_wheat_t']:,.0f} tonnes, "
          f"a cover of {100*cover_of(par['pattern_wheat_t']):.2f} percent, "
          f"{months_of(par['pattern_wheat_t']):.2f} months of stock, before recourse.")
    print("Tracked staples on the published basis: " +
          ", ".join(f"{c} {par['reference_by_crop'][c]:,.0f} tonnes" for c in TRACKED_STAPLES))


def frontier(par, levels, caps=False, label="", budget_scale=1.0,
             save_plans=False, price_override=None, cost_override=None,
             yield_override=None, land_limit=None):
    par_use = par
    if land_limit is not None:
        par_use = dict(par); par_use["land_limit"] = land_limit
    # Reporting fix: when a run carries its own prices or costs, the
    # reported margins must be valued on that same basis, so the
    # overrides are folded into the parameter copy used for both the
    # solve and the report. The primary runs carry no overrides and
    # are untouched by this.
    if price_override is not None:
        par_use = dict(par_use)
        merged = {c: dict(par_use["price"][c]) for c in ALL_CROPS}
        merged.update(price_override)
        par_use["price"] = merged
    if cost_override is not None:
        par_use = dict(par_use)
        par_use["cost"] = cost_override
    print(f"\nFRONTIER {label} caps={caps} budget_scale={budget_scale}")
    print("Cover percent | months | status | expected margin EGP | cost vs unconstrained EGP | "
          "cost vs next lower EGP | CVaR margin EGP | CVaR cost EGP | min scenario wheat tonnes")
    results = {}
    prev_margin, unc_margin = None, None
    prev_cvar, unc_cvar = None, None
    for lv in levels:
        t0 = time.time()
        prob, v = build(par_use, floor_cover=lv, caps=caps, budget_scale=budget_scale,
                        price_override=price_override, cost_override=cost_override,
                        yield_override=yield_override)
        st = solve(prob)
        if st != "Optimal":
            print(f"{lv*100:.1f} | {months_of(lv*WHEAT_CONSUMPTION_T):.2f} | {st} | none | none | none | "
                  f"none | none | none | seconds {time.time()-t0:.0f}")
            results[lv] = {"status": st}
            continue
        res = scenario_results(par_use, v)
        margin = res["margin"]
        cvar = cvar_of(res["margin_by_scenario"], par_use["prob"])
        if lv == 0:
            unc_margin, unc_cvar = margin, cvar
        cost_unc = (unc_margin - margin) if unc_margin is not None else 0.0
        cost_prev = (prev_margin - margin) if prev_margin is not None else 0.0
        cvar_cost = (unc_cvar - cvar) if unc_cvar is not None else 0.0
        print(f"{lv*100:.1f} | {months_of(lv*WHEAT_CONSUMPTION_T):.2f} | {st} | {margin:,.0f} | "
              f"{cost_unc:,.0f} | {cost_prev:,.0f} | {cvar:,.0f} | {cvar_cost:,.0f} | "
              f"{res['wheat_min']:,.0f} | seconds {time.time()-t0:.0f}")
        print(f"    expected wheat tonnes {res['wheat_expected']:,.0f} | "
              f"expected tracked staples {res['staple_expected']:,.0f}")
        planted_line = " | ".join(f"{c} {res['planted'][c]:,.0f} ha" for c in ALL_CROPS)
        print(f"    planted (probability weighted for late season crops): {planted_line}")
        for c in ALL_CROPS:
            base_tot = sum(par["baseline"][c].values())
            if base_tot > 0 and res["planted"][c] > 2 * base_tot:
                print(f"    MARKET ABSORPTION WARNING: {c} planted {res['planted'][c]:,.0f} hectares "
                      f"is {res['planted'][c]/base_tot:.2f} times its observed area of {base_tot:,.0f} hectares.")
        results[lv] = {"status": st, "margin": margin, "cvar": cvar, "res": res}
        prev_margin, prev_cvar = margin, cvar
        if save_plans:
            plan = plan_of(v)
            pct = int(round(lv * 100))
            tag = "caps" if caps else "relaxed"
            save_plan(plan, PROC_DIR / f"plan_v6_{tag}_cover{pct}.csv", lv)
            print(f"    plan saved to data/processed/plan_v6_{tag}_cover{pct}.csv")
    return results


def ceiling_run(par, caps=False, label="", budget_scale=1.0, land_limit=None):
    par_use = par
    if land_limit is not None:
        par_use = dict(par); par_use["land_limit"] = land_limit
    prob, v = build(par_use, caps=caps, objective="maxstaple", budget_scale=budget_scale)
    st = solve(prob)
    if st != "Optimal":
        print(f"CEILING {label}: status {st}")
        return None
    t = float(v["t"].value())
    print(f"CEILING {label}: maximum wheat tonnage held in every scenario {t:,.0f} tonnes, "
          f"a cover of {100*cover_of(t):.2f} percent, {months_of(t):.2f} months of stock")
    return cover_of(t)


def pattern_test(par):
    print("\nHISTORICAL PATTERN AGAINST THE LADDER (wheat cover units)")
    base_plan = {"winter": {(d, c): par["baseline"][c][d] for d in DISTRICTS for c in WINTER_CROPS},
                 "summer": {(d, c, w): par["baseline"][c][d] for d in DISTRICTS
                            for c in LATE_CROPS for w in WATER_STATES}}
    cap_by = {}
    for s in par["scenarios"]:
        prob_c, v_c = build(par, fixed=base_plan, objective="maxstaple", single_scenario=s)
        st_c = solve(prob_c, timelimit=300)
        cap_by[s] = float(v_c["t"].value()) if st_c == "Optimal" else None
    worst = min(v for v in cap_by.values() if v is not None)
    print(f"Pattern worst scenario wheat capacity: {worst:,.0f} tonnes, "
          f"a cover of {100*cover_of(worst):.2f} percent, {months_of(worst):.2f} months")
    held = None
    for lv in (0.15, 0.20, 0.25, 0.30):
        ok = worst >= lv * WHEAT_CONSUMPTION_T
        print(f"  cover level {lv*100:.0f} percent: {'HELD in every scenario' if ok else 'not held'}")
        if ok:
            held = lv
    ev = evaluate(par, base_plan)
    print(f"Pattern delivery under margin seeking recourse: expected margin "
          f"{ev['margin']:,.0f} pounds, expected wheat {ev['wheat_expected']:,.0f} tonnes, "
          f"minimum scenario wheat {ev['wheat_min']:,.0f} tonnes")
    return {"worst_capacity_t": worst, "held_cover": held,
            "delivery_margin": ev["margin"], "delivery_wheat_min": ev["wheat_min"]}


def winter_first_land_limit(par):
    """Winter first allocation of the unmodeled crop reserve, the
    construction carried from version 5, now with berseem modeled."""
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


def _frontier_record(res):
    return {f"{lv:.2f}": ({"margin": r["margin"], "cvar": r["cvar"],
                            "wheat_min": r["res"]["wheat_min"],
                            "wheat_expected": r["res"]["wheat_expected"]}
                           if r["status"] == "Optimal" else None)
            for lv, r in res.items()}


def main_mode():
    par = load_all()
    print_header(par)
    levels = [0.0, 0.15, 0.20, 0.25, 0.30, 0.35]
    res = frontier(par, levels, label="primary, no caps", save_plans=True)
    RESULTS["frontier_relaxed"] = _frontier_record(res)
    ceil = ceiling_run(par, label="primary, no caps")
    RESULTS["ceiling_relaxed_cover"] = ceil
    pat = pattern_test(par)
    RESULTS["pattern"] = pat
    price_o = {"Wheat": {"low": 14666.67, "expected": 14666.67, "high": 14666.67}}
    print("\nWHEAT PROCUREMENT VARIANT: wheat at the documented procurement price")
    print("of 14666.67 pounds per tonne (2025 harvest) in every layer, all else equal.")
    res_p = frontier(par, [0.0, 0.20, 0.25], label="wheat at procurement", price_override=price_o)
    RESULTS["frontier_wheat_procurement"] = _frontier_record(res_p)
    cover25 = {c: par["cost"][c] * 1.25 for c in ALL_CROPS}
    print("\nCOST SENSITIVITY: every cost 25 percent above the CPI bridge, a stated")
    print("bracket for farm costs outrunning consumer prices. It is a sensitivity")
    print("only; the primary bridge is the sourced one.")
    res_c = frontier(par, [0.0, 0.20], label="costs times 1.25", cost_override=cover25)
    RESULTS["frontier_costs_x1_25"] = _frontier_record(res_c)
    save_results("main")


def caps_mode():
    par = load_all()
    print_header(par)
    levels = [0.0, 0.15, 0.20, 0.25, 0.30, 0.35]
    res = frontier(par, levels, caps=True, label="with named caps", save_plans=True)
    RESULTS["frontier_caps"] = _frontier_record(res)
    ceil = ceiling_run(par, caps=True, label="with named caps")
    RESULTS["ceiling_caps_cover"] = ceil
    save_results("caps")


def scaled_mode():
    par = load_all()
    print_header(par)
    for scale in (0.90, 0.80):
        print(f"\n########## ANCHOR SCALE {scale:.2f} (total {ANCHOR_BCM*scale:.2f} BCM) ##########")
        res_r = frontier(par, [0.0, 0.15, 0.20, 0.25], label=f"relaxed, scale {scale}",
                         budget_scale=scale)
        ceil_r = ceiling_run(par, label=f"relaxed, scale {scale}", budget_scale=scale)
        res_c = frontier(par, [0.0, 0.15, 0.20, 0.25], caps=True,
                         label=f"capped, scale {scale}", budget_scale=scale)
        ceil_c = ceiling_run(par, caps=True, label=f"capped, scale {scale}", budget_scale=scale)
        RESULTS[f"frontier_relaxed_scale_{scale:.2f}"] = _frontier_record(res_r)
        RESULTS[f"ceiling_relaxed_scale_{scale:.2f}"] = ceil_r
        RESULTS[f"frontier_caps_scale_{scale:.2f}"] = _frontier_record(res_c)
        RESULTS[f"ceiling_caps_scale_{scale:.2f}"] = ceil_c
    # Named dry sequence stresses, capacity and choice side by side.
    print("\nDRY SEQUENCE STRESSES (named stresses, no probability)")
    print("Storage transition rule, stated: a dry year moves the storage")
    print("start one step down. A second dry year therefore opens at low")
    print("storage with a dry inflow, a state already in the scenario set;")
    print("its budget is the (low, dry) budget. A third dry year is priced")
    print("at the release rule floor of 0.70 of the anchor.")
    for label, scale in (("second dry year, budget of the (low, dry) state",
                          par["inflow"]["release_factors"][("low", "dry")]),
                         ("third dry year, release rule floor", RELEASE_MIN)):
        bud = {(d, w): ANCHOR_BCM * scale * 1e9 * par["physical"][d] / sum(par["physical"].values())
               for d in DISTRICTS for w in WATER_STATES}
        prob_c, v_c = build(par, objective="maxstaple", budget_override=bud)
        st_c = solve(prob_c)
        prob_m, v_m = build(par, floor_cover=0.0, budget_override=bud)
        st_m = solve(prob_m)
        if st_c == "Optimal":
            t = float(v_c["t"].value())
            print(f"  {label}: maximum wheat capacity {t:,.0f} tonnes, cover "
                  f"{100*cover_of(t):.2f} percent")
        if st_m == "Optimal":
            r_m = scenario_results(par, v_m)
            print(f"  {label}: profit choice margin {r_m['margin']:,.0f} pounds, "
                  f"expected wheat {r_m['wheat_expected']:,.0f} tonnes")
        RESULTS[f"stress_{label}"] = {"budget_scale": scale}
    save_results("scaled")


def _tilt(par, pred, factor=1.5):
    w = {}
    for s in par["scenarios"]:
        w[s] = par["prob"][s] * (factor if pred(s) else 1.0)
    tot = sum(w.values())
    return {s: v / tot for s, v in w.items()}


def dro_mode():
    par = load_all()
    print_header(par)
    sets = {"nominal": dict(par["prob"])}
    for w in WATER_STATES:
        sets[f"tilt {wkey(w)} x1.5"] = _tilt(par, lambda s, w=w: s[0] == w)
    sets["tilt low layer x1.5"] = _tilt(par, lambda s: s[1] == "low")
    sets["tilt low storage x1.5"] = _tilt(par, lambda s: s[0][0] == "low")
    print(f"\nDISTRIBUTIONALLY ROBUST RUNS, capped world, ambiguity set of "
          f"{len(sets)} weight vectors (nominal plus stated tilts of 1.5, renormalised)")
    RESULTS["dro"] = {}
    for lv in (0.0, 0.15, 0.20, 0.25):
        prob_n, v_n = build(par, floor_cover=lv, caps=True)
        st_n = solve(prob_n)
        if st_n != "Optimal":
            print(f"cover {lv*100:.0f} percent: nominal solve {st_n}")
            continue
        plan_n = plan_of(v_n)
        ev_n = evaluate(par, plan_n)
        marg_n = {s: ev_n["per"][s]["margin"] for s in par["scenarios"]}
        worst_n = min(sum(w[s] * marg_n[s] for s in par["scenarios"]) for w in sets.values())
        prob_d, v_d = build(par, floor_cover=lv, caps=True, dro_sets=list(sets.values()))
        st_d = solve(prob_d)
        if st_d != "Optimal":
            print(f"cover {lv*100:.0f} percent: robust solve {st_d}")
            continue
        z = float(pulp.value(prob_d.objective))
        plan_d = plan_of(v_d)
        ev_d = evaluate(par, plan_d)
        marg_d = {s: ev_d["per"][s]["margin"] for s in par["scenarios"]}
        worst_d = min(sum(w[s] * marg_d[s] for s in par["scenarios"]) for w in sets.values())
        print(f"cover {lv*100:.0f} percent: nominal plan expected {ev_n['margin']:,.0f}, "
              f"worst case over the set {worst_n:,.0f} | robust plan expected "
              f"{ev_d['margin']:,.0f}, worst case {worst_d:,.0f} (solver z {z:,.0f}) | "
              f"worst case gain {worst_d - worst_n:,.0f}, expected cost of robustness "
              f"{ev_n['margin'] - ev_d['margin']:,.0f}")
        RESULTS["dro"][f"{lv:.2f}"] = {
            "nominal_expected": ev_n["margin"], "nominal_worst": worst_n,
            "robust_expected": ev_d["margin"], "robust_worst": worst_d, "z": z}
    save_results("dro")


def reservealt_mode():
    par = load_all()
    print_header(par)
    print("\nRESERVE SPLIT RESULTS (printed in full, as the clarity assessment required)")
    alt = winter_first_land_limit(par)
    ceil_p = ceiling_run(par, caps=True, label="capped, primary proportional reserve split")
    ceil_a = ceiling_run(par, caps=True, label="capped, winter first reserve split",
                         land_limit=alt)
    res_p = frontier(par, [0.0, 0.20], caps=True, label="capped, primary split")
    res_a = frontier(par, [0.0, 0.20], caps=True, label="capped, winter first split",
                     land_limit=alt)
    RESULTS["ceiling_caps_primary_split"] = ceil_p
    RESULTS["ceiling_caps_winter_first_split"] = ceil_a
    RESULTS["frontier_caps_primary_split"] = _frontier_record(res_p)
    RESULTS["frontier_caps_winter_first_split"] = _frontier_record(res_a)
    if res_p.get(0.20, {}).get("status") == "Optimal" and res_a.get(0.20, {}).get("status") == "Optimal":
        print(f"\nAt 20 percent cover under caps: primary split margin "
              f"{res_p[0.20]['margin']:,.0f} pounds, winter first split margin "
              f"{res_a[0.20]['margin']:,.0f} pounds, a difference of "
              f"{res_a[0.20]['margin'] - res_p[0.20]['margin']:,.0f} pounds.")
    save_results("reservealt")


def usersupply_mode():
    par = load_all()
    print_header(par)
    print("\nUSER SUPPLIED DISTRICT WATER, demonstration run")
    print("A user holding district delivery records replaces the built split.")
    print("Demonstration supply: Damietta 20 percent above its default split,")
    print("Kafr El Sheikh 20 percent below, all other districts at default.")
    tot_phys = sum(par["physical"].values())
    demo = {}
    for d in DISTRICTS:
        v = ANCHOR_BCM * 1e9 * par["physical"][d] / tot_phys
        if d == "Damietta":
            v *= 1.20
        if d == "Kafr El Sheikh":
            v *= 0.80
        demo[d] = v
    path = PROC_DIR / "user_district_supply.csv"
    pd.DataFrame([{"governorate": d,
                   "user_supply_billion_cubic_metres": demo[d] / 1e9} for d in DISTRICTS]
                  ).to_csv(path, index=False)
    try:
        loaded = load_user_supply()
        print(f"Loader read the demonstration file: "
              f"{'all eight districts' if loaded == demo else 'MISMATCH'}")
        par_u = load_all(user_supply=loaded)
        ceil_d = ceiling_run(par, caps=True, label="capped, built split")
        ceil_u = ceiling_run(par_u, caps=True, label="capped, user supplied split")
        res_d = frontier(par, [0.0, 0.20], caps=True, label="capped, built split")
        res_u = frontier(par_u, [0.0, 0.20], caps=True, label="capped, user supplied split")
        RESULTS["usersupply"] = {"ceiling_built": ceil_d, "ceiling_user": ceil_u,
                                 "frontier_built": _frontier_record(res_d),
                                 "frontier_user": _frontier_record(res_u)}
    finally:
        path.unlink(missing_ok=True)
        print("Demonstration supply file removed; no user supply is stored.")
    save_results("usersupply")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "main"
    if mode == "main":
        main_mode()
    elif mode == "caps":
        caps_mode()
    elif mode == "scaled":
        scaled_mode()
    elif mode == "dro":
        dro_mode()
    elif mode == "reservealt":
        reservealt_mode()
    elif mode == "usersupply":
        usersupply_mode()
    else:
        print(f"unknown mode {mode}")
