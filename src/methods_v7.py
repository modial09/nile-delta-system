"""Version 7 methods: Monte Carlo over the delivery response and
the financial parameters, the break even price of wheat against
berseem by governorate, and the sensitivity ranking of the new
inputs.

Monte Carlo design. For each candidate price, 2,000 draws with
seed 20261117. Each draw takes: one of the three response curves
with weights 0.25, 0.50 and 0.25; a production multiplier from a
whole year drawn with replacement from the FAOSTAT production
record of 2015 to 2024 (the year production divided by the mean of
the ten years), applied to the 10.2 million tonne basis, which is
how yield variation enters; an alternative farm gate price drawn
from the three version 6 wheat price layers with their planning
weights 0.25, 0.50 and 0.25, which moves the ratio and so the
share; and a world price scenario drawn from the three scenarios
with the same weights, converted at the central exchange rate.
Draws are independent across inputs, a stated simplification. For
each price the run reports the share of draws in which deliveries
reach the announced target of 5.0 million tonnes, the share in
which the delivered cover reaches the promised cover of the
central case at that price, the mean total programme cost, and
the conditional value at risk of the total cost over the worst
quarter of draws, the same tail share as version 6 uses on its
scenario set.

Break even design. For each governorate, the state price at which
the farmer margin per hectare of wheat, valued at the blended
price of the state channel and the trader channel on the central
response curve, first equals the farmer margin per hectare of
berseem on the model basis. Berseem in the model has one yield,
one price and one cost in every governorate, so the ranking across
governorates is the ranking of their published wheat yields. A
second reading values every tonne of wheat at the state price, as
if the whole crop could be delivered, which is the most favourable
case for wheat. Both are margin comparisons on the model basis;
the text that reports them names what they leave out.

Sensitivity design. At the announced price of 2,650 pounds per
ardeb, each new input is moved between its low and its high value
with every other input at its central value, and the swing in
deliveries and in the total programme cost is recorded and ranked.
The response curve is moved as a whole, low curve against high
curve. The production basis is moved across the range the Monte
Carlo production draws span, the lowest and highest multipliers
of 2015 to 2024 applied to the basis.

Usage:
  .venv/bin/python src/methods_v7.py mc
  .venv/bin/python src/methods_v7.py breakeven
  .venv/bin/python src/methods_v7.py sensitivity
"""

import json
import random
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import allocation_model_v6 as m
import allocation_model_v7 as v7

BASE_DIR = m.BASE_DIR
EXT_DIR = m.EXT_DIR
PROC_DIR = m.PROC_DIR
RESULTS = {}


def grid_rows():
    data = json.loads((PROC_DIR / "results_v7_grid.json").read_text())
    return data["grid"], data["response"]


def production_multipliers():
    crops = pd.read_csv(EXT_DIR / "faostat_crops_egypt.csv")
    sub = crops[(crops["crop"] == "wheat") & (crops["element"] == "Production")]
    vals = {int(r["year"]): float(r["value"]) for _, r in sub.iterrows()
            if 2015 <= int(r["year"]) <= 2024}
    mean = float(np.mean(list(vals.values())))
    return {yr: v / mean for yr, v in vals.items()}, mean


def mc_mode(n_draws=2000):
    par = m.load_all()
    alt_expected = float(par["price"]["Wheat"]["expected"])
    grid, resp = grid_rows()
    curves = [resp["low"], resp["central"], resp["high"]]
    mults, mean_prod = production_multipliers()
    years = sorted(mults)
    layers = [(float(par["price"]["Wheat"][l]), w)
              for l, w in (("low", 0.25), ("expected", 0.50), ("high", 0.25))]
    worlds = [(v7.WORLD_USD[k], w) for k, w in
              (("low", 0.25), ("central", 0.50), ("high", 0.25))]
    curve_w = [0.25, 0.50, 0.25]
    print(f"MONTE CARLO: {n_draws} draws per price, seed 20261117. Production "
          f"multipliers from FAOSTAT wheat production 2015 to 2024 (mean "
          f"{mean_prod:,.0f} tonnes): " +
          ", ".join(f"{y} {mults[y]:.3f}" for y in years))
    rng = random.Random(20261117)

    def pick(pairs):
        r = rng.random()
        acc = 0.0
        for val, w in pairs:
            acc += w
            if r <= acc:
                return val
        return pairs[-1][0]

    out = {}
    sample_rows = []
    for ardeb in v7.GRID_ARDEB:
        price_t = ardeb / v7.ARDEB_T
        promised_cover = grid[str(ardeb)]["cover"]
        dels, tots = [], []
        for n in range(n_draws):
            curve = curves[rng.choices(range(3), weights=curve_w)[0]]
            year = rng.choice(years)
            prod = v7.PRODUCTION_T * mults[year]
            alt = pick(layers)
            share = v7.share_of(curve, price_t / alt)
            delivered = share * prod
            world = pick(worlds)
            bill = delivered * price_t
            gap_t = max(0.0, v7.TARGET_T - delivered)
            gap_cost = gap_t * world * v7.FX_EGP["central"]
            carry_per_t = (price_t * v7.FIN_RATE["central"]
                           * v7.HOLD_MONTHS["central"] / 12.0
                           + v7.STORAGE_EGP_T_MONTH["central"]
                           * v7.HOLD_MONTHS["central"])
            total = bill + gap_cost + delivered * carry_per_t
            dels.append(delivered)
            tots.append(total)
            if ardeb == v7.ANNOUNCED_ARDEB:
                sample_rows.append({"draw": n, "year": year, "delivered_t": delivered,
                                    "total_cost": total})
        dels = np.array(dels)
        tots = np.array(tots)
        cover_draws = dels / m.WHEAT_CONSUMPTION_T
        worst = np.sort(tots)[int(0.75 * n_draws):]
        out[str(ardeb)] = {
            "promised_cover": promised_cover,
            "mean_delivered_t": float(dels.mean()),
            "share_reaching_target": float((dels >= v7.TARGET_T).mean()),
            "share_reaching_promised_cover": float((cover_draws >= promised_cover).mean()),
            "mean_total_cost": float(tots.mean()),
            "cvar_total_cost": float(worst.mean()),
            "total_p10": float(np.quantile(tots, 0.10)),
            "total_p90": float(np.quantile(tots, 0.90))}
        o = out[str(ardeb)]
        print(f"price {ardeb}: mean delivered {o['mean_delivered_t']:,.0f} tonnes | "
              f"draws reaching the 5.0 million tonne target "
              f"{100*o['share_reaching_target']:.1f} percent | draws reaching the "
              f"promised cover of {100*promised_cover:.2f} percent: "
              f"{100*o['share_reaching_promised_cover']:.1f} percent | mean total "
              f"cost {o['mean_total_cost']:,.0f} | worst quarter mean total cost "
              f"{o['cvar_total_cost']:,.0f}")
    pd.DataFrame(sample_rows).to_csv(PROC_DIR / "montecarlo_samples_v7.csv", index=False)
    RESULTS["montecarlo"] = out
    save()


def breakeven_mode():
    par = m.load_all()
    alt = float(par["price"]["Wheat"]["expected"])
    grid, resp = grid_rows()
    central = resp["central"]
    berseem_margin = (float(par["price"]["Berseem"]["expected"])
                      * float(par["yield"]["Berseem"]["expected"]["Beheira"])
                      - float(par["cost"]["Berseem"]))
    wheat_cost = float(par["cost"]["Wheat"])
    print(f"BREAK EVEN, wheat against berseem, model basis. Berseem margin "
          f"{berseem_margin:,.0f} pounds per hectare (price "
          f"{par['price']['Berseem']['expected']:,.2f} pounds per tonne on a "
          f"constructed feed value, yield "
          f"{par['yield']['Berseem']['expected']['Beheira']:.3f} tonnes per "
          f"hectare, cost {par['cost']['Berseem']:,.0f}). Wheat cost "
          f"{wheat_cost:,.0f} pounds per hectare. The revenue wheat must earn "
          f"per hectare to match berseem is {berseem_margin + wheat_cost:,.0f} "
          f"pounds.")
    print("Governorate | wheat yield tonnes per hectare | break even state price "
          "at the blended value, pounds per ardeb | break even if every tonne "
          "could be delivered, pounds per ardeb")
    out = {}
    for d in m.DISTRICTS:
        y = float(par["yield"]["Wheat"]["expected"][d])
        needed_blend = (berseem_margin + wheat_cost) / y
        full = needed_blend / 1.0  # per tonne value needed if all at state price
        def blended(p_t):
            s = v7.share_of(central, p_t / alt)
            return s * p_t + (1 - s) * alt
        lo_p, hi_p = alt, 200_000.0
        if blended(hi_p) < needed_blend:
            be_blend = None
        else:
            for _ in range(60):
                mid = 0.5 * (lo_p + hi_p)
                if blended(mid) < needed_blend:
                    lo_p = mid
                else:
                    hi_p = mid
            be_blend = 0.5 * (lo_p + hi_p)
        out[d] = {"yield_t_ha": y, "needed_value_per_tonne": needed_blend,
                  "breakeven_ardeb_blended": (be_blend * v7.ARDEB_T
                                              if be_blend else None),
                  "breakeven_ardeb_full_delivery": full * v7.ARDEB_T}
        be_txt = f"{be_blend * v7.ARDEB_T:,.0f}" if be_blend else "none in range"
        print(f"{d} | {y:.2f} | {be_txt} | {full * v7.ARDEB_T:,.0f}")
    RESULTS["breakeven"] = {"berseem_margin_per_ha": berseem_margin,
                            "wheat_cost_per_ha": wheat_cost, "by_governorate": out}
    save()


def sensitivity_mode():
    par = m.load_all()
    alt = float(par["price"]["Wheat"]["expected"])
    grid, resp = grid_rows()
    price_t = v7.ANNOUNCED_ARDEB / v7.ARDEB_T
    mults, _ = production_multipliers()
    base_share = v7.share_of(resp["central"], price_t / alt)
    base_delivered = base_share * v7.PRODUCTION_T
    base = v7.finance(base_delivered, price_t)

    def total_with(delivered=None, **kw):
        d = base_delivered if delivered is None else delivered
        return v7.finance(d, price_t, **kw)

    rows = {}
    d_low = v7.share_of(resp["low"], price_t / alt) * v7.PRODUCTION_T
    d_high = v7.share_of(resp["high"], price_t / alt) * v7.PRODUCTION_T
    rows["response curve"] = (total_with(delivered=d_low), total_with(delivered=d_high),
                              d_low, d_high)
    p_low = base_share * v7.PRODUCTION_T * min(mults.values())
    p_high = base_share * v7.PRODUCTION_T * max(mults.values())
    rows["production basis"] = (total_with(delivered=p_low), total_with(delivered=p_high),
                                p_low, p_high)
    rows["world price"] = (total_with(world="low"), total_with(world="high"),
                           base_delivered, base_delivered)
    rows["exchange rate"] = (total_with(fx="low"), total_with(fx="high"),
                             base_delivered, base_delivered)
    rows["financing rate"] = (total_with(fin="low"), total_with(fin="high"),
                              base_delivered, base_delivered)
    rows["holding period"] = (total_with(hold="low"), total_with(hold="high"),
                              base_delivered, base_delivered)
    rows["storage cost"] = (total_with(storage="low"), total_with(storage="high"),
                            base_delivered, base_delivered)
    print(f"SENSITIVITY at the announced price of {v7.ANNOUNCED_ARDEB} pounds per "
          f"ardeb. Base deliveries {base_delivered:,.0f} tonnes, base total "
          f"{base['total']:,.0f} pounds.")
    print("Input | total at low, pounds | total at high, pounds | swing in total, "
          "pounds | swing in deliveries, tonnes")
    ranked = {}
    for name, (f_lo, f_hi, d_lo, d_hi) in rows.items():
        swing = abs(f_hi["total"] - f_lo["total"])
        ranked[name] = {"total_low": f_lo["total"], "total_high": f_hi["total"],
                        "swing_total": swing,
                        "swing_delivered": abs(d_hi - d_lo)}
        print(f"{name} | {f_lo['total']:,.0f} | {f_hi['total']:,.0f} | "
              f"{swing:,.0f} | {abs(d_hi - d_lo):,.0f}")
    order = sorted(ranked, key=lambda n: ranked[n]["swing_total"], reverse=True)
    print("Ranking by swing in the total programme cost: " +
          ", ".join(f"{i+1} {n}" for i, n in enumerate(order)))
    RESULTS["sensitivity"] = {"base_delivered_t": base_delivered,
                              "base_total": base["total"], "rows": ranked,
                              "ranking": order}
    save()


def save():
    path = PROC_DIR / "results_v7_methods.json"
    old = {}
    if path.exists():
        old = json.loads(path.read_text())
    old.update(RESULTS)
    with open(path, "w") as fh:
        json.dump(old, fh, indent=1, default=float)
    print("Method results written to data/processed/results_v7_methods.json")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "mc"
    if mode == "mc":
        mc_mode()
    elif mode == "breakeven":
        breakeven_mode()
    elif mode == "sensitivity":
        sensitivity_mode()
    else:
        print(f"unknown mode {mode}")
