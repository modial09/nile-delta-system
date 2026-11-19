"""Methods for the allocation model: Monte Carlo testing, the ten year backtest,
and the break even sensitivity.

Monte Carlo and backtest share one evaluation. A fixed plan (the
capped plan at the headline cover level, saved by the caps mode of
allocation_model) is replayed under one historical year at a
time. The year supplies two things: a yield multiplier per crop
group, the national yield of that year divided by the national
yield of 2021, the panel year of the district yields; and a price
vector, the farm gate prices of that year scaled by one deflator,
the 2025 wheat forecast price divided by the wheat price of that
year, so relative prices of the drawn year are preserved and the
level sits on 2025. Rice and sugar beet prices are missing for
2019 to 2021 in the source; for those years the nearest observed
year price is carried, and the log says so. Water is held at the
reference water state (normal storage, normal inflow) so the test
isolates price and yield history. Two readings per year: the wheat
capacity of the fixed plan under wheat maximising recourse, and
the delivered margin and wheat under margin seeking recourse.

The Monte Carlo draws whole years with replacement from 2015 to
2024, seed 20261116, 200 draws. The backtest runs the same ten
years in order, for the chosen plan and for the historical pattern.

The break even sensitivity perturbs one input at a time around the
capped frontier at the headline level and ranks the inputs by the
change they cause in the guarantee cost. For the strongest input
it then searches for the break even change at which the guarantee
cost falls to half its base value.

Usage:
  .venv/bin/python src/methods.py mc
  .venv/bin/python src/methods.py backtest
  .venv/bin/python src/methods.py breakeven
"""

import json
import random
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import pulp

sys.path.insert(0, str(Path(__file__).resolve().parent))
import allocation_model as m

BASE_DIR = m.BASE_DIR
EXT_DIR = m.EXT_DIR
PROC_DIR = m.PROC_DIR
REF_WATER = ("normal", "normal")
REF_SCENARIO = (REF_WATER, "expected")
YEARS = list(range(2015, 2025))
RESULTS = {}


def headline_cover():
    """The highest feasible capped cover level, from the caps run."""
    data = json.loads((PROC_DIR / "results_caps.json").read_text())
    fr = data["frontier_caps"]
    feas = [float(k) for k, v in fr.items() if v is not None]
    return max(feas)


def load_history():
    crops = pd.read_csv(EXT_DIR / "faostat_crops_egypt.csv")
    prices = pd.read_csv(EXT_DIR / "faostat_producer_prices_egypt_dec2025.csv")
    prices = prices[prices["unit"] == "EGP per tonne"]
    yld = {}
    for g in ["wheat", "rice_paddy", "maize", "sugar_beet", "potatoes"]:
        sub = crops[(crops["crop"] == g) & (crops["element"] == "Yield")]
        yld[g] = dict(zip(sub["year"].astype(int), sub["value"].astype(float)))
    pri = {}
    for g in ["wheat", "rice_paddy", "maize", "sugar_beet", "potatoes"]:
        sub = prices[prices["crop"] == g]
        pri[g] = dict(zip(sub["year"].astype(int), sub["price"].astype(float)))
    return yld, pri


def nearest_price(pri_g, year):
    if year in pri_g:
        return pri_g[year], year
    cand = sorted(pri_g.keys(), key=lambda y: (abs(y - year), y))
    return pri_g[cand[0]], cand[0]


def year_overrides(par, yld, pri, year):
    """Price and yield overrides that replay one historical year."""
    mult = {}
    for g in ["wheat", "rice_paddy", "maize", "sugar_beet", "potatoes"]:
        mult[g] = yld[g][year] / yld[g][2021]
    mult["berseem"] = mult["wheat"]
    deflator = par["price_forecast"]["wheat"]["forecast"] / pri["wheat"][year]
    price_o, carried = {}, {}
    for c in m.ALL_CROPS:
        if c == "Berseem":
            mp, used = nearest_price(pri["maize"], year)
            price_o[c] = {l: m.BERSEEM_FEED_RATIO * mp * deflator for l in m.LAYER_STATES}
            if used != year:
                carried[c] = used
            continue
        p, used = nearest_price(pri[m.GROUP[c]], year)
        price_o[c] = {l: p * deflator for l in m.LAYER_STATES}
        if used != year:
            carried[c] = used
    yield_o = {}
    for c in m.ALL_CROPS:
        yield_o[c] = {l: {d: par["yield"][c]["expected"][d] * mult[m.GROUP[c]]
                          for d in m.DISTRICTS} for l in m.LAYER_STATES}
    return price_o, yield_o, carried


def replay_year(par, plan, yld, pri, year):
    """Both readings of one fixed plan under one historical year."""
    price_o, yield_o, carried = year_overrides(par, yld, pri, year)
    prob_c, v_c = m.build(par, fixed=plan, objective="maxstaple",
                          single_scenario=REF_SCENARIO,
                          price_override=price_o, yield_override=yield_o)
    st_c = m.solve(prob_c, timelimit=300)
    wheat_cap = float(v_c["t"].value()) if st_c == "Optimal" else None
    prob_m, v_m = m.build(par, fixed=plan, single_scenario=REF_SCENARIO,
                          price_override=price_o, yield_override=yield_o)
    st_m = m.solve(prob_m, timelimit=300)
    margin, wheat_del = None, None
    if st_m == "Optimal":
        rev = sum(price_o[c]["expected"] * float(pulp.value(v_m["prod"][(d, c, REF_SCENARIO)]))
                  for d in m.DISTRICTS for c in m.ALL_CROPS)
        cst = sum(par["cost"][c] * plan["winter"][(d, c)] for d in m.DISTRICTS for c in m.WINTER_CROPS)
        cst += sum(par["cost"][c] * plan["summer"][(d, c, REF_WATER)]
                   for d in m.DISTRICTS for c in m.LATE_CROPS)
        margin = rev - cst
        wheat_del = sum(float(pulp.value(v_m["prod"][(d, "Wheat", REF_SCENARIO)]))
                        for d in m.DISTRICTS)
    return {"year": year, "wheat_capacity_t": wheat_cap,
            "delivery_margin": margin, "delivery_wheat_t": wheat_del,
            "carried_prices": carried}


def mc_mode(n_draws=200):
    par = m.load_all()
    yld, pri = load_history()
    cover = headline_cover()
    pct = int(round(cover * 100))
    plan, _ = m.load_plan(PROC_DIR / f"plan_caps_cover{pct}.csv")
    floor_t = cover * m.WHEAT_CONSUMPTION_T
    print(f"MONTE CARLO: capped plan at {cover*100:.0f} percent cover "
          f"(floor {floor_t:,.0f} tonnes of wheat), {n_draws} whole year "
          f"draws from 2015 to 2024, seed 20261116, water at the reference state")
    rng = random.Random(20261116)
    rows = []
    for n in range(n_draws):
        year = rng.choice(YEARS)
        r = replay_year(par, plan, yld, pri, year)
        r["draw"] = n
        rows.append(r)
        if n % 40 == 0:
            print(f"  draw {n} (year {year}) done")
    df = pd.DataFrame(rows)
    df.to_csv(PROC_DIR / "montecarlo_samples.csv", index=False)
    cap = df["wheat_capacity_t"].dropna()
    dwt = df["delivery_wheat_t"].dropna()
    mar = df["delivery_margin"].dropna()
    print(f"Draws solved: capacity {len(cap)}, delivery {len(dwt)} of {n_draws}")
    print(f"Wheat capacity of the fixed plan: share of draws holding the floor "
          f"{100*(cap >= floor_t).mean():.1f} percent | percentiles in tonnes: "
          f"10th {cap.quantile(0.10):,.0f}, median {cap.median():,.0f}, 90th {cap.quantile(0.90):,.0f}")
    print(f"Delivered wheat under margin seeking recourse: share of draws at or above "
          f"the floor {100*(dwt >= floor_t).mean():.1f} percent | median {dwt.median():,.0f} tonnes")
    print(f"Delivered margin: 10th percentile {mar.quantile(0.10):,.0f}, median "
          f"{mar.median():,.0f}, 90th percentile {mar.quantile(0.90):,.0f} pounds")
    RESULTS["montecarlo"] = {
        "cover": cover, "floor_t": floor_t, "n_draws": n_draws,
        "capacity_hold_share": float((cap >= floor_t).mean()),
        "capacity_p10": float(cap.quantile(0.10)), "capacity_median": float(cap.median()),
        "capacity_p90": float(cap.quantile(0.90)),
        "delivery_hold_share": float((dwt >= floor_t).mean()),
        "delivery_wheat_median": float(dwt.median()),
        "margin_p10": float(mar.quantile(0.10)), "margin_median": float(mar.median()),
        "margin_p90": float(mar.quantile(0.90))}
    save()


def backtest_mode():
    par = m.load_all()
    yld, pri = load_history()
    cover = headline_cover()
    pct = int(round(cover * 100))
    plan, _ = m.load_plan(PROC_DIR / f"plan_caps_cover{pct}.csv")
    pattern = {"winter": {(d, c): par["baseline"][c][d] for d in m.DISTRICTS for c in m.WINTER_CROPS},
               "summer": {(d, c, w): par["baseline"][c][d] for d in m.DISTRICTS
                          for c in m.LATE_CROPS for w in m.WATER_STATES}}
    floor_t = cover * m.WHEAT_CONSUMPTION_T
    print(f"BACKTEST: the actual years 2015 to 2024 in order, water at the "
          f"reference state, floor {floor_t:,.0f} tonnes (cover {cover*100:.0f} percent)")
    print("Year | plan wheat capacity | capacity holds | plan delivered wheat | plan margin | "
          "pattern wheat capacity | pattern holds")
    out = {}
    for year in YEARS:
        rp = replay_year(par, plan, yld, pri, year)
        rb = replay_year(par, pattern, yld, pri, year)
        holds_p = rp["wheat_capacity_t"] is not None and rp["wheat_capacity_t"] >= floor_t
        holds_b = rb["wheat_capacity_t"] is not None and rb["wheat_capacity_t"] >= floor_t
        print(f"{year} | {rp['wheat_capacity_t']:,.0f} | {'yes' if holds_p else 'no'} | "
              f"{rp['delivery_wheat_t']:,.0f} | {rp['delivery_margin']:,.0f} | "
              f"{rb['wheat_capacity_t']:,.0f} | {'yes' if holds_b else 'no'}"
              + (f" | carried prices from {rp['carried_prices']}" if rp["carried_prices"] else ""))
        out[str(year)] = {"plan_capacity_t": rp["wheat_capacity_t"], "plan_holds": bool(holds_p),
                          "plan_delivery_wheat_t": rp["delivery_wheat_t"],
                          "plan_margin": rp["delivery_margin"],
                          "pattern_capacity_t": rb["wheat_capacity_t"],
                          "pattern_holds": bool(holds_b)}
    RESULTS["backtest"] = {"cover": cover, "floor_t": floor_t, "years": out}
    save()


def _pair_cost(par, cover, **kw):
    """Guarantee cost at the headline cover under one perturbation."""
    out = {}
    for lv in (0.0, cover):
        prob, v = m.build(par, floor_cover=lv, caps=True, **kw)
        st = m.solve(prob)
        if st != "Optimal":
            return None
        out[lv] = float(pulp.value(prob.objective))
    return out[0.0] - out[cover]


def breakeven_mode():
    par = m.load_all()
    cover = headline_cover()
    print(f"BREAK EVEN SENSITIVITY at the capped headline level of {cover*100:.0f} percent cover")
    t0 = time.time()
    base = _pair_cost(par, cover)
    print(f"Base guarantee cost: {base:,.0f} pounds | seconds {time.time()-t0:.0f}")
    pert = {}
    price_sets = {
        "wheat price": ["Wheat"], "rice price": ["Rice"], "maize price": ["Maize_summer", "Maize_nili"],
        "potato prices": ["Potatoes_winter", "Potatoes_summer", "Potatoes_nili"],
        "berseem price": ["Berseem"],
    }
    for name, crops in price_sets.items():
        for tag, f in (("down", 0.90), ("up", 1.10)):
            po = {c: {l: par["price"][c][l] * f for l in m.LAYER_STATES} for c in crops}
            pert[(name, tag)] = _pair_cost(par, cover, price_override=po)
    for tag, f in (("down", 0.90), ("up", 1.10)):
        co = {c: par["cost"][c] * (f if c == "Wheat" else 1.0) for c in m.ALL_CROPS}
        pert[("wheat cost", tag)] = _pair_cost(par, cover, cost_override=co)
    yo = {}
    for tag, f in (("down", 0.90), ("up", 1.10)):
        yo[tag] = {c: ({l: {d: par["yield"][c][l][d] * (f if c == "Wheat" else 1.0)
                            for d in m.DISTRICTS} for l in m.LAYER_STATES} if c == "Wheat"
                       else par["yield"][c]) for c in m.ALL_CROPS}
        pert[("wheat yield", tag)] = _pair_cost(par, cover, yield_override=yo[tag])
    for tag, f in (("down", 0.90), ("up", 1.10)):
        pert[("water anchor", tag)] = _pair_cost(par, cover, budget_scale=f)
    names = sorted({n for n, _ in pert})
    rows = {}
    print("Input | cost at minus 10 percent | cost at plus 10 percent | largest swing vs base")
    for name in names:
        dn, up = pert[(name, "down")], pert[(name, "up")]
        swing = max(abs(dn - base), abs(up - base))
        rows[name] = {"down": dn, "up": up, "swing": swing}
        print(f"{name} | {dn:,.0f} | {up:,.0f} | {swing:,.0f}")
    winner = max(rows, key=lambda n: rows[n]["swing"])
    print(f"Strongest single input: {winner}, swing {rows[winner]['swing']:,.0f} pounds "
          f"({100*rows[winner]['swing']/base:.1f} percent of the base cost)")
    # Break even search on the winner: the multiplier at which the
    # guarantee cost falls to half the base value, in the direction
    # that lowers the cost, by bisection on the stated bracket.
    direction = "up" if rows[winner]["up"] < rows[winner]["down"] else "down"
    lo, hi = (1.10, 2.00) if direction == "up" else (0.50, 0.90)
    print(f"Break even search on {winner}, direction {direction}, bracket {lo} to {hi}, "
          f"target cost {0.5*base:,.0f} (half the base)")

    def cost_at(mult):
        if winner in price_sets:
            po = {c: {l: par["price"][c][l] * mult for l in m.LAYER_STATES}
                  for c in price_sets[winner]}
            return _pair_cost(par, cover, price_override=po)
        if winner == "wheat cost":
            co = {c: par["cost"][c] * (mult if c == "Wheat" else 1.0) for c in m.ALL_CROPS}
            return _pair_cost(par, cover, cost_override=co)
        if winner == "wheat yield":
            yo2 = {c: ({l: {d: par["yield"][c][l][d] * (mult if c == "Wheat" else 1.0)
                             for d in m.DISTRICTS} for l in m.LAYER_STATES} if c == "Wheat"
                        else par["yield"][c]) for c in m.ALL_CROPS}
            return _pair_cost(par, cover, yield_override=yo2)
        return _pair_cost(par, cover, budget_scale=mult)

    c_lo, c_hi = cost_at(lo), cost_at(hi)
    print(f"  cost at {lo}: {c_lo:,.0f} | cost at {hi}: {c_hi:,.0f}")
    be = {"winner": winner, "direction": direction, "bracket": [lo, hi],
          "cost_at_lo": c_lo, "cost_at_hi": c_hi, "breakeven_multiplier": None}
    target = 0.5 * base
    if min(c_lo, c_hi) <= target <= max(c_lo, c_hi):
        for _ in range(5):
            mid = 0.5 * (lo + hi)
            c_mid = cost_at(mid)
            print(f"  cost at {mid:.3f}: {c_mid:,.0f}")
            if (c_mid - target) * (c_lo - target) > 0:
                lo, c_lo = mid, c_mid
            else:
                hi, c_hi = mid, c_mid
        be["breakeven_multiplier"] = 0.5 * (lo + hi)
        print(f"Break even multiplier for {winner}: about {be['breakeven_multiplier']:.3f}, "
              f"where the guarantee cost halves")
    else:
        print(f"No break even inside the bracket: the cost does not reach half the "
              f"base value between {lo} and {hi} for {winner}.")
    RESULTS["breakeven"] = {"base_cost": base, "cover": cover, "rows": rows, "breakeven": be}
    save()


def save():
    path = PROC_DIR / "results_methods.json"
    old = {}
    if path.exists():
        old = json.loads(path.read_text())
    old.update(RESULTS)
    with open(path, "w") as fh:
        json.dump(old, fh, indent=1, default=float)
    print(f"Method results written to data/processed/results_methods.json")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "mc"
    if mode == "mc":
        mc_mode()
    elif mode == "backtest":
        backtest_mode()
    elif mode == "breakeven":
        breakeven_mode()
    else:
        print(f"unknown mode {mode}")
