"""Independent arithmetic checks for version 5, run by the verifier.

Reads only the saved original artifacts (results JSON files, run logs
are not read here, robustness CSV, price extract) plus load_all from
the original model module for parameter values. Changes no file.
Run with PYTHONDONTWRITEBYTECODE=1 and the project venv python.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))
import allocation_model_v5 as M  # noqa: E402

PROC = ROOT / "data" / "processed"
EXT = ROOT / "data" / "external"


def close(a, b, tol):
    return abs(a - b) <= tol


print("=" * 70)
print("A. Frontier arithmetic from results_v5_main.json")
res = json.loads((PROC / "results_v5_main.json").read_text())
fr = res["frontier_primary"]
levels = ["0.00", "0.50", "0.60", "0.70", "0.75", "0.80"]
vals = [fr[k] for k in levels]
for k, v in zip(levels, vals):
    print(f"  floor {k}: {v:,.2f}" if v is not None else f"  floor {k}: null")
print("  infeasible levels (null):", [k for k in fr if fr[k] is None])
mono = all(vals[i] > vals[i + 1] for i in range(len(vals) - 1))
print("  margins strictly decreasing in the floor:", mono)
cost80 = fr["0.00"] - fr["0.80"]
print(f"  cost of the 80 percent guarantee = {cost80:,.2f}")
print("  log prints 268,610,886,052 -> match:", close(cost80, 268610886052, 1.0))
steps = [(levels[i], levels[i + 1], vals[i] - vals[i + 1]) for i in range(len(vals) - 1)]
for a, b, d in steps:
    print(f"  step cost {a} to {b}: {d:,.2f}")

print("=" * 70)
print("B. Probabilities and reference tonnage from load_all")
par = M.load_all()
inf = par["inflow"]
print("  inflow counts:", inf["counts"], "probs:", {k: round(v, 6) for k, v in inf["probs"].items()})
print("  inflow prob sum:", sum(inf["probs"].values()))
print("  layer prob sum:", sum(M.LAYER_PROB.values()))
print("  combined scenario prob sum:", sum(par["prob"].values()))
print("  number of scenarios:", len(par["scenarios"]), "drought among them:",
      any("drought" in s for s in par["prob"]))
print(f"  reference tonnage: {par['reference_t']:,.4f}")
print("  reference by crop:", {k: round(v, 1) for k, v in par["reference_by_crop"].items()})

print("=" * 70)
print("C. Ceiling and dual floor")
share = res["ceiling_primary_share"]
tonnes = share * par["reference_t"]
print(f"  ceiling share in JSON: {share:.16f} -> percent {100*share:.4f}")
print(f"  ceiling tonnage = share x reference: {tonnes:,.2f} (log prints 10,099,349)")
print("  match:", close(tonnes, 10099349, 1.0))
dual = res["dual"]
print(f"  dual floor in JSON: {dual['floor_exact_share']:.16f}")
print("  ceiling share minus 0.001:", share - 0.001)
print("  equal:", close(dual["floor_exact_share"], share - 0.001, 1e-15))
gap = dual["lp_objective"] - dual["mip_objective"]
print(f"  LP objective {dual['lp_objective']:,.2f}; MIP objective {dual['mip_objective']:,.2f}")
print(f"  gap {gap:,.2f} = {100*gap/dual['mip_objective']:.4f} percent of MIP (log: 387,494,759.19, 0.142 percent)")
print("  gap match:", close(gap, 387494759.19, 1.0))

print("=" * 70)
print("D. Historical pattern from JSON")
pat = res["pattern"]
worst = pat["worst_capacity"]
print(f"  worst scenario capacity: {worst:,.1f} in the JSON; per scenario min check:",
      close(worst, min(pat["capacity_by_scenario"].values()), 1e-6))
for lv in (0.50, 0.60, 0.65, 0.70, 0.75, 0.80):
    ft = lv * par["reference_t"]
    print(f"  level {lv:.2f}: floor tonnage {ft:,.1f}; held in every scenario: {worst >= ft}")
print("  highest level held in JSON:", pat["highest_level_held"])
print(f"  worst as percent of reference: {100*worst/par['reference_t']:.2f} (log: 65.75)")

print("=" * 70)
print("E. Information values from JSON")
info = res["info"]
print(f"  RP {info['rp']:,.2f} equals frontier 0.80: {close(info['rp'], fr['0.80'], 0.01)}")
print(f"  WS minus RP: {info['ws'] - info['rp']:,.2f}; EVPI in JSON: {info['evpi']:,.2f}; "
      f"match: {close(info['ws'] - info['rp'], info['evpi'], 0.01)}")
pv = info["penalised_rp"] - info["penalised_eev"]
print(f"  penalised RP {info['penalised_rp']:,.2f} minus penalised EEV {info['penalised_eev']:,.2f} = {pv:,.2f}")
print(f"  penalised VSS in JSON: {info['penalised_vss']:,.2f}; match: {close(pv, info['penalised_vss'], 0.01)}")
print("  keys in info block:", sorted(info.keys()))
print("  standard VSS key present:", any(k == "vss" for k in info))

print("=" * 70)
print("F. Robustness split statistics recomputed from robustness_samples_v5.csv")
rob = pd.read_csv(PROC / "robustness_samples_v5.csv")
print("  rows:", len(rob), "kinds:", rob["kind"].value_counts().to_dict())
target_t = 0.80 * par["reference_t"]
for kind in ("single year", "ten year window mean"):
    sub = rob[rob["kind"] == kind]
    sh = sub["share_percent"]
    sf = sub["shortfall_tonnes"]
    worst_dec = sf.sort_values(ascending=False).head(max(1, len(sf) // 10))
    hold_shortfall = 100.0 * (sf <= 1e-6).mean()
    hold_share = 100.0 * (sh / 100.0 >= 0.80).mean()
    print(f"  {kind}: n={len(sub)} min {sh.min():.2f} p10 {sh.quantile(0.10):.2f} "
          f"median {sh.median():.2f} mean {sh.mean():.2f} max {sh.max():.2f}")
    print(f"    hold share by shortfall zero: {hold_shortfall:.1f}; by share >= 80: {hold_share:.1f}")
    print(f"    worst decile mean shortfall: {worst_dec.mean():,.0f}; mean shortfall: {sf.mean():,.0f}")
    chk = np.allclose(sub["shortfall_tonnes"],
                      np.maximum(0.0, target_t - sub["max_staple_tonnes"]), atol=1.0)
    print("    shortfall column consistent with target tonnage:", chk)
    chk2 = np.allclose(sub["share_percent"], 100 * sub["max_staple_tonnes"] / par["reference_t"], atol=0.01)
    print("    share column consistent with reference tonnage:", chk2)
    chk3 = np.allclose(sub["budget_billion_cubic_metres"], 11.00 * sub["ratio"], atol=1e-6)
    print("    budget column equals 11.00 x ratio:", chk3)

print("=" * 70)
print("G. Price extract checks, faostat_producer_prices_egypt_dec2025.csv")
px = pd.read_csv(EXT / "faostat_producer_prices_egypt_dec2025.csv")
px = px[px["unit"] == "EGP per tonne"]
for crop in ("wheat", "maize", "potatoes", "rice_paddy", "sugar_beet"):
    sub = px[px["crop"] == crop].sort_values("year")
    last = sub.iloc[-1]
    v2024 = sub[sub["year"] == 2024]["price"]
    print(f"  {crop}: last observed {int(last['year'])} = {last['price']:,.0f}; "
          f"2024 value: {('%.0f' % v2024.iloc[0]) if len(v2024) else 'none'}; "
          f"missing years in 2018..2024: {[y for y in range(2018, 2025) if y not in set(sub['year'])]}")

print("=" * 70)
print("H. Drift forecasts recomputed from the extract (all five price series "
      "selected drift)")
fc = pd.read_csv(PROC / "forecast_prices_yields_v5.csv")
for crop in ("wheat", "maize", "potatoes", "rice_paddy", "sugar_beet"):
    sub = px[px["crop"] == crop].sort_values("year")
    vals = sub["price"].to_numpy(dtype=float)
    last_year = int(sub["year"].iloc[-1])
    horizon = 2025 - last_year
    mine = vals[-1] + horizon * float(np.mean(np.diff(vals)))
    row = fc[(fc["crop"] == crop) & (fc["target"] == "price")].iloc[0]
    print(f"  {crop}: my drift forecast {mine:,.4f}; saved {row['forecast_value']:,.4f}; "
          f"match: {close(mine, row['forecast_value'], 1e-6)}; "
          f"saved target season {int(row['forecast_season'])}, horizon {int(row['horizon_steps'])}")
for crop in ("wheat", "maize", "potatoes", "rice_paddy", "sugar_beet"):
    row = fc[(fc["crop"] == crop) & (fc["target"] == "yield")].iloc[0]
    print(f"  yield {crop}: saved target season {int(row['forecast_season'])}, "
          f"last observed {int(row['last_observed_year'])}, model {row['selected_model']}")
print("=" * 70)
print("I. Layer values the allocation model consumes (par price table)")
for crop in M.ALL_CROPS:
    p = par["price"][crop]
    flag = "  <-- LOW ABOVE EXPECTED" if p["low"] > p["expected"] else ""
    print(f"  {crop}: low {p['low']:,.2f} expected {p['expected']:,.2f} high {p['high']:,.2f}{flag}")
print("DONE")
