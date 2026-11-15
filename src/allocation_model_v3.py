"""Problem One version 3: allocation of land and water under uncertainty.

Structure carried forward unchanged from version 2: a two stage
stochastic linear program in PuLP. Stage one plants hectares by
district and crop before the inflow is known. Stage two allocates
water under the scenario that occurs. Production uses the linear
yield response form with a production floor at zero on every
planting and scenario. Crop cap shares, district water budgets as
shares of the scenario total by land share, the food floor as one
constraint per scenario on staple production, dual reporting in
raw and conditional units, brute force dual verification inside
both the stochastic and the deterministic model, the water
coverage table, information values with wait and see statuses
reported, and stress runs at 10 and 20 percent water cuts all
follow version 2.

What changes in version 3 is the data. Every parameter now comes
from data/DATA_FOUNDATION.md, the permitted source. Each
parameter block below cites its foundation section. Prices are
FAOSTAT producer prices for 2023 in Egyptian pounds per tonne
(Section 2), with sugar beet run under two price concepts.
Costs are CAPMAS 2016 to 2017 levels in Egyptian pounds per
hectare, rent inclusive (Section 4), and every printed money
figure that rests on costs carries that label. National yields
are the FAOSTAT via Our World in Data Egypt means over 2014 to
2023 exactly as version 2 loads them (Section 1). District yield
multipliers are real and crop specific, computed from the 2020
to 2021 governorate panels (Section 7). The land base is total
cropped area for 2020 to 2021 by governorate (Section 5). The
baseline pattern is the real district pattern for 2020 to 2021
(Section 6). Water requirements are applied basis in the primary
case (Section 8) with a net basis sensitivity. Yield response
factors follow Section 9. Scenarios follow Derivation A of
Section 10 in the primary case, applied to the calibration
anchor of 11.00 billion cubic metres, with Derivation B as a
sensitivity. The 11.00 figure is a calibration, as Section 11
requires it to be labelled.

Usage: run with a variant argument, beet795 or beet2400.
"""

import sys
from pathlib import Path

import pandas as pd
import pulp

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"
EXT_DIR = BASE_DIR / "data" / "external"

CROPS = ["Wheat", "Rice", "Maize", "Sugar beet", "Potatoes"]
STAPLES = ["Wheat", "Rice", "Maize"]

OWID_STEMS = {
    "Wheat": "wheat",
    "Rice": "rice",
    "Maize": "maize",
    "Sugar beet": "sugar-beet",
    "Potatoes": "potato",
}

# Governorate panel keys in the external CSV files: crop name and
# season that carry each model crop for 2020 to 2021
# (foundation Section 6).
PANEL_KEY = {
    "Wheat": ("wheat", "winter"),
    "Rice": ("rice", "summer"),
    "Maize": ("maize", "summer"),
    "Sugar beet": ("sugar_beet", "winter"),
    "Potatoes": ("potatoes", "all_seasons"),
}

DISTRICTS = [
    "Beheira", "Sharkia", "Dakahlia", "Kafr El Sheikh",
    "Gharbia", "Menoufia", "Qalyubia", "Damietta",
]
SCENARIOS = ["low", "expected", "high"]

# Prices, FAOSTAT producer prices, latest complete year 2023,
# Egyptian pounds per tonne (foundation Section 2). Rice is
# paddy rice. Sugar beet is set by the run variant: 795 is the
# FAOSTAT farm gate value (Section 2) and 2400 is the factory
# procurement price for the 2024 to 2025 season (Section 3).
PRICE_2023_EGP_TON = {
    "Wheat": 10_000.0,
    "Rice": 18_761.0,
    "Maize": 14_400.0,
    "Potatoes": 8_160.0,
}
BEET_PRICE_VARIANTS = {"beet795": 795.0, "beet2400": 2_400.0}
# Confirmed 2025 wheat procurement anchor, Egyptian pounds per
# tonne (foundation Section 3), used in one variant run.
WHEAT_PROCUREMENT_2025_EGP_TON = 14_667.0

# Production costs, CAPMAS 2016 to 2017, Egyptian pounds per
# hectare, rent inclusive (foundation Section 4). Maize is the
# summer row. Potatoes: CAPMAS publishes no winter potatoes cost,
# so the summer row is adopted and flagged; see RERUN_CHOICES.md.
COST_EGP_HA_2016_2017 = {
    "Wheat": 21_473.81,
    "Rice": 19_902.38,
    "Maize": 18_933.33,
    "Sugar beet": 17_607.14,
    "Potatoes": 49_533.33,
}

# Water requirements, applied basis, primary case, cubic metres
# per hectare: CAPMAS 2017 as printed in Abdelwahab et al. 2024
# (foundation Section 8). The potatoes value is computed in code
# below as the area weighted mean of the winter value 4079 and
# the summer value 6145, weighted by the delivered 2020 to 2021
# winter and summer potato areas summed over the eight
# governorates, with the Nili area excluded for want of a
# published Nili requirement. That result is arithmetic on
# sourced values.
WATER_REQ_APPLIED_M3_HA = {
    "Wheat": 5_126.0,
    "Rice": 16_600.0,
    "Maize": 9_305.0,
    "Sugar beet": 9_426.0,
}
POTATO_WINTER_REQ = 4_079.0
POTATO_SUMMER_REQ = 6_145.0

# Water requirements, net basis, sensitivity case, cubic metres
# per hectare: Gabr 2022 (foundation Section 8). The wheat net
# row carries the foundation flag of internal inconsistency; the
# run log prints that flag where the net case is reported.
WATER_REQ_NET_M3_HA = {
    "Wheat": 1_272.0,
    "Rice": 11_441.0,
    "Maize": 5_762.0,
    "Sugar beet": 3_927.0,
    "Potatoes": 2_448.0,
}

# Yield response factors (foundation Section 9). Wheat is 1.05,
# the winter wheat value; Egypt grows winter wheat, and version
# 2 used 1.00. Rice 1.20 is carried from version 2 but is
# unverified per Section 9 and gap 23, and outputs label it so.
YIELD_RESPONSE = {
    "Wheat": 1.05,
    "Rice": 1.20,
    "Maize": 1.25,
    "Sugar beet": 1.00,
    "Potatoes": 1.10,
}

# Crop cap shares as in version 2. Declared modelling device.
CROP_CAP_SHARE = {
    "Wheat": 0.50,
    "Rice": 0.35,
    "Maize": 0.40,
    "Sugar beet": 0.30,
    "Potatoes": 0.15,
}

# Scenario anchor and derivations (foundation Section 10 applied
# to the calibration anchor of Section 11). The 11.00 billion
# cubic metres expected budget is a calibration.
ANCHOR_BCM = 11.00
DERIVATION_A_PROB = {"low": 0.23, "expected": 0.45, "high": 0.32}
DERIVATION_A_MULT = {"low": 0.781, "expected": 0.955, "high": 1.221}
DERIVATION_B_PROB = {"low": 0.33, "expected": 0.34, "high": 0.33}
DERIVATION_B_MULT = {"low": 0.811, "expected": 0.973, "high": 1.217}

# Foundation printed production weighted mean yields for the
# multiplier check, tonnes per hectare (foundation Section 7).
FOUNDATION_WEIGHTED_MEANS = {
    "Wheat": 6.87, "Rice": 9.14, "Maize": 8.79,
    "Sugar beet": 49.37, "Potatoes": 28.39,
}

FOOD_FLOOR_SHARE = 0.90


def load_crop_facts() -> pd.DataFrame:
    """National yields and areas exactly as version 2 loads them:
    FAOSTAT via Our World in Data, Egypt means over 2014 to 2023
    (foundation Section 1)."""
    rows = []
    for crop in CROPS:
        stem = OWID_STEMS[crop]
        yld = pd.read_csv(RAW_DIR / f"owid_{stem}-yields.csv")
        prd = pd.read_csv(RAW_DIR / f"owid_{stem}-production.csv")
        ycol = [c for c in yld.columns if c not in ("Entity", "Code", "Year")][0]
        pcol = [c for c in prd.columns if c not in ("Entity", "Code", "Year")][0]
        y = yld[(yld.Code == "EGY") & yld.Year.between(2014, 2023)].dropna(subset=[ycol])
        p = prd[(prd.Code == "EGY") & prd.Year.between(2014, 2023)].dropna(subset=[pcol])
        merged = y.set_index("Year")[ycol].rename("y").to_frame()
        merged["p"] = p.set_index("Year")[pcol]
        merged = merged.dropna()
        area = (merged["p"] / merged["y"]).mean()
        rows.append(
            {
                "crop": crop,
                "yield_t_ha": float(merged["y"].mean()),
                "area_ha": float(area),
                "production_t": float(area * merged["y"].mean()),
            }
        )
    return pd.DataFrame(rows).set_index("crop")


def load_land_base() -> dict:
    """Total cropped area 2020 to 2021 by governorate, hectares,
    read from capmas_governorate_total_cropped_area.csv
    (foundation Section 5)."""
    frame = pd.read_csv(EXT_DIR / "capmas_governorate_total_cropped_area.csv")
    frame = frame[
        (frame["agricultural_year"] == "2020/2021")
        & (frame["measure"] == "total_cropped_area")
    ]
    return {d: float(frame.loc[frame["governorate"] == d, "area_hectares"].iloc[0])
            for d in DISTRICTS}


def load_district_multipliers() -> tuple:
    """Real crop specific district yield multipliers from the
    2020 to 2021 panels (foundation Section 7).

    The production weighted mean yield for a crop is total
    production over the eight governorates divided by total area,
    where each governorate area is implied by its production and
    its published yield, both from the delivered CSV files. The
    multiplier for a district and crop is the district yield
    divided by that weighted mean. Menoufia rice is not reported
    in the source for 2020 to 2021: that one cell is filled with
    1.00, the weighted mean itself, a neutral fill for an
    unreported cell, flagged in the run log and in
    RERUN_CHOICES.md.
    Returns the multiplier table, the computed weighted means and
    the district yield table.
    """
    yld = pd.read_csv(EXT_DIR / "capmas_governorate_yield.csv")
    prd = pd.read_csv(EXT_DIR / "capmas_governorate_production.csv")
    mult = {}
    yields = {}
    weighted_means = {}
    for crop in CROPS:
        key_crop, key_season = PANEL_KEY[crop]
        ysub = yld[(yld["crop"] == key_crop) & (yld["season"] == key_season)
                   & (yld["agricultural_year"] == "2020/2021")]
        psub = prd[(prd["crop"] == key_crop) & (prd["season"] == key_season)
                   & (prd["agricultural_year"] == "2020/2021")]
        ymap = dict(zip(ysub["governorate"], ysub["yield_tons_per_hectare"]))
        yfed = dict(zip(ysub["governorate"], ysub["yield_tons_per_feddan"]))
        pmap = dict(zip(psub["governorate"], psub["production_tons"]))
        total_prod = 0.0
        total_area_ha = 0.0
        for d in DISTRICTS:
            if pd.isna(ymap.get(d)) or pd.isna(pmap.get(d)):
                continue
            total_prod += float(pmap[d])
            total_area_ha += float(pmap[d]) / float(yfed[d]) * 0.42
        wmean = total_prod / total_area_ha
        weighted_means[crop] = wmean
        for d in DISTRICTS:
            yields[(d, crop)] = ymap.get(d)
            if pd.isna(ymap.get(d)):
                mult[(d, crop)] = 1.00
            else:
                mult[(d, crop)] = float(ymap[d]) / wmean
    return mult, weighted_means, yields


def load_baseline_pattern() -> dict:
    """The real district pattern: hectares by governorate and
    crop for 2020 to 2021 from capmas_governorate_area.csv
    (foundation Section 6). Wheat winter, sugar beet winter,
    rice summer, maize summer, potatoes all seasons. Menoufia
    rice for 2020 to 2021 is not reported in the source table;
    the delivered 2019 to 2020 published value for that cell is
    used and flagged in RERUN_CHOICES.md."""
    area = pd.read_csv(EXT_DIR / "capmas_governorate_area.csv")
    baseline = {}
    for crop in CROPS:
        key_crop, key_season = PANEL_KEY[crop]
        sub = area[(area["crop"] == key_crop) & (area["season"] == key_season)
                   & (area["agricultural_year"] == "2020/2021")]
        amap = dict(zip(sub["governorate"], sub["area_hectares"]))
        for d in DISTRICTS:
            value = amap.get(d)
            if value is None or pd.isna(value):
                fill = area[(area["crop"] == key_crop)
                            & (area["season"] == key_season)
                            & (area["agricultural_year"] == "2019/2020")
                            & (area["governorate"] == d)]
                value = float(fill["area_hectares"].iloc[0])
            baseline[(d, crop)] = float(value)
    return baseline


def potato_applied_requirement() -> tuple:
    """Area weighted mean of the winter and summer applied
    potato requirements (foundation Section 8), weighted by the
    delivered 2020 to 2021 winter and summer potato areas summed
    over the eight governorates. The Nili area is excluded from
    the weighting for want of a published Nili requirement.
    Returns the requirement and the two weights in hectares."""
    area = pd.read_csv(EXT_DIR / "capmas_governorate_area.csv")
    pot = area[(area["crop"] == "potatoes")
               & (area["agricultural_year"] == "2020/2021")]
    winter_ha = float(pot.loc[pot["season"] == "winter", "area_hectares"].sum())
    summer_ha = float(pot.loc[pot["season"] == "summer", "area_hectares"].sum())
    req = (POTATO_WINTER_REQ * winter_ha + POTATO_SUMMER_REQ * summer_ha) / (
        winter_ha + summer_ha)
    return req, winter_ha, summer_ha


def build_parameter_set(beet_price: float, wheat_price: float | None = None,
                        water_req: dict | None = None,
                        prob: dict | None = None, mult: dict | None = None,
                        floor_share: float = FOOD_FLOOR_SHARE) -> dict:
    """Assemble every parameter from the foundation sources."""
    facts = load_crop_facts()
    land_ha = load_land_base()
    yield_mult, weighted_means, district_yields = load_district_multipliers()
    baseline_x = load_baseline_pattern()
    potato_req, potato_winter_ha, potato_summer_ha = potato_applied_requirement()

    price = dict(PRICE_2023_EGP_TON)
    price["Sugar beet"] = beet_price
    if wheat_price is not None:
        price["Wheat"] = wheat_price

    if water_req is None:
        water_req = dict(WATER_REQ_APPLIED_M3_HA)
        water_req["Potatoes"] = potato_req

    prob = dict(prob) if prob is not None else dict(DERIVATION_A_PROB)
    mult = dict(mult) if mult is not None else dict(DERIVATION_A_MULT)
    budgets_bcm = {s: ANCHOR_BCM * mult[s] for s in SCENARIOS}

    total_land_ha = sum(land_ha.values())
    land_share = {d: land_ha[d] / total_land_ha for d in DISTRICTS}
    water_budget = {
        (d, s): budgets_bcm[s] * 1e9 * land_share[d]
        for d in DISTRICTS for s in SCENARIOS
    }

    # Baseline staple production at full water, with the same
    # national yields and real multipliers as the model, so the
    # floor and the baseline stay consistent.
    baseline_staple_t = sum(
        baseline_x[(d, c)] * facts.loc[c, "yield_t_ha"] * yield_mult[(d, c)]
        for d in DISTRICTS for c in STAPLES
    )

    return {
        "facts": facts,
        "yield_t_ha": {c: float(facts.loc[c, "yield_t_ha"]) for c in CROPS},
        "price": price,
        "cost": dict(COST_EGP_HA_2016_2017),
        "water_req": water_req,
        "ky": dict(YIELD_RESPONSE),
        "cap_share": dict(CROP_CAP_SHARE),
        "land_ha": land_ha,
        "yield_mult": yield_mult,
        "district_yields": district_yields,
        "weighted_means": weighted_means,
        "water_budget": water_budget,
        "budgets_bcm": budgets_bcm,
        "baseline_x": baseline_x,
        "food_floor_t": floor_share * baseline_staple_t,
        "baseline_staple_t": baseline_staple_t,
        "prob": prob,
        "scenarios": list(SCENARIOS),
        "potato_req": potato_req,
        "potato_winter_ha": potato_winter_ha,
        "potato_summer_ha": potato_summer_ha,
    }


def production_expr(par: dict, d: str, c: str, x, w):
    """Linear production in tons for one planting in one scenario.
    Carried from version 2: production equals the full water
    yield times one minus the yield response factor times the
    shortfall share, written in x and w so it stays linear.
    The district multiplier is now crop specific: yield_mult is
    keyed by district and crop."""
    y = par["yield_t_ha"][c] * par["yield_mult"][(d, c)]
    ky = par["ky"][c]
    req = par["water_req"][c]
    return y * (1.0 - ky) * x + (y * ky / req) * w


def build_problem(par: dict, scenario_names: list, water_scale: float = 1.0,
                  food_floor: bool = True, fixed_x: dict | None = None,
                  name: str = "allocation", floor_tolerance: float = 0.0) -> tuple:
    """Build one linear program over the given scenarios, as in
    version 2. Stage one variables are hectares by district and
    crop. Stage two variables are water delivered by district,
    crop and scenario. The production floor at zero applies to
    every planting and scenario. The food floor is one constraint
    per scenario on staple production."""
    prob_model = pulp.LpProblem(name, pulp.LpMaximize)
    x = {}
    for d in DISTRICTS:
        for c in CROPS:
            if fixed_x is None:
                x[(d, c)] = pulp.LpVariable(f"x_{d}_{c}", lowBound=0)
            else:
                x[(d, c)] = fixed_x[(d, c)]
    w = {
        (d, c, s): pulp.LpVariable(f"w_{d}_{c}_{s}", lowBound=0)
        for d in DISTRICTS for c in CROPS for s in scenario_names
    }
    revenue = pulp.lpSum(
        par["prob"][s] / sum(par["prob"][t] for t in scenario_names)
        * par["price"][c]
        * production_expr(par, d, c, x[(d, c)], w[(d, c, s)])
        for d in DISTRICTS for c in CROPS for s in scenario_names
    )
    cost = pulp.lpSum(par["cost"][c] * x[(d, c)] for d in DISTRICTS for c in CROPS)
    prob_model += revenue - cost
    for d in DISTRICTS:
        if fixed_x is None:
            prob_model += (
                pulp.lpSum(x[(d, c)] for c in CROPS) <= par["land_ha"][d],
                f"Land_{d}",
            )
            for c in CROPS:
                prob_model += (
                    x[(d, c)] <= par["cap_share"][c] * par["land_ha"][d],
                    f"Cap_{d}_{c}",
                )
        for s in scenario_names:
            prob_model += (
                pulp.lpSum(w[(d, c, s)] for c in CROPS)
                <= par["water_budget"][(d, s)] * water_scale,
                f"Water_{d}_{s}",
            )
            for c in CROPS:
                prob_model += (
                    w[(d, c, s)] <= par["water_req"][c] * x[(d, c)],
                    f"Req_{d}_{c}_{s}",
                )
            for c in CROPS:
                prob_model += (
                    production_expr(par, d, c, x[(d, c)], w[(d, c, s)]) >= 0,
                    f"ProdFloor_{d}_{c}_{s}",
                )
    if food_floor:
        for s in scenario_names:
            prob_model += (
                pulp.lpSum(
                    production_expr(par, d, c, x[(d, c)], w[(d, c, s)])
                    for d in DISTRICTS for c in STAPLES
                )
                >= par["food_floor_t"] * (1.0 - floor_tolerance),
                f"FoodFloor_{s}",
            )
    return prob_model, {"x": x, "w": w}


def solve_model(prob_model) -> str:
    prob_model.solve(pulp.PULP_CBC_CMD(msg=False))
    return pulp.LpStatus[prob_model.status]


def build_deterministic_model(par: dict, scenario: str, water_scale: float = 1.0,
                              food_floor: bool = True) -> tuple:
    prob_model, variables = build_problem(
        par, [scenario], water_scale=water_scale, food_floor=food_floor,
        name=f"deterministic_{scenario}",
    )
    status = solve_model(prob_model)
    return prob_model, variables, status


def build_stochastic_model(par: dict, water_scale: float = 1.0,
                           food_floor: bool = True) -> tuple:
    """Build and solve the extensive form across all scenarios.
    If the food floor makes the problem infeasible, the model is
    rebuilt without the floor and the caller is told through the
    returned flag, as in version 2, because a floor that cannot
    be held under a water cut is itself a result."""
    prob_model, variables = build_problem(
        par, par["scenarios"], water_scale=water_scale, food_floor=food_floor,
        name="stochastic",
    )
    status = solve_model(prob_model)
    floor_held = food_floor
    if status != "Optimal" and food_floor:
        prob_model, variables = build_problem(
            par, par["scenarios"], water_scale=water_scale, food_floor=False,
            name="stochastic_nofloor",
        )
        status = solve_model(prob_model)
        floor_held = False
    return prob_model, variables, status, floor_held


def evaluate_plan(par: dict, x_values: dict, water_scale: float = 1.0,
                  food_floor: bool = False) -> dict:
    """Evaluate one fixed planting plan across all scenarios, as
    in version 2. The water recourse alone is free. A scenario the
    fixed plan cannot satisfy under the floor is reported with
    its status and no numbers."""
    out = {"margin": 0.0, "staple_t": 0.0, "water_m3": 0.0, "per_scenario": {},
           "all_feasible": True}
    for s in par["scenarios"]:
        # The planting is held through the fixed_x path of
        # build_problem, which is the path its own docstring
        # names for this evaluation. Bounding the stage one
        # variables instead, as version 2 did, misreports plans
        # that sit exactly on a crop cap as infeasible, because
        # solver values carry rounding at the cap boundary. The
        # version 3 run caught that fault: the average year plan
        # scored as infeasible in all three scenarios. With the
        # planting fixed as numbers, the water recourse alone is
        # free, exactly as the design states.
        prob_model, variables = build_problem(
            par, [s], water_scale=water_scale, food_floor=food_floor,
            fixed_x=x_values, name=f"eval_{s}", floor_tolerance=1e-6,
        )
        status = solve_model(prob_model)
        if status != "Optimal":
            out["per_scenario"][s] = {"status": status, "margin": None,
                                      "staple_t": None, "water_m3": None}
            out["all_feasible"] = False
            continue
        margin = pulp.value(prob_model.objective)
        staple = sum(
            float(pulp.value(production_expr(
                par, d, c, variables["x"][(d, c)],
                variables["w"][(d, c, s)])))
            for d in DISTRICTS for c in STAPLES
        )
        water = sum(
            float(variables["w"][(d, c, s)].value())
            for d in DISTRICTS for c in CROPS
        )
        out["per_scenario"][s] = {"margin": margin, "staple_t": staple, "water_m3": water}
        out["margin"] += par["prob"][s] * margin
        out["staple_t"] += par["prob"][s] * staple
        out["water_m3"] += par["prob"][s] * water
    return out


def extract_shadow_prices(solved_model, par: dict,
                          scenario_names: list | None = None) -> pd.DataFrame:
    """Return the water value map from a solved model, as in
    version 2: one row per district and scenario, in two labelled
    units. shadow_price_egp_m3 is the raw dual on the district
    water constraint, the change in expected margin from one more
    cubic metre delivered in that scenario. conditional_egp_m3
    divides the raw dual by the scenario probability and gives
    the value of one more cubic metre inside that scenario. Both
    are duals, that is marginal values."""
    names = scenario_names or par["scenarios"]
    probs = par["prob"]
    name_lookup = {d.replace(" ", "_"): d for d in DISTRICTS}
    rows = []
    for constraint_name, constraint in solved_model.constraints.items():
        if not constraint_name.startswith("Water_"):
            continue
        rest = constraint_name[len("Water_"):]
        for s in names:
            if rest.endswith("_" + s):
                district = name_lookup.get(rest[: -len(s) - 1], rest[: -len(s) - 1])
                raw = abs(float(constraint.pi))
                row = {
                    "district": district,
                    "scenario": s,
                    "shadow_price_egp_m3": raw,
                }
                total = sum(probs[t] for t in names)
                row["conditional_egp_m3"] = raw / (probs[s] / total)
                rows.append(row)
    frame = pd.DataFrame(rows)
    return frame.sort_values(["district", "scenario"]).reset_index(drop=True)


def plan_from_variables(variables: dict) -> dict:
    return {k: float(v.value()) for k, v in variables["x"].items()}


def scenario_results(par: dict, prob_model, variables: dict) -> dict:
    out = {"per_scenario": {}, "margin": 0.0, "staple_t": 0.0, "water_m3": 0.0}
    planted_cost = sum(
        par["cost"][c] * float(variables["x"][(d, c)].value())
        for d in DISTRICTS for c in CROPS
    )
    for s in par["scenarios"]:
        revenue = sum(
            par["price"][c]
            * float(pulp.value(production_expr(
                par, d, c, variables["x"][(d, c)], variables["w"][(d, c, s)])))
            for d in DISTRICTS for c in CROPS
        )
        staple = sum(
            float(pulp.value(production_expr(
                par, d, c, variables["x"][(d, c)], variables["w"][(d, c, s)])))
            for d in DISTRICTS for c in STAPLES
        )
        water = sum(
            float(variables["w"][(d, c, s)].value())
            for d in DISTRICTS for c in CROPS
        )
        margin = revenue - planted_cost
        out["per_scenario"][s] = {"margin": margin, "staple_t": staple, "water_m3": water}
        out["margin"] += par["prob"][s] * margin
        out["staple_t"] += par["prob"][s] * staple
        out["water_m3"] += par["prob"][s] * water
    return out


def district_margins(par: dict, variables: dict, scenario: str) -> dict:
    out = {}
    for d in DISTRICTS:
        value = 0.0
        for c in CROPS:
            prod = float(pulp.value(production_expr(
                par, d, c, variables["x"][(d, c)], variables["w"][(d, c, scenario)])))
            value += par["price"][c] * prod - par["cost"][c] * float(
                variables["x"][(d, c)].value())
        out[d] = value
    return out


def district_staples(par: dict, variables: dict, scenario: str) -> dict:
    out = {}
    for d in DISTRICTS:
        out[d] = sum(
            float(pulp.value(production_expr(
                par, d, c, variables["x"][(d, c)], variables["w"][(d, c, scenario)])))
            for c in STAPLES
        )
    return out


def information_values(par: dict) -> dict:
    """Expected value of perfect information and value of the
    stochastic solution, as in version 2. Wait and see statuses
    are recorded and reported, never silently zeroed."""
    scenarios = par["scenarios"]
    rp_model, _vars_rp, status_rp, _floor = build_stochastic_model(par)
    rp = pulp.value(rp_model.objective) if status_rp == "Optimal" else float("nan")
    ws = 0.0
    ws_status = {}
    for s in scenarios:
        det_model, _, status = build_deterministic_model(par, s)
        ws_status[s] = status
        if status != "Optimal":
            ws += 0.0
        else:
            ws += par["prob"][s] * pulp.value(det_model.objective)
    det_exp, vars_exp, status_exp = build_deterministic_model(par, "expected")
    x_exp = plan_from_variables(vars_exp)
    eev_floored = evaluate_plan(par, x_exp, food_floor=True)
    if eev_floored["all_feasible"]:
        eev = eev_floored["margin"]
        return {
            "recourse_value_egp": rp,
            "wait_and_see_egp": ws,
            "ws_status": ws_status,
            "evpi_egp": ws - rp,
            "eev_egp": eev,
            "vss_egp": rp - eev,
            "eev_floor_breach": [],
        }
    breach = [
        s for s in scenarios
        if eev_floored["per_scenario"][s]["margin"] is None
    ]
    eev_upper = evaluate_plan(par, x_exp, food_floor=False)["margin"]
    return {
        "recourse_value_egp": rp,
        "wait_and_see_egp": ws,
        "ws_status": ws_status,
        "evpi_egp": ws - rp,
        "eev_egp": None,
        "eev_upper_bound_egp": eev_upper,
        "vss_egp": None,
        "eev_floor_breach": breach,
    }


def dual_check(par: dict, district: str = "Dakahlia", bump: float = 0.01) -> dict:
    """Verify one shadow price by brute force inside the
    deterministic expected scenario model, as in version 2."""
    base_model, _, status = build_deterministic_model(par, "expected")
    base_obj = pulp.value(base_model.objective)
    base_dual = abs(float(base_model.constraints[f"Water_{district}_expected"].pi))
    bumped = dict(par)
    bumped["water_budget"] = dict(par["water_budget"])
    key = (district, "expected")
    bumped["water_budget"][key] = par["water_budget"][key] * (1.0 + bump)
    bump_model, _, _ = build_deterministic_model(bumped, "expected")
    delta_m3 = par["water_budget"][key] * bump
    implied = (pulp.value(bump_model.objective) - base_obj) / delta_m3
    return {"dual": base_dual, "implied_by_bump": implied, "delta_m3": delta_m3}


def water_coverage(par: dict, variables: dict) -> pd.DataFrame:
    """Share of the agronomic water requirement actually
    delivered, by crop and scenario, as in version 2."""
    rows = []
    for c in CROPS:
        row = {"crop": c}
        for s in par["scenarios"]:
            delivered = sum(
                float(variables["w"][(d, c, s)].value()) for d in DISTRICTS
            )
            required = sum(
                par["water_req"][c] * float(variables["x"][(d, c)].value())
                for d in DISTRICTS
            )
            row[s] = delivered / required if required > 0 else float("nan")
        rows.append(row)
    return pd.DataFrame(rows).set_index("crop")


def dual_check_stochastic(par: dict, district: str = "Dakahlia",
                          scenario: str = "expected",
                          bump: float = 0.001) -> dict:
    """Verify one reported stochastic dual by brute force inside
    the full stochastic model, as in version 2. The bump is one
    tenth of the version 2 share: on the real data a 1 percent
    bump crosses a kink point and understates the dual, while a
    0.1 percent bump reproduces it, as the run log shows."""
    base_model, _vars, status, _held = build_stochastic_model(par)
    base_obj = pulp.value(base_model.objective)
    base_dual = abs(float(base_model.constraints[
        f"Water_{district.replace(' ', '_')}_{scenario}"].pi))
    bumped = dict(par)
    bumped["water_budget"] = dict(par["water_budget"])
    key = (district, scenario)
    bumped["water_budget"][key] = par["water_budget"][key] * (1.0 + bump)
    bump_model, _bvars, bstatus, _bheld = build_stochastic_model(bumped)
    delta_m3 = par["water_budget"][key] * bump
    implied = (pulp.value(bump_model.objective) - base_obj) / delta_m3
    return {"dual": base_dual, "implied_by_bump": implied,
            "delta_m3": delta_m3, "status": bstatus}


def gain_under(par_mod: dict) -> dict | None:
    """Optimised margin, baseline margin and gain under one
    parameter set, with the baseline reevaluated under the same
    parameters, as in version 2."""
    m, v, st, fh = build_stochastic_model(par_mod)
    if st != "Optimal":
        return None
    r = scenario_results(par_mod, m, v)
    b = evaluate_plan(par_mod, par_mod["baseline_x"])
    gain = r["margin"] - b["margin"]
    return {"opt": r["margin"], "base": b["margin"], "gain": gain,
            "gain_pct": 100.0 * gain / b["margin"], "floor_held": fh,
            "opt_per_m3": r["margin"] / r["water_m3"],
            "base_per_m3": b["margin"] / b["water_m3"]}


COST_LABEL = "costs at 2016 to 2017 levels"
PRICE_LABEL = "prices at 2023 levels"


def print_parameters(par: dict, beet_label: str) -> None:
    """Print the full parameter set with foundation sections."""
    print("=" * 72)
    print(f"PROBLEM ONE, VERSION 3 RUN, variant {beet_label}")
    print("Every parameter is from data/DATA_FOUNDATION.md.")
    print("=" * 72)
    facts = par["facts"]
    print("\nNational crop yields, Egypt means 2014 to 2023, FAOSTAT via")
    print("Our World in Data (foundation Section 1):")
    print(facts.round(2).to_string())
    print("\nPrices, FAOSTAT producer prices, latest complete year 2023,")
    print("Egyptian pounds per tonne (foundation Section 2). Rice is paddy.")
    for c in CROPS:
        note = ""
        if c == "Sugar beet":
            if par["price"][c] == 795.0:
                note = " (FAOSTAT farm gate, Section 2)"
            else:
                note = " (factory procurement 2024 to 2025, Section 3)"
        if c == "Wheat" and par["price"][c] == WHEAT_PROCUREMENT_2025_EGP_TON:
            note = " (confirmed 2025 procurement anchor, Section 3)"
        print(f"  {c:<12} EGP {par['price'][c]:>10,.0f} per tonne{note}")
    print("\nProduction costs, CAPMAS 2016 to 2017, Egyptian pounds per")
    print("hectare, rent inclusive (foundation Section 4). Potatoes uses")
    print("the summer row: CAPMAS publishes no winter potatoes cost, so")
    print("the summer row is adopted and flagged. Every cost figure in")
    print("this run is at 2016 to 2017 levels.")
    for c in CROPS:
        print(f"  {c:<12} EGP {par['cost'][c]:>10,.2f} per hectare")
    print("\nWater requirements in this parameter set, cubic metres per hectare:")
    for c in CROPS:
        print(f"  {c:<12} {par['water_req'][c]:>10,.2f}")
    print(f"Potatoes applied value is arithmetic on sourced values: winter "
          f"{POTATO_WINTER_REQ:,.0f} weighted by {par['potato_winter_ha']:,.2f} "
          f"hectares and summer {POTATO_SUMMER_REQ:,.0f} weighted by "
          f"{par['potato_summer_ha']:,.2f} hectares, Nili area excluded "
          f"(foundation Section 8).")
    print("\nYield response factors (foundation Section 9). Wheat 1.05 is")
    print("the winter wheat value. Rice 1.20 is carried from version 2")
    print("but is unverified, per Section 9 and gap 23.")
    for c in CROPS:
        print(f"  {c:<12} {par['ky'][c]:.2f}")
    print("\nLand base, total cropped area 2020 to 2021, hectares, read from")
    print("capmas_governorate_total_cropped_area.csv (foundation Section 5):")
    for d in DISTRICTS:
        print(f"  {d:<16} {par['land_ha'][d]:>12,.2f}")
    print(f"  {'Total':<16} {sum(par['land_ha'].values()):>12,.2f}")
    print("\nDistrict yield multipliers, real and crop specific, computed")
    print("from the 2020 to 2021 panels (foundation Section 7). Menoufia")
    print("rice is a neutral fill of 1.00 for an unreported cell.")
    mult_frame = pd.DataFrame(
        {c: [par["yield_mult"][(d, c)] for d in DISTRICTS] for c in CROPS},
        index=DISTRICTS)
    print(mult_frame.round(3).to_string())
    print("\nProduction weighted mean yields, computed against foundation")
    print("Section 7 printed values, tonnes per hectare:")
    for c in CROPS:
        print(f"  {c:<12} computed {par['weighted_means'][c]:.2f} | "
              f"foundation prints {FOUNDATION_WEIGHTED_MEANS[c]:.2f}")
    print("\nBaseline pattern, the real district pattern for 2020 to 2021,")
    print("hectares by governorate and crop (foundation Section 6).")
    print("Menoufia rice uses the delivered 2019 to 2020 published value")
    print("of 7.98 hectares for that one cell, flagged in RERUN_CHOICES.md.")
    base_frame = pd.DataFrame(
        {c: [par["baseline_x"][(d, c)] for d in DISTRICTS] for c in CROPS},
        index=DISTRICTS)
    print(base_frame.round(2).to_string())
    print(f"\nBaseline staple production at full water: "
          f"{par['baseline_staple_t']:,.0f} tons")
    print(f"Food floor at 90 percent: {0.90 * par['baseline_staple_t']:,.0f} tons "
          f"of staples per scenario")
    print("\nScenario budgets and probabilities in this parameter set.")
    print("Every budget rests on the expected anchor of 11.00 billion")
    print("cubic metres, which is a calibration (foundation Section 11).")
    for s in par["scenarios"]:
        print(f"  {s:<9} budget {par['budgets_bcm'][s]:.3f} billion cubic "
              f"metres | probability {par['prob'][s]:.2f}")


def guarantee_sweep(base_par: dict, title: str) -> dict:
    """The food floor at 90, 95 and 100 percent of baseline staple
    production. For each level: optimised expected margin,
    baseline expected margin, gain in pounds and percent, and
    margin per cubic metre for both plans. Margin per cubic
    metre is an average return, never a price. Prices are 2023
    levels and costs are 2016 to 2017 levels in every figure."""
    print(f"\n{title}")
    print("Margin per cubic metre below is an average return, never a price.")
    base = evaluate_plan(base_par, base_par["baseline_x"])
    out = {}
    for share in (0.90, 0.95, 1.00):
        par_f = dict(base_par)
        par_f["food_floor_t"] = share * base_par["baseline_staple_t"]
        model, variables = build_problem(
            par_f, par_f["scenarios"], food_floor=True, name="sweep")
        status = solve_model(model)
        label = f"Floor at {int(share * 100)} percent of baseline staple production"
        if status != "Optimal":
            print(f"  {label}: the floor CANNOT be held in every scenario "
                  f"(solve status {status}). No margin is reported for "
                  f"this level.")
            out[share] = {"status": status, "held": False}
            continue
        res = scenario_results(par_f, model, variables)
        gain = res["margin"] - base["margin"]
        gain_pct = 100.0 * gain / base["margin"]
        opt_per_m3 = res["margin"] / res["water_m3"]
        base_per_m3 = base["margin"] / base["water_m3"]
        print(f"  {label}:")
        print(f"    Optimised expected margin: EGP {res['margin']:,.0f}")
        print(f"    Baseline expected margin:  EGP {base['margin']:,.0f}")
        print(f"    Gain: EGP {gain:,.0f} ({gain_pct:.2f} percent)")
        print(f"    Margin per cubic metre, optimised: EGP {opt_per_m3:.2f} "
              f"(average return)")
        print(f"    Margin per cubic metre, baseline:  EGP {base_per_m3:.2f} "
              f"(average return)")
        out[share] = {"status": status, "held": True, "opt": res["margin"],
                      "base": base["margin"], "gain": gain,
                      "gain_pct": gain_pct, "opt_per_m3": opt_per_m3,
                      "base_per_m3": base_per_m3}
    return out


def headline(par: dict, title: str) -> dict:
    """Optimised plan against the baseline pattern at the 90
    percent floor under one parameter set. Prices are 2023
    levels and costs are 2016 to 2017 levels in every figure."""
    print(f"\n{title}")
    model, variables, status, floor_held = build_stochastic_model(par)
    print(f"Stochastic model status: {status}; food floor held: {floor_held}")
    res = scenario_results(par, model, variables)
    base = evaluate_plan(par, par["baseline_x"])
    gain = res["margin"] - base["margin"]
    print(f"  Optimised expected margin: EGP {res['margin']:,.0f}")
    print(f"  Baseline expected margin:  EGP {base['margin']:,.0f}")
    print(f"  Gain: EGP {gain:,.0f} ({100.0 * gain / base['margin']:.2f} percent)")
    print(f"  Optimised expected staple output: {res['staple_t']:,.0f} tons")
    print(f"  Baseline expected staple output:  {base['staple_t']:,.0f} tons")
    print(f"  Margin per cubic metre, optimised: "
          f"EGP {res['margin'] / res['water_m3']:.2f} (average return, never a price)")
    print(f"  Margin per cubic metre, baseline:  "
          f"EGP {base['margin'] / base['water_m3']:.2f} (average return, never a price)")
    return {"res": res, "base": base, "gain": gain, "floor_held": floor_held,
            "status": status}


def sensitivity_report(par: dict) -> list:
    """Version 2 style sensitivity swings. Each swing reevaluates
    the baseline under the same moved parameters. Prices are
    2023 levels and costs are 2016 to 2017 levels."""
    rows = []

    def record(label, par_mod):
        out = gain_under(par_mod)
        if out is None:
            rows.append((label, None))
            print(f"  {label:<42} solve not optimal")
            return
        rows.append((label, out))
        print(f"  {label:<42} gain EGP {out['gain']:>16,.0f} "
              f"({out['gain_pct']:6.2f} percent) | floor held: {out['floor_held']}")

    record("Base case", par)
    for crop in ("Rice", "Potatoes"):
        for factor in (0.8, 1.2):
            pm = dict(par)
            pm["price"] = dict(par["price"])
            pm["price"][crop] = par["price"][crop] * factor
            record(f"{crop} price times {factor}", pm)
    for factor in (0.8, 1.2):
        pm = dict(par)
        pm["price"] = dict(par["price"])
        for crop in ("Rice", "Potatoes"):
            pm["price"][crop] = par["price"][crop] * factor
        record(f"Rice and potatoes prices times {factor}", pm)
    for factor in (0.8, 1.2):
        pm = dict(par)
        pm["cost"] = {c: par["cost"][c] * factor for c in CROPS}
        record(f"All production costs times {factor}", pm)
    for factor in (0.95, 1.05):
        pm = dict(par)
        pm["water_budget"] = {
            k: v * factor for k, v in par["water_budget"].items()
        }
        record(f"All water budgets times {factor}", pm)
    return rows


def stress_runs(par: dict, res: dict) -> dict:
    """Stress runs at 10 and 20 percent water cuts, with the
    version 2 honest reporting when the floor cannot be held.
    Prices are 2023 levels and costs are 2016 to 2017 levels."""
    print("\nStress runs, stochastic model rebuilt at reduced budgets:")
    stress_out = {}
    model, variables, status, floor_held = build_stochastic_model(par)
    base_district_margin = district_margins(par, variables, "expected")
    base_district_staples = district_staples(par, variables, "expected")
    for cut in (0.10, 0.20):
        s_model, s_vars, s_status, s_floor = build_stochastic_model(
            par, water_scale=1.0 - cut)
        s_res = scenario_results(par, s_model, s_vars)
        s_district_margin = district_margins(par, s_vars, "expected")
        drops = {
            d: base_district_margin[d] - s_district_margin[d] for d in DISTRICTS
        }
        worst = max(drops, key=drops.get)
        entry = {
            "status": s_status, "floor_held": s_floor, "res": s_res,
            "worst_district": worst, "worst_drop_egp": drops[worst],
        }
        print(f"\n  Water cut {int(cut * 100)} percent (status {s_status}, "
              f"food floor held: {s_floor}):")
        if s_floor:
            print(f"    Expected margin:        EGP {s_res['margin']:,.0f} "
                  f"(change {s_res['margin'] - res['margin']:,.0f})")
            print(f"    Expected staple output: {s_res['staple_t']:,.0f} tons "
                  f"(change {s_res['staple_t'] - res['staple_t']:,.0f})")
            print(f"    District absorbing the largest margin loss: {worst} "
                  f"(EGP {drops[worst]:,.0f} in the expected scenario)")
        else:
            s_district_staples = district_staples(par, s_vars, "expected")
            staple_drops = {
                d: base_district_staples[d] - s_district_staples[d]
                for d in DISTRICTS
            }
            worst_food = max(staple_drops, key=staple_drops.get)
            entry["worst_food_district"] = worst_food
            entry["worst_food_drop_t"] = staple_drops[worst_food]
            print(f"    The food floor CANNOT be held at this cut. "
                  f"Staple output falls to {s_res['staple_t']:,.0f} tons, "
                  f"which is {s_res['staple_t'] / par['food_floor_t'] * 100:.0f} "
                  f"percent of the floor.")
            print(f"    Margin without the floor is EGP {s_res['margin']:,.0f} "
                  f"and is NOT comparable to the floored runs, because it "
                  f"is bought by cutting food production.")
            print(f"    District absorbing the largest staple loss: "
                  f"{worst_food} ({staple_drops[worst_food]:,.0f} tons in "
                  f"the expected scenario)")
        stress_out[cut] = entry
    return stress_out


def main_run(par: dict) -> dict:
    """The main stochastic run at the 90 percent floor: planting
    plan, water coverage table, shadow price tables in both
    units, both dual verifications, baseline evaluation and
    information values. Prices are 2023 levels and costs are
    2016 to 2017 levels in every figure."""
    model, variables, status, floor_held = build_stochastic_model(par)
    print(f"\nStochastic model status: {status}; food floor held: {floor_held}")
    res = scenario_results(par, model, variables)
    x_opt = plan_from_variables(variables)
    print("\nOptimised plan, expected values across scenarios:")
    print(f"  Expected margin:        EGP {res['margin']:,.0f}")
    print(f"  Expected staple output: {res['staple_t']:,.0f} tons")
    print(f"  Expected water use:     {res['water_m3'] / 1e9:.3f} billion cubic metres")
    for s in par["scenarios"]:
        r = res["per_scenario"][s]
        print(f"  Scenario {s:<9} margin EGP {r['margin']:,.0f} | "
              f"staples {r['staple_t']:,.0f} t | water {r['water_m3'] / 1e9:.3f} BCM")
    print("\nPlanting plan, hectares by district and crop:")
    plan_frame = pd.DataFrame(
        {c: [x_opt[(d, c)] for d in DISTRICTS] for c in CROPS}, index=DISTRICTS
    )
    print(plan_frame.round(0).to_string())
    print("\nWater coverage, share of the agronomic requirement delivered:")
    print(water_coverage(par, variables).round(3).to_string())
    print("A share of zero means the plan writes that crop off in that "
          "scenario: hectares planted, cost sunk, nothing harvested.")
    shadow = extract_shadow_prices(model, par)
    print("\nWater shadow prices, raw duals of the stochastic model, "
          "Egyptian pounds per cubic metre of expected margin:")
    print(shadow.pivot(index="district", columns="scenario",
                       values="shadow_price_egp_m3").round(3).to_string())
    print("\nWater values inside each scenario, raw dual divided by the "
          "scenario probability, Egyptian pounds per cubic metre:")
    print(shadow.pivot(index="district", columns="scenario",
                       values="conditional_egp_m3").round(2).to_string())
    print("Both tables report duals, that is marginal values. Menoufia "
          "rice multiplier is a neutral fill of 1.00 for an unreported "
          "cell (foundation Sections 6 and 7), so read the Menoufia "
          "row with that flag in mind.")
    check = dual_check(par)
    print(f"\nDual verification, deterministic model, Dakahlia expected "
          f"scenario: solver dual {check['dual']:.3f} EGP per cubic metre; "
          f"brute force bump implies {check['implied_by_bump']:.3f}; close "
          f"agreement expected, exact equality is not, because a finite "
          f"bump crosses kink points.")
    scheck = dual_check_stochastic(par)
    print(f"Dual verification, stochastic model, Dakahlia expected "
          f"scenario: reported raw dual {scheck['dual']:.3f}; brute force "
          f"bump inside the stochastic model implies "
          f"{scheck['implied_by_bump']:.3f}.")
    base = evaluate_plan(par, par["baseline_x"])
    base_demand = sum(
        par["baseline_x"][(d, c)] * par["water_req"][c]
        for d in DISTRICTS for c in CROPS
    )
    budget_expected = par["budgets_bcm"]["expected"] * 1e9
    print("\nBaseline, the real district pattern in the same data:")
    print(f"  Water demand at full watering: {base_demand / 1e9:.3f} BCM "
          f"against an expected budget of {budget_expected / 1e9:.2f} BCM. "
          f"The budget is a calibration (foundation Section 11).")
    print(f"  Expected margin:        EGP {base['margin']:,.0f}")
    print(f"  Expected staple output: {base['staple_t']:,.0f} tons")
    print(f"  Expected water use:     {base['water_m3'] / 1e9:.3f} BCM")
    print(f"  Margin per cubic metre: EGP {base['margin'] / base['water_m3']:.2f} "
          f"baseline against EGP {res['margin'] / res['water_m3']:.2f} optimised. "
          f"Margin per cubic metre is an average return, never a price.")
    margin_gain = res["margin"] - base["margin"]
    print(f"  HEADLINE: optimised minus baseline expected margin = "
          f"EGP {margin_gain:,.0f} ({margin_gain / base['margin'] * 100:.2f} percent)")
    if margin_gain <= 0:
        print("  FALSIFICATION RULE: the optimised plan does NOT beat the "
              "current pattern. The thesis fails on this data and the "
              "results note must say so.")
    stress_out = stress_runs(par, res)
    info = information_values(par)
    print("\nInformation values (prices at 2023 levels, costs at 2016 to "
          "2017 levels):")
    bad_ws = [s for s, st in info["ws_status"].items() if st != "Optimal"]
    if bad_ws:
        print(f"  WARNING: wait and see solves not optimal for {bad_ws}; "
              f"the wait and see value and EVPI are unreliable.")
    else:
        print(f"  Wait and see statuses: all Optimal "
              f"({info['ws_status']})")
    print(f"  Recourse (stochastic) value: EGP {info['recourse_value_egp']:,.0f}")
    print(f"  Wait and see value:          EGP {info['wait_and_see_egp']:,.0f}")
    print(f"  EVPI:                        EGP {info['evpi_egp']:,.0f}")
    if info["eev_egp"] is not None:
        print(f"  Expected result of planning on the average year: "
              f"EGP {info['eev_egp']:,.0f}")
        print(f"  VSS:                         EGP {info['vss_egp']:,.0f}")
    else:
        print(f"  Planning on the average year CANNOT keep the food floor "
              f"in scenario(s): {', '.join(info['eev_floor_breach'])}. "
              f"Scored without the floor it would reach "
              f"EGP {info['eev_upper_bound_egp']:,.0f}, an upper bound "
              f"that flatters it. VSS is therefore not a single number "
              f"in this version.")
    return {"res": res, "base": base, "shadow": shadow, "stress": stress_out,
            "info": info, "x_opt": x_opt, "floor_held": floor_held}


def run_variant(beet_label: str) -> dict:
    """Run the full run set for one sugar beet price variant."""
    beet_price = BEET_PRICE_VARIANTS[beet_label]
    par = build_parameter_set(beet_price)
    print_parameters(par, beet_label)
    main = main_run(par)
    sweep = guarantee_sweep(
        par,
        "GUARANTEE SWEEP, sugar beet at EGP {:,.0f} per tonne. The food "
        "floor at 90, 95 and 100 percent of baseline staple "
        "production.".format(beet_price))
    out = {"par": par, "main": main, "sweep": sweep}
    if beet_label == "beet795":
        wheat_par = build_parameter_set(
            beet_price, wheat_price=WHEAT_PROCUREMENT_2025_EGP_TON)
        out["wheat_sweep"] = guarantee_sweep(
            wheat_par,
            "WHEAT PROCUREMENT VARIANT, beet795 set. Wheat at EGP "
            "14,667 per tonne, the confirmed 2025 procurement anchor "
            "(foundation Section 3); sugar beet stays at EGP 795 per "
            "tonne; everything else held equal.")
        net_req = dict(WATER_REQ_NET_M3_HA)
        net_par = build_parameter_set(beet_price, water_req=net_req)
        print("\nNET WATER BASIS RUN, beet795 set. Water requirements "
              "on the net basis, Gabr 2022 (foundation Section 8).")
        print("Flag from foundation Section 8: the Gabr wheat net row is "
              "internally inconsistent with the same paper tables for its "
              "other territories, and the row is used here as published, "
              "with that flag attached.")
        for c in CROPS:
            print(f"  {c:<12} net requirement {net_req[c]:>10,.0f} cubic "
                  f"metres per hectare")
        out["net_headline"] = headline(
            net_par, "Net basis headline at the 90 percent floor:")
        out["net_sweep"] = guarantee_sweep(
            net_par, "Net basis guarantee sweep:")
        print("Flag repeated at the end of the net case: the wheat net "
              "requirement of 1,272 cubic metres per hectare carries the "
              "foundation Section 8 flag of internal inconsistency.")
        derivb_par = build_parameter_set(
            beet_price, prob=DERIVATION_B_PROB, mult=DERIVATION_B_MULT)
        print("\nDERIVATION B RUN, beet795 set. Scenario probabilities "
              "0.33, 0.34 and 0.33 with budget multipliers 0.811, 0.973 "
              "and 1.217 (foundation Section 10, Derivation B), on the "
              "same calibration anchor of 11.00 billion cubic metres "
              "(foundation Section 11).")
        for s in derivb_par["scenarios"]:
            print(f"  {s:<9} budget {derivb_par['budgets_bcm'][s]:.3f} "
                  f"billion cubic metres | probability "
                  f"{derivb_par['prob'][s]:.2f}")
        out["derivb_headline"] = headline(
            derivb_par, "Derivation B headline at the 90 percent floor:")
        out["derivb_sweep"] = guarantee_sweep(
            derivb_par, "Derivation B guarantee sweep:")
        print("\nSensitivity runs (the gain is the optimised margin minus "
              "the baseline margin, both under the same moved parameters; "
              "prices at 2023 levels, costs at 2016 to 2017 levels):")
        out["sensitivity"] = sensitivity_report(par)
    print(f"\nEnd of run for variant {beet_label}.")
    return out


if __name__ == "__main__":
    label = sys.argv[1] if len(sys.argv) > 1 else "beet795"
    if label not in BEET_PRICE_VARIANTS:
        raise SystemExit(f"Unknown variant {label}")
    run_variant(label)
