import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import au

par = au.load()
R = {}

R["physical_total"] = sum(par["physical"].values())
R["annual_total"] = sum(par["annual"].values())
R["reference_t"] = par["reference_t"]
R["reference_by_crop"] = par["reference_by_crop"]
R["yield_fills"] = [(c, d, round(v, 4)) for c, d, v in par["yield_fills"]]
R["yield_scale"] = {c: round(v, 4) for c, v in par["yield_scale"].items()}
R["inflow"] = {k: par["inflow"][k] for k in ("ratios", "probs", "budgets_bcm", "counts", "n_windows", "n_at_below")}
R["true_mean_budget"] = sum(par["inflow"]["probs"][i] * par["inflow"]["budgets_bcm"][i] for i in au.INF)

fails_cap = [c for c in par["check"] if c["obs"] > c["limit"] + 1e-9]
fails_unc = [c for c in par["check"] if c["obs"] > c["limit_uncapped"] + 1e-9]
R["baseline_check_capped_failures"] = fails_cap
R["baseline_check_uncapped_failures"] = [
    {"d": c["d"], "pool": c["pool"], "obs": c["obs"], "limit_uncapped": c["limit_uncapped"],
     "excess": c["obs"] - c["limit_uncapped"]} for c in fails_unc]
capped_pools = []
trunc_total = 0.0
reserve_sum_gap = {}
for d in au.D:
    tot_res = 0.0
    for p in au.POOLS:
        r = par["reserve"][d][p]
        tot_res += r["reserve"]
        if r["capped"]:
            capped_pools.append({"d": d, "pool": p, "prop": r["prop"], "reserve": r["reserve"],
                                 "truncated": r["prop"] - r["reserve"], "limit": par["land_limit"][d][p],
                                 "obs": r["obs"]})
            trunc_total += r["prop"] - r["reserve"]
    reserve_sum_gap[d] = {"annual_unmodeled": par["reserve"][d]["winter"]["unmod_annual"],
                          "sum_capped_reserves": tot_res,
                          "gap": par["reserve"][d]["winter"]["unmod_annual"] - tot_res}
R["capped_pools"] = capped_pools
R["truncated_total_ha"] = trunc_total
R["reserve_sum_gap"] = reserve_sum_gap
R["uncapped_limits_negative_or_tiny"] = [
    {"d": d, "pool": p, "limit_uncapped": par["land_limit_uncapped"][d][p]}
    for d in au.D for p in au.POOLS if par["land_limit_uncapped"][d][p] < par["reserve"][d][p]["obs"]]

# Robustness distribution from the saved file alone
rs = pd.read_csv(au.PROC / "robustness_samples_v4_1.csv")
shares = rs["share_percent"]
shorts = rs["shortfall_tonnes"]
worst = shorts.sort_values(ascending=False).head(10)
R["robust_file"] = {
    "n": int(len(rs)), "min": float(shares.min()), "p10": float(shares.quantile(0.10)),
    "median": float(shares.median()), "mean": float(shares.mean()), "max": float(shares.max()),
    "hold_share_pct": float(100 * (shares >= 80.0).mean()),
    "worst_decile_shortfall_mean": float(worst.mean()), "mean_shortfall": float(shorts.mean()),
    "max_staple_tonnes_max": float(rs["max_staple_tonnes"].max()),
    "floor_ref_80": 0.80 * par["reference_t"]}

# Saved plans: beet planting, pool sums against limits, single cells against pool limits
plan_info = {}
for name in ["floor50", "floor60", "floor70", "floor75", "floor80", "robust_plan"]:
    path = au.PROC / f"plan_v4_1_{name}.csv"
    if name == "robust_plan":
        path = au.PROC / "plan_v4_1_robust_plan.csv"
    plan, share = au.load_plan(path)
    beet = sum(plan["winter"][(d, "Sugar beet")] for d in au.D)
    worst_slack = None
    cell_over = []
    for d in au.D:
        for p, cs in au.POOLS.items():
            if p == "winter":
                tot = sum(plan["winter"][(d, c)] for c in cs)
                cells = [(c, plan["winter"][(d, c)]) for c in cs]
            else:
                for i in au.INF:
                    tot = sum(plan["summer"][(d, c, i)] for c in cs)
                    slack = par["land_limit"][d][p] - tot
                    if worst_slack is None or slack < worst_slack["slack"]:
                        worst_slack = {"d": d, "pool": p, "inflow": i, "planted": tot,
                                       "limit": par["land_limit"][d][p], "slack": slack}
                cells = [(c, plan["summer"][(d, c, au.INF[0])]) for c in cs]
            if p == "winter":
                slack = par["land_limit"][d][p] - tot
                if worst_slack is None or slack < worst_slack["slack"]:
                    worst_slack = {"d": d, "pool": p, "inflow": "all", "planted": tot,
                                   "limit": par["land_limit"][d][p], "slack": slack}
            for c, v in cells:
                if v > par["land_limit"][d][p] + 1e-9:
                    cell_over.append((d, c, v, par["land_limit"][d][p]))
        # single cell checks for every inflow
        for c in au.L_CROPS:
            for i in au.INF:
                v = plan["summer"][(d, c, i)]
                if v > par["land_limit"][d][au.POOL_OF[c]] + 1e-9:
                    cell_over.append((d, c, i, v, par["land_limit"][d][au.POOL_OF[c]]))
    planted = {}
    for c in au.A_CROPS:
        if c in au.W_CROPS:
            planted[c] = sum(plan["winter"][(d, c)] for d in au.D)
        else:
            planted[c] = sum(par["inflow"]["probs"][i] * plan["summer"][(d, c, i)]
                             for d in au.D for i in au.INF)
    plan_info[name] = {"share": share, "beet_winter_ha": beet, "worst_pool_slack": worst_slack,
                       "cells_over_pool_limit": cell_over, "planted_weighted": planted}
R["plans"] = plan_info

# Absorption multiples from saved plans (weighted planted against observed)
for name in ["floor80"]:
    mult = {}
    for c in au.A_CROPS:
        obs = sum(par["baseline"][c].values())
        mult[c] = plan_info[name]["planted_weighted"][c] / obs if obs > 0 else None
    R[f"absorption_{name}"] = mult

# Note arithmetic: frontier costs from the margins printed in the note
note_margins = {0: 403078762407, 50: 297739198932, 60: 262520406731, 70: 223222240454,
                75: 202983384826, 80: 175143528384}
note_cost_unc = {50: 105339563475, 60: 140558355676, 70: 179856521953, 75: 200095377581, 80: 227935234023}
note_cost_prev = {50: 105339563475, 60: 35218792200, 70: 39298166277, 75: 20238855628, 80: 27839856443}
levels = [0, 50, 60, 70, 75, 80]
arith = {}
for j, lv in enumerate(levels):
    if lv == 0:
        continue
    arith[lv] = {
        "cost_unc_recomputed": note_margins[0] - note_margins[lv],
        "cost_unc_note": note_cost_unc[lv],
        "cost_prev_recomputed": note_margins[levels[j - 1]] - note_margins[lv],
        "cost_prev_note": note_cost_prev[lv]}
R["frontier_arithmetic_on_note_margins"] = arith
R["penalised_consistency"] = {"rp_minus_pen_eev": 175143528384 - 167535664790,
                              "printed_pen_vss": 7607863594}
R["evpi_consistency"] = {"ws_minus_rp": 198927633193 - 175143528384, "printed_evpi": 23784104809}
R["accounting"] = {"diff": 403078762407 - 86006146997,
                   "pct": 100 * (403078762407 - 86006146997) / 86006146997}

# Forecasts as printed in the note, Section 12, against the forecast file
note_fc = {("wheat", "price"): (10296.94, 1485.60, 14.61), ("rice_paddy", "price"): (19394.14, 3735.60, 14.47),
           ("maize", "price"): (14836.22, 1998.12, 15.64), ("sugar_beet", "price"): (820.52, 92.26, 10.21),
           ("potatoes", "price"): (8405.44, 1396.76, 19.52),
           ("wheat", "yield"): (6.6789, 0.3250, 4.05), ("rice_paddy", "yield"): (9.1315, 0.2696, 2.12),
           ("maize", "yield"): (7.6834, 0.6912, 6.16), ("sugar_beet", "yield"): (56.0570, 5.8925, 6.39),
           ("potatoes", "yield"): (31.5165, 1.4879, 3.10)}
fc_check = {}
src = par["price_fc"] | {}
for (crop, tgt), (fv, rmse, mape) in note_fc.items():
    e = (par["price_fc"] if tgt == "price" else par["yield_fc"])[crop]
    fc_check[f"{crop}_{tgt}"] = {"file_forecast": e["forecast"], "note": fv,
                                 "file_rmse": e["rmse"], "note_rmse": rmse,
                                 "file_mape": e["mape"], "note_mape": mape}
R["forecast_check"] = fc_check

# WaPOR replay
wp = pd.read_csv(au.EXT / "wapor_aeti_governorate_2018_2025.csv")
wp_mean = wp.groupby("governorate")["consumption_billion_cubic_metres"].mean()
tot_m, tot_w, below = 0.0, 0.0, {}
for d in au.D:
    modeled = sum(par["baseline"][c][d] * par["water_req"][c] for c in au.A_CROPS) / 1e9
    tot_m += modeled
    tot_w += float(wp_mean[d])
    below[d] = modeled < float(wp_mean[d])
R["wapor"] = {"modeled_total_bcm": tot_m, "wapor_total_bcm": tot_w, "below_all": below}

print(json.dumps(R, indent=1, default=str))
Path(au.BASE / "data/processed/audit_v4_1_work/basics.json").write_text(json.dumps(R, indent=1, default=str))
