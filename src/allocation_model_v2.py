"""Problem One: allocation of land and water under uncertainty.

A two stage stochastic linear program. Stage one plants hectares
by crop and district before the inflow is known. Stage two
allocates water under the scenario that occurs. The objective is
expected farm margin, where a water shortfall cuts yield through
a published style yield response factor. Dual values on the
district water constraints are a primary output: they state the
money value of one more cubic metre of water in each district.

Version 1 data position, stated honestly. Yields and harvested
areas are real pulled data: FAOSTAT series republished by Our
World in Data, Egypt, means over 2014 to 2023, pulled 12 November
2026 after the FAOSTAT site itself failed with server errors.
Prices are Egyptian pounds per ton at 2025 levels. The wheat
price is the published government procurement price. The other
prices, all production costs, all crop water requirements, the
district land base and the district yield multipliers are
declared illustrative values inside published ranges, pending
the FAOSTAT prices pull, the CAPMAS district pull and the
extension guidance pull listed in data/SOURCES.md. Every printed
result carries the word illustrative for this reason.

Design reference: docs/design.md, Problem One section.

Version 2 changes, driven by the audit recorded in
paper/Audit_Log_v2.md. One: production is constrained to be
nonnegative for every planting and scenario, which closes the
region where the linear yield response form would otherwise
extrapolate below zero for crops with a response factor above
one. Two: shadow prices are reported in two labelled units,
the probability weighted dual of the extensive form and the
conditional value inside the scenario, because version one
reported the first while its prose described the second.
Three: the run prints a water coverage table by crop and
scenario, so a recourse that starves one crop completely is
visible instead of buried. Four: the sensitivity work the
design promised is part of the run: price and cost swings,
budget scaling, and a food floor curve that prices the staple
trade. Five: the dual verification now also runs inside the
stochastic model whose duals are actually reported.
"""

from pathlib import Path

import pandas as pd
import pulp

RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"

# ---------------------------------------------------------------- crops
# Crop order is fixed everywhere so tables stay readable.
CROPS = ["Wheat", "Rice", "Maize", "Sugar beet", "Potatoes"]
STAPLES = ["Wheat", "Rice", "Maize"]

# OWID grapher file stems per crop. The yield and production
# series together imply harvested area, which sets the real
# current crop mix used for the baseline pattern.
OWID_STEMS = {
    "Wheat": "wheat",
    "Rice": "rice",
    "Maize": "maize",
    "Sugar beet": "sugar-beet",
    "Potatoes": "potato",
}

# ------------------------------------------------------- declared values
# Producer prices, Egyptian pounds per ton, 2025 levels.
# Wheat is the published procurement price of 2,200 pounds per
# ardeb of 150 kilograms, which is 14,667 pounds per ton
# (USDA FAS Cairo, Grain and Feed Annual, and FAO GIEWS).
# The rest are illustrative midpoints of reported farm prices.
PRICE_EGP_TON = {
    "Wheat": 14_667.0,
    "Rice": 16_000.0,       # illustrative, paddy
    "Maize": 9_500.0,       # illustrative
    "Sugar beet": 2_500.0,  # illustrative, factory contract
    "Potatoes": 7_000.0,    # illustrative, farm gate, very variable
}

# Production cost, Egyptian pounds per hectare. Illustrative.
COST_EGP_HA = {
    "Wheat": 30_000.0,
    "Rice": 42_000.0,
    "Maize": 32_000.0,
    "Sugar beet": 36_000.0,
    "Potatoes": 95_000.0,
}

# Applied irrigation water requirement, cubic metres per hectare.
# Illustrative midpoints of published Delta ranges, pending the
# extension guidance pull. Rice is the heavy user, as published.
WATER_REQ_M3_HA = {
    "Wheat": 4_200.0,
    "Rice": 12_000.0,
    "Maize": 5_800.0,
    "Sugar beet": 5_200.0,
    "Potatoes": 4_800.0,
}

# Yield response factor: the share of yield lost when the share
# of water shortfall is one. Values follow the style of the FAO
# yield response factors. Used linearly, which is an approximation
# that the paper states openly.
YIELD_RESPONSE = {
    "Wheat": 1.00,
    "Rice": 1.20,
    "Maize": 1.25,
    "Sugar beet": 1.00,
    "Potatoes": 1.10,
}

# Largest share of district land any one crop may take, a rotation
# and market limit. Declared modelling device, stated in results.
CROP_CAP_SHARE = {
    "Wheat": 0.50,
    "Rice": 0.35,
    "Maize": 0.40,
    "Sugar beet": 0.30,
    "Potatoes": 0.15,
}

# ------------------------------------------------------------- districts
# Eight Delta governorates. Land is cropped hectares in thousands.
# Illustrative, pending the CAPMAS pull. Beheira is the largest
# Delta governorate by cropped area and Damietta the smallest,
# which matches published orders of magnitude.
DISTRICT_LAND_KHA = {
    "Beheira": 380.0,
    "Sharkia": 330.0,
    "Dakahlia": 300.0,
    "Kafr El Sheikh": 260.0,
    "Gharbia": 190.0,
    "Menoufia": 170.0,
    "Qalyubia": 150.0,
    "Damietta": 120.0,
}

# District yield multiplier on the national yield. Illustrative.
# The northern Delta loses yield to soil salinity, which is a
# published pattern; the southern Delta sits slightly above the
# national mean. Multipliers stay close to one on purpose.
DISTRICT_YIELD_MULT = {
    "Beheira": 1.00,
    "Sharkia": 1.02,
    "Dakahlia": 1.03,
    "Kafr El Sheikh": 0.90,
    "Gharbia": 1.04,
    "Menoufia": 1.05,
    "Qalyubia": 1.03,
    "Damietta": 0.92,
}

DISTRICTS = list(DISTRICT_LAND_KHA)

# ------------------------------------------------------------- scenarios
# Total seasonal water budget for the model area, billion cubic
# metres. The expected budget is calibrated just under the water
# demand of the current cropping pattern, which is the scarcity
# the Delta actually faces. Low and high scale it by published
# style inflow variability. Probabilities are declared judgment.
TOTAL_BUDGET_BCM = {"low": 9.35, "expected": 11.00, "high": 11.90}
SCENARIO_PROB = {"low": 0.25, "expected": 0.50, "high": 0.25}
SCENARIOS = list(TOTAL_BUDGET_BCM)

# The food floor: staple production in every scenario must reach
# at least this share of the staple production of the current
# pattern at full water. Declared policy parameter.
FOOD_FLOOR_SHARE = 0.90


def load_crop_facts() -> pd.DataFrame:
    """Read the pulled OWID files and return one row per crop.

    Columns: crop, yield in tons per hectare, and harvested area
    in hectares, both Egypt means over 2014 to 2023, plus the
    implied national production in tons.
    """
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


def build_parameter_set() -> dict:
    """Assemble every parameter the model needs, with provenance.

    Returns a dictionary. Anything not pulled from a data file is
    a module level declared value above, so a reader can audit
    each number in one place.
    """
    facts = load_crop_facts()
    total_land_ha = sum(DISTRICT_LAND_KHA.values()) * 1000.0
    total_area = facts["area_ha"].sum()

    # The baseline pattern: the real national crop mix, scaled to
    # the model land base and applied in every district. District
    # level pattern data is the CAPMAS pull, still owed.
    baseline_share = {c: float(facts.loc[c, "area_ha"] / total_area) for c in CROPS}
    baseline_x = {
        (d, c): baseline_share[c] * DISTRICT_LAND_KHA[d] * 1000.0
        for d in DISTRICTS
        for c in CROPS
    }

    # Staple production of the baseline at full water sets the
    # food floor. District multipliers apply, as in the model.
    baseline_staple_t = sum(
        baseline_x[(d, c)] * facts.loc[c, "yield_t_ha"] * DISTRICT_YIELD_MULT[d]
        for d in DISTRICTS
        for c in STAPLES
    )

    # District water budgets: shares of the scenario total follow
    # land shares. A declared simplification for version one.
    land_share = {d: DISTRICT_LAND_KHA[d] * 1000.0 / total_land_ha for d in DISTRICTS}
    water_budget = {
        (d, s): TOTAL_BUDGET_BCM[s] * 1e9 * land_share[d]
        for d in DISTRICTS
        for s in SCENARIOS
    }

    return {
        "facts": facts,
        "yield_t_ha": {c: float(facts.loc[c, "yield_t_ha"]) for c in CROPS},
        "price": PRICE_EGP_TON,
        "cost": COST_EGP_HA,
        "water_req": WATER_REQ_M3_HA,
        "ky": YIELD_RESPONSE,
        "cap_share": CROP_CAP_SHARE,
        "land_ha": {d: DISTRICT_LAND_KHA[d] * 1000.0 for d in DISTRICTS},
        "yield_mult": DISTRICT_YIELD_MULT,
        "water_budget": water_budget,
        "baseline_x": baseline_x,
        "baseline_share": baseline_share,
        "food_floor_t": FOOD_FLOOR_SHARE * baseline_staple_t,
        "baseline_staple_t": baseline_staple_t,
        "prob": SCENARIO_PROB,
    }


def production_expr(par: dict, d: str, c: str, x, w):
    """Linear production in tons for one planting in one scenario.

    Production equals the full water yield times one minus the
    yield response factor times the shortfall share. Written in x
    and w only, so it stays linear: the constant part rides on x
    and the recovered part rides on w.
    """
    y = par["yield_t_ha"][c] * par["yield_mult"][d]
    ky = par["ky"][c]
    req = par["water_req"][c]
    return y * (1.0 - ky) * x + (y * ky / req) * w


def build_problem(par: dict, scenario_names: list, water_scale: float = 1.0,
                  food_floor: bool = True, fixed_x: dict | None = None,
                  name: str = "allocation", floor_tolerance: float = 0.0) -> tuple:
    """Build one linear program over the given scenarios.

    Stage one variables are hectares by district and crop. Stage
    two variables are water delivered by district, crop and
    scenario. When fixed_x is given, planting is held at those
    values and only the water recourse is free, which is how the
    expected value of the expected solution is computed.
    Returns the problem and a dictionary of its variables.
    """
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

    # Objective: probability weighted revenue across scenarios,
    # minus planting cost, which is paid once in stage one.
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
                # Production can never be negative. The linear
                # yield response form crosses zero at a shortfall
                # share of one over the response factor, and for
                # factors above one it would extrapolate below
                # zero beyond that point. This constraint fences
                # the form at zero, which is where the agronomy
                # says production stops. Added in version two.
                prob_model += (
                    production_expr(par, d, c, x[(d, c)], w[(d, c, s)]) >= 0,
                    f"ProdFloor_{d}_{c}_{s}",
                )
    if food_floor:
        # The floor is one constraint per scenario across all
        # districts, so it is added outside the district loop.
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
    """Solve with the bundled CBC solver and return the status."""
    prob_model.solve(pulp.PULP_CBC_CMD(msg=False))
    return pulp.LpStatus[prob_model.status]


def build_deterministic_model(par: dict, scenario: str, water_scale: float = 1.0,
                              food_floor: bool = True) -> tuple:
    """Build and solve the single scenario linear program.

    This is the deterministic core the design ships first. It is
    also the building block for the wait and see value used by
    the information measures.
    """
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
    returned flag, because a floor that cannot be held under a
    water cut is itself a result.
    """
    prob_model, variables = build_problem(
        par, SCENARIOS, water_scale=water_scale, food_floor=food_floor,
        name="stochastic",
    )
    status = solve_model(prob_model)
    floor_held = food_floor
    if status != "Optimal" and food_floor:
        prob_model, variables = build_problem(
            par, SCENARIOS, water_scale=water_scale, food_floor=False,
            name="stochastic_nofloor",
        )
        status = solve_model(prob_model)
        floor_held = False
    return prob_model, variables, status, floor_held


def evaluate_plan(par: dict, x_values: dict, water_scale: float = 1.0,
                  food_floor: bool = False) -> dict:
    """Evaluate one fixed planting plan across all scenarios.

    Solves only the water recourse for each scenario with the
    planting held fixed, and returns expected margin, expected
    staple production in tons, and expected water use in cubic
    metres. With food_floor set, the floor is imposed in every
    scenario; a scenario the fixed plan cannot satisfy is
    reported with its status and no numbers, because a plan
    that breaks the food rule in a dry year must not be scored
    as if it had kept it.
    """
    out = {"margin": 0.0, "staple_t": 0.0, "water_m3": 0.0, "per_scenario": {},
           "all_feasible": True}
    for s in SCENARIOS:
        # The planting is fixed by bounding every stage one
        # variable to the plan value, so only water is free.
        # A plan that keeps the floor sits exactly on it, so a
        # one part in a million tolerance keeps solver rounding
        # from misreporting a kept promise as a broken one. On a
        # floor near eleven million tons this is about eleven
        # tons, which is immaterial and stated here openly.
        prob_model, variables = build_problem(
            par, [s], water_scale=water_scale, food_floor=food_floor,
            name=f"eval_{s}", floor_tolerance=1e-6,
        )
        for k, var in variables["x"].items():
            var.lowBound = x_values[k]
            var.upBound = x_values[k]
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


def extract_shadow_prices(solved_model, scenario_names: list | None = None,
                          probs: dict | None = None) -> pd.DataFrame:
    """Return the water value map from a solved model.

    One row per district and scenario, in two labelled units.
    The column shadow_price_egp_m3 is the raw dual on the
    district water constraint. In the extensive form the
    objective weights each scenario by its probability, so the
    raw dual is the change in expected margin from one more
    cubic metre delivered in that scenario. The column
    conditional_egp_m3 divides the raw dual by the scenario
    probability and gives the value of one more cubic metre
    inside that scenario, which is the number a planner means
    by the value of water in a dry year. Version one reported
    the raw dual while its prose described the conditional
    value. Both are correct numbers; they answer different
    questions, and version two labels them apart.

    CBC reports duals on the constraint as built; for a
    maximisation with a less than or equal water limit the
    reported value is negative, and its size is the value of
    one more cubic metre, so the table reports the size.
    """
    names = scenario_names or SCENARIOS
    # PuLP replaces spaces in constraint names with underscores,
    # so district names are matched back through this lookup.
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
                if probs is not None:
                    total = sum(probs[t] for t in names)
                    row["conditional_egp_m3"] = raw / (probs[s] / total)
                rows.append(row)
    frame = pd.DataFrame(rows)
    return frame.sort_values(["district", "scenario"]).reset_index(drop=True)


def plan_from_variables(variables: dict) -> dict:
    """Read stage one hectares out of a solved model."""
    return {k: float(v.value()) for k, v in variables["x"].items()}


def scenario_results(par: dict, prob_model, variables: dict) -> dict:
    """Per scenario margin, staple production and water use of a
    solved stochastic model, plus expected values."""
    out = {"per_scenario": {}, "margin": 0.0, "staple_t": 0.0, "water_m3": 0.0}
    planted_cost = sum(
        par["cost"][c] * float(variables["x"][(d, c)].value())
        for d in DISTRICTS for c in CROPS
    )
    for s in SCENARIOS:
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
    """Margin by district under one scenario of a solved model."""
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
    """Staple production in tons by district under one scenario."""
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
    stochastic solution, in Egyptian pounds.

    Wait and see value: plant after seeing the scenario, averaged.
    Recourse value: the stochastic optimum. Expected result of
    the expected value solution: plant for the expected scenario,
    then face all scenarios. EVPI is wait and see minus recourse.
    VSS is recourse minus that expected result.
    """
    rp_model, _vars_rp, status_rp, _floor = build_stochastic_model(par)
    rp = pulp.value(rp_model.objective) if status_rp == "Optimal" else float("nan")

    ws = 0.0
    ws_status = {}
    for s in SCENARIOS:
        det_model, _, status = build_deterministic_model(par, s)
        ws_status[s] = status
        if status != "Optimal":
            # A wait and see term that cannot be solved must be
            # named, never silently zeroed. Version two records
            # the status; the run prints it.
            ws += 0.0
        else:
            ws += par["prob"][s] * pulp.value(det_model.objective)

    det_exp, vars_exp, status_exp = build_deterministic_model(par, "expected")
    x_exp = plan_from_variables(vars_exp)

    # The expected result of the average year plan must be scored
    # under the same rules as the stochastic plan, food floor
    # included. If that plan cannot keep the floor in some
    # scenario, the honest finding is the breach itself, and any
    # margin scored without the floor is only an upper bound
    # that flatters the average year plan.
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
        s for s in SCENARIOS
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
    """Verify one shadow price by brute force.

    Rebuilds the expected scenario model with the district water
    budget raised by the bump share, and compares the objective
    change per cubic metre against the reported dual value.
    """
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
    delivered, by crop and scenario, aggregated over districts.

    Version one never printed this table, and its plan starved
    one crop completely in the dry scenario without the run
    output saying so. A recourse that writes a crop off must be
    visible in the results, not discovered by an auditor.
    """
    rows = []
    for c in CROPS:
        row = {"crop": c}
        for s in SCENARIOS:
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
                          bump: float = 0.01) -> dict:
    """Verify one reported stochastic dual by brute force.

    Raises the district budget in one scenario inside the full
    stochastic model and compares the change in expected margin
    per cubic metre against the raw dual the run reports.
    Version one verified its duals only inside a deterministic
    model whose duals it did not report.
    """
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
    modified parameter set. The baseline is reevaluated under
    the same parameters, as the design requires."""
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


def sensitivity_report(par: dict) -> list:
    """The sensitivity work the design promises, as printed
    rows. Price swings of twenty percent on the two highest
    margin crops, joint price swings, joint cost swings,
    budget scaling, and the food floor curve that prices the
    staple trade. Returns the rows it prints.
    """
    rows = []

    def record(label, par_mod):
        out = gain_under(par_mod)
        if out is None:
            rows.append((label, None))
            print(f"  {label:<38} solve not optimal")
            return
        rows.append((label, out))
        print(f"  {label:<38} gain EGP {out['gain']:>16,.0f} "
              f"({out['gain_pct']:6.2f} percent)")

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
    for share in (0.95, 1.00):
        pm = dict(par)
        pm["food_floor_t"] = share * par["baseline_staple_t"]
        record(f"Food floor at {share:.2f} of current staples", pm)
    return rows


def run_all() -> dict:
    """Run the full version two pipeline and print every result.

    Prints carry the word illustrative because most money and
    water parameters are declared values pending the pulls listed
    in data/SOURCES.md. Yields, areas and the crop mix are real.
    """
    par = build_parameter_set()
    facts = par["facts"]
    print("=" * 72)
    print("PROBLEM ONE, VERSION 2 RUN (illustrative money parameters)")
    print("=" * 72)
    print("\nPulled crop facts, Egypt means 2014 to 2023 (FAOSTAT via OWID):")
    print(facts.round(2).to_string())
    print("\nBaseline crop mix shares from real harvested areas:")
    for c in CROPS:
        print(f"  {c:<12} {par['baseline_share'][c] * 100:5.1f} percent")
    print(f"\nFood floor: {par['food_floor_t']:,.0f} tons of staples per scenario")
    print(f"(90 percent of baseline staple production {par['baseline_staple_t']:,.0f} tons)")

    # ------------------------------------------------ stochastic solution
    model, variables, status, floor_held = build_stochastic_model(par)
    print(f"\nStochastic model status: {status}; food floor held: {floor_held}")
    res = scenario_results(par, model, variables)
    x_opt = plan_from_variables(variables)
    print("\nOptimised plan, expected values across scenarios:")
    print(f"  Expected margin:        EGP {res['margin']:,.0f}")
    print(f"  Expected staple output: {res['staple_t']:,.0f} tons")
    print(f"  Expected water use:     {res['water_m3'] / 1e9:.3f} billion cubic metres")
    for s in SCENARIOS:
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

    # ------------------------------------------------------- shadow prices
    shadow = extract_shadow_prices(model, probs=par["prob"])
    print("\nWater shadow prices, raw duals of the stochastic model, "
          "Egyptian pounds per cubic metre of expected margin (illustrative):")
    print(shadow.pivot(index="district", columns="scenario",
                       values="shadow_price_egp_m3").round(3).to_string())
    print("\nWater values inside each scenario, raw dual divided by the "
          "scenario probability, Egyptian pounds per cubic metre (illustrative):")
    print(shadow.pivot(index="district", columns="scenario",
                       values="conditional_egp_m3").round(2).to_string())
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

    # ------------------------------------------------------------- baseline
    base = evaluate_plan(par, par["baseline_x"])
    base_demand = sum(
        par["baseline_x"][(d, c)] * par["water_req"][c]
        for d in DISTRICTS for c in CROPS
    )
    budget_expected = TOTAL_BUDGET_BCM["expected"] * 1e9
    print("\nBaseline, the current pattern in the same data:")
    print(f"  Water demand at full watering: {base_demand / 1e9:.3f} BCM "
          f"against an expected budget of {budget_expected / 1e9:.2f} BCM")
    print(f"  Expected margin:        EGP {base['margin']:,.0f}")
    print(f"  Expected staple output: {base['staple_t']:,.0f} tons")
    print(f"  Expected water use:     {base['water_m3'] / 1e9:.3f} BCM")
    print(f"  Margin per cubic metre: EGP {base['margin'] / base['water_m3']:.2f} "
          f"baseline against EGP {res['margin'] / res['water_m3']:.2f} optimised")
    margin_gain = res["margin"] - base["margin"]
    print(f"  HEADLINE: optimised minus baseline expected margin = "
          f"EGP {margin_gain:,.0f} ({margin_gain / base['margin'] * 100:.1f} percent)")
    if margin_gain <= 0:
        print("  FALSIFICATION RULE: the optimised plan does NOT beat the "
              "current pattern. The thesis fails on this data and the "
              "results note must say so.")

    # --------------------------------------------------------------- stress
    print("\nStress runs, stochastic model rebuilt at reduced budgets:")
    stress_out = {}
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
            # With the floor dropped the margin is not comparable:
            # the solver buys margin back by cutting food. The
            # honest stress answer is the size of the food breach
            # and where it lands.
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

    # ---------------------------------------------------- information values
    info = information_values(par)
    print("\nInformation values (illustrative money parameters):")
    bad_ws = [s for s, st in info["ws_status"].items() if st != "Optimal"]
    if bad_ws:
        print(f"  WARNING: wait and see solves not optimal for {bad_ws}; "
              f"the wait and see value and EVPI are unreliable.")
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
              f"in this version: the stochastic plan keeps a promise "
              f"the average year plan breaks.")

    # ------------------------------------------------------------ sensitivity
    print("\nSensitivity runs (the gain is the optimised margin minus the "
          "baseline margin, both under the same moved parameters):")
    sens = sensitivity_report(par)

    return {
        "par": par, "res": res, "base": base, "shadow": shadow,
        "stress": stress_out, "info": info, "x_opt": x_opt,
        "floor_held": floor_held, "sensitivity": sens,
    }


if __name__ == "__main__":
    run_all()
