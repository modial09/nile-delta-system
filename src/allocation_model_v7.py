"""Problem One version 7: the procurement price as a decision variable.

Version 6 stays on disk unchanged as the verified record. This file
imports its loaders and its builder and adds one extension, approved
by the user on 17 November 2026: the wheat procurement price is
treated as a choice, and the model answers the price fight of the
coming season, an announced 2,650 pounds per ardeb against farmer
and parliament demands of 3,000 to 3,500 pounds per ardeb.

The extension has three parts.

1. A delivery response, fitted in this file from the public record
   assembled in data/external/v7_delivery_evidence.csv and written
   up in docs/foundation_rebuild/V7_Delivery_Response_Evidence.md.
   The response gives the share of national wheat production that
   reaches state collection points as a line in the ratio of the
   procurement price to the farm gate price. Three curves are
   carried: a central fit on the six seasons with a published farm
   gate price (2019 to 2024), a low curve at one standard error
   below the fitted slope, and a high curve fitted on all eight
   seasons including 2025 and 2026 on a constructed alternative
   price. The evidence note labels every weakness of this record:
   six fit points, one season with a legal delivery requirement,
   and a farm gate series that is partly administered.

2. A price grid. For each candidate price from 2,200 to 3,500
   pounds per ardeb the grid computes expected tonnes delivered on
   the central curve with the curve band beside it, the wheat cover
   and months of stock those tonnes buy, and the cropping plan the
   version 6 model chooses under its caps, its rice decree bound,
   berseem and its storage scenarios when wheat earns the blended
   price of the state channel and the trader channel. Two plan
   readings are reported: the free plan, which plants what margin
   alone would plant, and the pattern floor plan, which holds wheat
   production at the level the observed pattern can hold in every
   scenario, so the cost of holding production can be read at each
   price. A bisection also finds the blended price at which the
   free plan first plants wheat on its own.

3. A financial layer. For each price: the procurement bill on the
   tonnes delivered; the import gap against the announced delivery
   target of 5.0 million tonnes and its cost at world price
   scenarios with a stated shipping lag; the carrying and financing
   cost of the stock bought; and the total state programme cost.
   Every financial parameter is sourced or labelled in the evidence
   note, section 7. Money in the printed log is exact; the results
   log rounds to billions with one decimal, as version 6 did.

Usage, with the project venv python:
  .venv/bin/python src/allocation_model_v7.py grid
"""

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import pulp

sys.path.insert(0, str(Path(__file__).resolve().parent))
import allocation_model_v6 as m

BASE_DIR = m.BASE_DIR
EXT_DIR = m.EXT_DIR
PROC_DIR = m.PROC_DIR

ARDEB_T = 0.15  # one ardeb of wheat is 150 kilograms, 0.15 tonnes
GRID_ARDEB = [2200, 2350, 2500, 2650, 2800, 3000, 3250, 3500]
ANNOUNCED_ARDEB = 2650

# Financial parameters. Sources and labels are in section 7 of
# docs/foundation_rebuild/V7_Delivery_Response_Evidence.md.
PRODUCTION_T = 10_200_000.0        # FAO record 2026 harvest, carried as the basis
TARGET_T = 5_000_000.0             # announced delivery goal for the 2026 season
WORLD_USD = {"low": 265.0, "central": 313.0, "high": 400.0}   # per tonne, cost and freight
FX_EGP = {"low": 54.47, "central": 55.25, "high": 57.00}      # pounds per dollar
FIN_RATE = {"low": 0.23956, "central": 0.25, "high": 0.2635}  # treasury bill yields
HOLD_MONTHS = {"low": 3.0, "central": 5.0, "high": 7.0}       # labelled assumption
STORAGE_EGP_T_MONTH = {"low": 40.0, "central": 60.0, "high": 90.0}  # labelled assumption
LAG_DAYS = 75                      # labelled assumption, see the evidence note

RESULTS = {}


def fit_response():
    """Fit the delivery response from the evidence file and return
    the three curves with their diagnostics."""
    df = pd.read_csv(EXT_DIR / "v7_delivery_evidence.csv")
    fit = df[df["in_fit"] == "yes"]
    x = fit["price_ratio"].to_numpy(dtype=float)
    y = fit["delivery_share"].to_numpy(dtype=float)
    A = np.vstack([np.ones_like(x), x]).T
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    resid = y - A @ coef
    dof = len(x) - 2
    s2 = float((resid ** 2).sum() / dof)
    cov = s2 * np.linalg.inv(A.T @ A)
    se = np.sqrt(np.diag(cov))
    r2 = 1.0 - float((resid ** 2).sum()) / float(((y - y.mean()) ** 2).sum())
    central = {"intercept": float(coef[0]), "slope": float(coef[1])}
    mean_x, mean_y = float(x.mean()), float(y.mean())
    low_slope = float(coef[1] - se[1])
    low = {"intercept": mean_y - low_slope * mean_x, "slope": low_slope}
    df["ratio_all"] = df["price_egp_per_tonne"] / df["farm_gate_alternative_egp_per_tonne"]
    carried = df["season_harvest_year"].isin([2025, 2026])
    df.loc[carried, "ratio_all"] = (df.loc[carried, "price_egp_per_tonne"]
                                    / ALT_CARRIED)
    xa = df["ratio_all"].to_numpy(dtype=float)
    ya = df["delivery_share"].to_numpy(dtype=float)
    Aa = np.vstack([np.ones_like(xa), xa]).T
    coef_a, *_ = np.linalg.lstsq(Aa, ya, rcond=None)
    high = {"intercept": float(coef_a[0]), "slope": float(coef_a[1])}
    # Refit without 2022, the season with the legal delivery floor.
    keep = fit["season_harvest_year"] != 2022
    xw, yw = x[keep.to_numpy()], y[keep.to_numpy()]
    Aw = np.vstack([np.ones_like(xw), xw]).T
    coef_w, *_ = np.linalg.lstsq(Aw, yw, rcond=None)
    validation = {}
    for _, r in df[carried].iterrows():
        ratio = float(r["price_egp_per_tonne"]) / ALT_CARRIED
        validation[int(r["season_harvest_year"])] = {
            "ratio": ratio,
            "predicted_share": central["intercept"] + central["slope"] * ratio,
            "actual_share": float(r["delivery_share"])}
    return {"central": central, "low": low, "high": high,
            "se_intercept": float(se[0]), "se_slope": float(se[1]),
            "resid_std": float(np.sqrt(s2)), "r_squared": r2,
            "n_fit": int(len(x)), "mean_ratio": mean_x, "mean_share": mean_y,
            "fit_without_2022": {"intercept": float(coef_w[0]), "slope": float(coef_w[1])},
            "validation": validation}


ALT_CARRIED = 17_892.0  # placeholder, replaced by the loaded model price in grid_mode


def share_of(curve, ratio):
    return curve["intercept"] + curve["slope"] * ratio


def finance(delivered_t, price_t, world="central", fx="central",
            fin="central", hold="central", storage="central"):
    """The financial layer for one delivery outcome at one price.
    Returns the bill, the gap against the target and its import
    cost, the carrying cost, and the total programme cost, all in
    pounds. Gap tonnes are priced at the world scenario of the
    arrival quarter after the stated shipping lag; carrying is
    charged on delivered local tonnes only, a stated choice."""
    bill = delivered_t * price_t
    gap_t = max(0.0, TARGET_T - delivered_t)
    gap_cost = gap_t * WORLD_USD[world] * FX_EGP[fx]
    carry_per_t = (price_t * FIN_RATE[fin] * HOLD_MONTHS[hold] / 12.0
                   + STORAGE_EGP_T_MONTH[storage] * HOLD_MONTHS[hold])
    carrying = delivered_t * carry_per_t
    return {"bill": bill, "gap_t": gap_t, "gap_cost": gap_cost,
            "carrying": carrying, "total": bill + gap_cost + carrying}


def solve_plan(par, price_override=None, floor_cover=0.0):
    """Solve the version 6 capped model with a wheat price override
    folded into the parameter copy, the way the version 6 frontier
    folds its overrides, so the reported margins are valued on the
    same basis the solver used."""
    par_use = dict(par)
    if price_override is not None:
        merged = {c: dict(par["price"][c]) for c in m.ALL_CROPS}
        merged.update(price_override)
        par_use["price"] = merged
    prob, v = m.build(par_use, floor_cover=floor_cover, caps=True)
    st = m.solve(prob)
    if st != "Optimal":
        return st, None, None
    res = m.scenario_results(par_use, v)
    return st, res, m.plan_of(v)


def pattern_floor_cover(par):
    """The wheat cover the observed pattern can hold in every
    scenario, from the version 6 main run record."""
    path = PROC_DIR / "results_v6_main.json"
    if path.exists():
        data = json.loads(path.read_text())
        worst = data.get("pattern", {}).get("worst_capacity_t")
        if worst:
            return worst / m.WHEAT_CONSUMPTION_T
    return par["pattern_wheat_t"] / m.WHEAT_CONSUMPTION_T


def print_header(par, resp, alt):
    print("=" * 76)
    print("NILE DELTA ALLOCATION MODEL VERSION 7, PROCUREMENT PRICE EXTENSION")
    print("Built 17 November 2026 on version 6, which is unchanged on disk.")
    print("The procurement price is a decision variable. The grid runs from")
    print("2,200 to 3,500 pounds per ardeb of 150 kilograms. The announced")
    print(f"price for the coming season is {ANNOUNCED_ARDEB} pounds per ardeb.")
    print()
    print("DELIVERY RESPONSE, fitted from data/external/v7_delivery_evidence.csv")
    c = resp["central"]
    print(f"  Central curve, {resp['n_fit']} fit seasons 2019 to 2024: share = "
          f"{c['intercept']:.4f} + {c['slope']:.4f} times ratio")
    print(f"  Slope standard error {resp['se_slope']:.4f}, intercept standard error "
          f"{resp['se_intercept']:.4f}, residual standard deviation "
          f"{resp['resid_std']:.4f} of share, R squared {resp['r_squared']:.3f}")
    w = resp["fit_without_2022"]
    print(f"  Refit without 2022 (the legal delivery requirement season): share = "
          f"{w['intercept']:.4f} + {w['slope']:.4f} times ratio")
    lo, hi = resp["low"], resp["high"]
    print(f"  Low curve (slope less one standard error, pivoted at the mean): "
          f"share = {lo['intercept']:.4f} + {lo['slope']:.4f} times ratio")
    print(f"  High curve (all eight seasons, constructed alternative for 2025 "
          f"and 2026): share = {hi['intercept']:.4f} + {hi['slope']:.4f} times ratio")
    for yr, v in resp["validation"].items():
        print(f"  Validation {yr}: ratio {v['ratio']:.3f} on the carried alternative, "
              f"fitted share {v['predicted_share']:.4f}, actual share {v['actual_share']:.4f}")
    print()
    print(f"Alternative price for the coming season: the model farm gate wheat "
          f"price of {alt:,.2f} pounds per tonne (expected layer, version 6 basis).")
    print(f"Production basis: {PRODUCTION_T:,.0f} tonnes, the FAO record 2026 "
          f"harvest carried as the planning basis, labelled in the evidence note.")
    print(f"Delivery target: {TARGET_T:,.0f} tonnes, the announced goal for the "
          f"2026 season.")
    print(f"World price scenarios, dollars per tonne cost and freight: low "
          f"{WORLD_USD['low']:.0f}, central {WORLD_USD['central']:.0f}, high "
          f"{WORLD_USD['high']:.0f}. Exchange rate, pounds per dollar: low "
          f"{FX_EGP['low']:.2f}, central {FX_EGP['central']:.2f}, high {FX_EGP['high']:.2f}.")
    print(f"Financing rate on treasury bill yields: low {FIN_RATE['low']:.5f}, "
          f"central {FIN_RATE['central']:.2f}, high {FIN_RATE['high']:.4f}.")
    print(f"Holding period in months (labelled assumption): low {HOLD_MONTHS['low']:.0f}, "
          f"central {HOLD_MONTHS['central']:.0f}, high {HOLD_MONTHS['high']:.0f}. Storage "
          f"in pounds per tonne per month (labelled assumption): low "
          f"{STORAGE_EGP_T_MONTH['low']:.0f}, central {STORAGE_EGP_T_MONTH['central']:.0f}, "
          f"high {STORAGE_EGP_T_MONTH['high']:.0f}. Shipping lag on gap imports: "
          f"{LAG_DAYS} days, labelled assumption, cost carried through the arrival "
          f"quarter world scenario.")
    print("=" * 76)


def grid_mode():
    global ALT_CARRIED
    par = m.load_all()
    alt = float(par["price"]["Wheat"]["expected"])
    ALT_CARRIED = alt
    resp = fit_response()
    print_header(par, resp, alt)
    floor_cover = pattern_floor_cover(par)
    print(f"\nPattern floor for the plan readings: cover {floor_cover:.4f}, "
          f"{floor_cover * m.WHEAT_CONSUMPTION_T:,.0f} tonnes of wheat production "
          f"held in every scenario, the level the version 6 pattern test found "
          f"the observed pattern can hold.")
    curves = resp
    rows = {}
    prev = None
    print("\nPRICE GRID, central response curve and central financial parameters")
    print("Price per ardeb | price per tonne | ratio | share low, central, high | "
          "delivered central, million tonnes | cover percent | months | bill B | "
          "gap million tonnes | gap cost B | carrying B | total B | step cost per "
          "extra tonne")
    for ardeb in GRID_ARDEB:
        t0 = time.time()
        price_t = ardeb / ARDEB_T
        ratio = price_t / alt
        shares = {k: share_of(curves[k], ratio) for k in ("low", "central", "high")}
        delivered = shares["central"] * PRODUCTION_T
        fin = finance(delivered, price_t)
        fin_low = finance(shares["low"] * PRODUCTION_T, price_t)
        fin_high = finance(shares["high"] * PRODUCTION_T, price_t)
        step_per_t = None
        if prev is not None and delivered > prev["delivered"]:
            step_per_t = (fin["total"] - prev["total"]) / (delivered - prev["delivered"])
        # Plan readings at the blended price of the two channels.
        blend = {l: shares["central"] * price_t + (1 - shares["central"]) * par["price"]["Wheat"][l]
                 for l in m.LAYER_STATES}
        po = {"Wheat": blend}
        st_f, res_f, plan_f = solve_plan(par, price_override=po, floor_cover=0.0)
        st_p, res_p, plan_p = solve_plan(par, price_override=po, floor_cover=floor_cover)
        row = {"ardeb": ardeb, "price_t": price_t, "ratio": ratio,
               "share_low": shares["low"], "share_central": shares["central"],
               "share_high": shares["high"], "delivered_t": delivered,
               "delivered_low_t": shares["low"] * PRODUCTION_T,
               "delivered_high_t": shares["high"] * PRODUCTION_T,
               "cover": delivered / m.WHEAT_CONSUMPTION_T,
               "months": m.months_of(delivered), "finance": fin,
               "total_low_curve": fin_low["total"], "total_high_curve": fin_high["total"],
               "step_cost_per_extra_tonne": step_per_t,
               "extrapolated": bool(ratio > 1.0)}
        if st_f == "Optimal" and res_f is not None:
            row["free"] = {"margin": res_f["margin"],
                           "wheat_area_ha": res_f["planted"]["Wheat"],
                           "wheat_expected_t": res_f["wheat_expected"],
                           "planted": res_f["planted"]}
            m.save_plan(plan_f, PROC_DIR / f"plan_v7_free_price{ardeb}.csv", 0.0)
        if st_p == "Optimal" and res_p is not None:
            row["floor"] = {"margin": res_p["margin"],
                            "wheat_area_ha": res_p["planted"]["Wheat"],
                            "wheat_expected_t": res_p["wheat_expected"],
                            "planted": res_p["planted"]}
            row["guarantee_cost_at_price"] = (row.get("free", {}).get("margin")
                                              - res_p["margin"]
                                              if "free" in row else None)
            row["plan_deliveries_t"] = shares["central"] * res_p["wheat_expected"]
            m.save_plan(plan_p, PROC_DIR / f"plan_v7_floor_price{ardeb}.csv", floor_cover)
        rows[ardeb] = row
        print(f"{ardeb} | {price_t:,.2f} | {ratio:.4f} | {shares['low']:.4f}, "
              f"{shares['central']:.4f}, {shares['high']:.4f} | "
              f"{delivered/1e6:.4f} | {100*row['cover']:.2f} | {row['months']:.2f} | "
              f"{fin['bill']/1e9:.4f} | {fin['gap_t']/1e6:.4f} | "
              f"{fin['gap_cost']/1e9:.4f} | {fin['carrying']/1e9:.4f} | "
              f"{fin['total']/1e9:.4f} | "
              f"{step_per_t:,.0f}" if step_per_t is not None else
              f"{ardeb} | {price_t:,.2f} | {ratio:.4f} | {shares['low']:.4f}, "
              f"{shares['central']:.4f}, {shares['high']:.4f} | "
              f"{delivered/1e6:.4f} | {100*row['cover']:.2f} | {row['months']:.2f} | "
              f"{fin['bill']/1e9:.4f} | {fin['gap_t']/1e6:.4f} | "
              f"{fin['gap_cost']/1e9:.4f} | {fin['carrying']/1e9:.4f} | "
              f"{fin['total']/1e9:.4f} | first row")
        if "free" in row:
            print(f"    free plan at the blended price: margin "
                  f"{row['free']['margin']:,.0f} pounds, wheat area "
                  f"{row['free']['wheat_area_ha']:,.0f} hectares, expected wheat "
                  f"production {row['free']['wheat_expected_t']:,.0f} tonnes")
        if "floor" in row:
            print(f"    pattern floor plan: margin {row['floor']['margin']:,.0f} "
                  f"pounds, wheat area {row['floor']['wheat_area_ha']:,.0f} hectares, "
                  f"expected wheat production {row['floor']['wheat_expected_t']:,.0f} "
                  f"tonnes, cost of holding the floor at this price "
                  f"{row['guarantee_cost_at_price']:,.0f} pounds, study area "
                  f"deliveries on the central share {row['plan_deliveries_t']:,.0f} tonnes")
        print(f"    curve band on the total: low curve {fin_low['total']/1e9:.4f} "
              f"billion, high curve {fin_high['total']/1e9:.4f} billion | "
              f"seconds {time.time()-t0:.0f}")
        prev = {"delivered": delivered, "total": fin["total"]}
    # The blended price at which the free plan first plants wheat.
    print("\nWHEAT ENTRY THRESHOLD, free plan, flat wheat price in every layer")
    lo_p, hi_p = alt, 30_000.0
    def wheat_area_at(p):
        po = {"Wheat": {l: p for l in m.LAYER_STATES}}
        st, res, _ = solve_plan(par, price_override=po, floor_cover=0.0)
        return res["planted"]["Wheat"] if st == "Optimal" and res else 0.0
    a_lo = wheat_area_at(lo_p)
    a_hi = wheat_area_at(hi_p)
    print(f"  at the farm gate price {lo_p:,.0f}: wheat area {a_lo:,.0f} hectares")
    print(f"  at {hi_p:,.0f} pounds per tonne: wheat area {a_hi:,.0f} hectares")
    threshold = None
    if a_lo <= 0 < a_hi:
        for _ in range(6):
            mid = 0.5 * (lo_p + hi_p)
            if wheat_area_at(mid) > 0:
                hi_p = mid
            else:
                lo_p = mid
        threshold = hi_p
        print(f"  first wheat enters the free plan at a blended price of about "
              f"{threshold:,.0f} pounds per tonne")
        # The state price that produces that blended price on the
        # central curve, found by bisection on the state price.
        lo_s, hi_s = alt, 60_000.0
        for _ in range(40):
            mid = 0.5 * (lo_s + hi_s)
            s_mid = share_of(curves["central"], mid / alt)
            if s_mid * mid + (1 - s_mid) * alt < threshold:
                lo_s = mid
            else:
                hi_s = mid
        state_price = 0.5 * (lo_s + hi_s)
        print(f"  on the central response curve that blended price is reached at "
              f"a state price of about {state_price:,.0f} pounds per tonne, "
              f"{state_price * ARDEB_T:,.0f} pounds per ardeb")
        RESULTS["entry_threshold"] = {"blended_price_t": threshold,
                                      "state_price_t": state_price,
                                      "state_price_ardeb": state_price * ARDEB_T}
    RESULTS["response"] = resp
    RESULTS["pattern_floor_cover"] = floor_cover
    RESULTS["grid"] = {str(k): v for k, v in rows.items()}
    path = PROC_DIR / "results_v7_grid.json"
    with open(path, "w") as fh:
        json.dump(RESULTS, fh, indent=1, default=float)
    print(f"\nUnrounded results written to data/processed/results_v7_grid.json")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "grid"
    if mode == "grid":
        grid_mode()
    else:
        print(f"unknown mode {mode}")
