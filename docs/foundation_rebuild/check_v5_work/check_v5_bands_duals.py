"""Independent band, coverage and dual checks for version 5.

Bands: reruns the module rolling backtest per series, then computes
the residual quartiles, the band and the sequential coverage with
this script own arithmetic, and compares against the saved
forecast_prices_yields_v5.csv.
Duals: solves the LP relaxation and the mixed integer model at the
exact dual floor with this script own calls, reads the water
constraint duals, and compares two printed cells and both objectives
against the run log and the results JSON.
Changes no existing file. Run with PYTHONDONTWRITEBYTECODE=1.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pulp

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))
import allocation_model_v5 as M  # noqa: E402
import forecasting_v5 as F  # noqa: E402

PROC = ROOT / "data" / "processed"
fc = pd.read_csv(PROC / "forecast_prices_yields_v5.csv")


def my_coverage(preds, min_prior=5):
    p = preds.sort_values("year")
    resid = p["actual"].to_numpy(dtype=float) - p["forecast"].to_numpy(dtype=float)
    hits, n = 0, 0
    for i in range(min_prior, len(resid)):
        lo = float(np.quantile(resid[:i], 0.25))
        hi = float(np.quantile(resid[:i], 0.75))
        n += 1
        if lo <= resid[i] <= hi:
            hits += 1
    return (100.0 * hits / n if n else float("nan")), n


print("=" * 70)
print("Band and coverage recomputation")
prices = F.load_price_series()
yields, areas = F.load_yield_and_area_series()
for target, series_map, train_end, target_year in (
        ("price", prices, F.PRICE_FIRST_TRAIN_END, F.PRICE_TARGET_YEAR),
        ("yield", yields, F.YIELD_FIRST_TRAIN_END, F.YIELD_TARGET_YEAR)):
    for crop in F.CROPS:
        series = F.attach_lagged_externals(series_map[crop], areas[crop], None)
        last_year = int(series["year"].max())
        horizon = target_year - last_year
        preds, _fails = F.rolling_backtest(series, train_end, horizon=horizon)
        row = fc[(fc["crop"] == crop) & (fc["target"] == target)].iloc[0]
        sel = row["selected_model"]
        sp = preds[preds["model"] == sel]
        resid = sp["actual"].to_numpy(dtype=float) - sp["forecast"].to_numpy(dtype=float)
        fcv = float(row["forecast_value"])
        lo = fcv + float(np.quantile(resid, 0.25))
        hi = fcv + float(np.quantile(resid, 0.75))
        cov, n = my_coverage(sp)
        ok = (abs(lo - row["band_low"]) < 1e-6 and abs(hi - row["band_high"]) < 1e-6
              and abs(cov - row["band_coverage_pct"]) < 1e-9 and n == int(row["coverage_origins"]))
        print(f"  {crop} {target} ({sel}, horizon {horizon}): my band "
              f"{lo:,.4f} to {hi:,.4f}; saved {row['band_low']:,.4f} to "
              f"{row['band_high']:,.4f}; my coverage {cov:.2f} over {n}; "
              f"saved {row['band_coverage_pct']:.2f} over {int(row['coverage_origins'])}; "
              f"match: {ok}")
        if target == "price" and crop == "potatoes":
            print(f"    note: residual quartiles are {float(np.quantile(resid, 0.25)):,.2f} "
                  f"and {float(np.quantile(resid, 0.75)):,.2f}; both positive, so the "
                  f"low band sits above the point forecast")

print("=" * 70)
print("Dual run replay at the exact floor")
par = M.load_all()
res = json.loads((PROC / "results_v5_main.json").read_text())
floor = res["dual"]["floor_exact_share"]
prob, v = M.build(par, floor_share=floor, relax=True)
st = M.solve(prob, gap=0.0)
lp_obj = float(pulp.value(prob.objective))
print(f"  LP status {st}; my LP objective {lp_obj:,.2f}; saved "
      f"{res['dual']['lp_objective']:,.2f}; diff {lp_obj - res['dual']['lp_objective']:,.2f}")
cells = {}
for name, con in prob.constraints.items():
    if name.startswith("Water_"):
        rest = name[len("Water_"):]
        for s in par["scenarios"]:
            sk = M.skey(*s)
            if rest.endswith("_" + sk):
                dname = rest[: -len(sk) - 1].replace("_", " ")
                raw = abs(float(con.pi)) / 1000.0
                cells[(dname, sk)] = (raw, raw / par["prob"][s])
for cell, printed in ((("Beheira", "dry_low"), (51.3494, 893.03)),
                      (("Damietta", "normal_expected"), (5.5007, 24.45)),
                      (("Qalyubia", "high_low"), (2.5290, 31.61))):
    raw, cond = cells[cell]
    print(f"  {cell}: my raw {raw:.4f} conditional {cond:.2f}; printed "
          f"{printed[0]:.4f} and {printed[1]:.2f}; match: "
          f"{abs(raw - printed[0]) < 0.001 and abs(cond - printed[1]) < 0.02}")
prob_m, _ = M.build(par, floor_share=floor)
st_m = M.solve(prob_m, gap=0.0)
mip_obj = float(pulp.value(prob_m.objective))
print(f"  MIP status {st_m}; my MIP objective {mip_obj:,.2f}; saved "
      f"{res['dual']['mip_objective']:,.2f}; diff {mip_obj - res['dual']['mip_objective']:,.2f}")
print(f"  my gap: {lp_obj - mip_obj:,.2f} ({100*(lp_obj - mip_obj)/mip_obj:.3f} percent)")
print("DONE")
