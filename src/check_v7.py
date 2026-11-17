"""Independent check routine for version 7.

Written separately from allocation_model_v7.py and methods_v7.py.
It recomputes the headline numbers by paths the build did not use:
the response fit is recomputed with numpy polyfit rather than the
build lstsq call; the grid arithmetic is recomputed from the saved
inputs with plain arithmetic; the announced price plans are
replayed under HiGHS, a different solver from the CBC the build
used; the saved floor plan is checked against the rice decree
directly from its file; the Monte Carlo shares at the announced
price are recomputed from the saved samples; and one break even
price is recomputed directly from the parameter values.

Usage: .venv/bin/python src/check_v7.py
Writes its verdicts to the console; the run is captured into
docs/foundation_rebuild/CheckV7_Independent_Verification.md by the
verification pass.
"""

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pulp

sys.path.insert(0, str(Path(__file__).resolve().parent))
import allocation_model_v6 as m
import allocation_model_v7 as v7

BASE = m.BASE_DIR
PROC = m.PROC_DIR
EXT = m.EXT_DIR
VERDICTS = []


def verdict(name, ok, detail):
    VERDICTS.append((name, ok, detail))
    print(f"{'PASS' if ok else 'FAIL'} | {name} | {detail}")


def close(a, b, tol):
    return abs(a - b) <= tol


grid = json.loads((PROC / "results_v7_grid.json").read_text())
resp_saved = grid["response"]
rows = grid["grid"]

# 1. The response fit, recomputed with polyfit.
df = pd.read_csv(EXT / "v7_delivery_evidence.csv")
fit = df[df["in_fit"] == "yes"]
x = fit["price_ratio"].to_numpy(dtype=float)
y = fit["delivery_share"].to_numpy(dtype=float)
slope, intercept = np.polyfit(x, y, 1)
verdict("Response fit recomputed",
        close(intercept, resp_saved["central"]["intercept"], 1e-9)
        and close(slope, resp_saved["central"]["slope"], 1e-9),
        f"polyfit intercept {intercept:.6f} slope {slope:.6f} against build "
        f"{resp_saved['central']['intercept']:.6f} and {resp_saved['central']['slope']:.6f}")
pred = intercept + slope * x
r2 = 1.0 - float(((y - pred) ** 2).sum()) / float(((y - y.mean()) ** 2).sum())
verdict("Response fit R squared", close(r2, resp_saved["r_squared"], 1e-9),
        f"recomputed {r2:.6f} against saved {resp_saved['r_squared']:.6f}")
val = resp_saved["validation"]["2026"]
verdict("Validation 2026 underprediction stands as reported",
        val["actual_share"] > val["predicted_share"],
        f"fitted {val['predicted_share']:.4f} against actual {val['actual_share']:.4f}; "
        f"the check confirms the direction of the miss rather than hiding it")

# 2. Grid arithmetic recomputed for three prices.
par = m.load_all()
alt = float(par["price"]["Wheat"]["expected"])
bad = []
for ardeb in (2200, 2650, 3500):
    row = rows[str(ardeb)]
    price_t = ardeb / 0.15
    ratio = price_t / alt
    share = resp_saved["central"]["intercept"] + resp_saved["central"]["slope"] * ratio
    delivered = share * v7.PRODUCTION_T
    bill = delivered * price_t
    gap_t = max(0.0, v7.TARGET_T - delivered)
    gap_cost = gap_t * v7.WORLD_USD["central"] * v7.FX_EGP["central"]
    carrying = delivered * (price_t * v7.FIN_RATE["central"] * 5.0 / 12.0 + 60.0 * 5.0)
    total = bill + gap_cost + carrying
    fin = row["finance"]
    if not (close(delivered, row["delivered_t"], 1.0) and close(bill, fin["bill"], 1.0)
            and close(gap_cost, fin["gap_cost"], 1.0)
            and close(carrying, fin["carrying"], 1.0) and close(total, fin["total"], 1.0)):
        bad.append(ardeb)
verdict("Grid arithmetic at 2200, 2650 and 3500", not bad,
        "deliveries, bill, gap cost, carrying and total recompute from the "
        "saved inputs" if not bad else f"mismatch at {bad}")

# 3. Monotonicity and conversion checks on the saved grid.
ard = sorted(int(k) for k in rows)
dels = [rows[str(a)]["delivered_t"] for a in ard]
bills = [rows[str(a)]["finance"]["bill"] for a in ard]
verdict("Deliveries non decreasing in price",
        all(dels[i] <= dels[i + 1] for i in range(len(dels) - 1)),
        "deliveries in million tonnes: " + ", ".join(f"{d/1e6:.3f}" for d in dels))
verdict("Bill strictly increasing in price",
        all(bills[i] < bills[i + 1] for i in range(len(bills) - 1)),
        "the bill rises at every step even though the share also rises")
conv_ok = all(close(rows[str(a)]["cover"] * 12.0, rows[str(a)]["months"], 1e-9)
              for a in ard)
verdict("Cover and months conversion", conv_ok,
        "months equal cover times twelve at every grid row")

# 4. HiGHS replays of the announced price plans.
ann = rows[str(v7.ANNOUNCED_ARDEB)]
price_t = v7.ANNOUNCED_ARDEB / v7.ARDEB_T
s_c = ann["share_central"]
blend = {l: s_c * price_t + (1 - s_c) * par["price"]["Wheat"][l]
         for l in m.LAYER_STATES}
floor_cover = grid["pattern_floor_cover"]
for tag, fc, saved in (("free", 0.0, ann["free"]), ("floor", floor_cover, ann["floor"])):
    par_use = dict(par)
    merged = {c: dict(par["price"][c]) for c in m.ALL_CROPS}
    merged.update({"Wheat": blend})
    par_use["price"] = merged
    prob, v = m.build(par_use, floor_cover=fc, caps=True)
    prob.solve(pulp.HiGHS(msg=False))
    st = pulp.LpStatus[prob.status]
    if st != "Optimal":
        verdict(f"HiGHS replay of the announced price {tag} plan", False,
                f"HiGHS status {st}")
        continue
    res = m.scenario_results(par_use, v)
    verdict(f"HiGHS replay of the announced price {tag} plan",
            close(res["margin"], saved["margin"], max(1.0, 1e-6 * abs(saved["margin"])))
            and close(res["wheat_expected"], saved["wheat_expected_t"],
                      max(1.0, 1e-6 * abs(saved["wheat_expected_t"]))),
            f"HiGHS margin {res['margin']:,.0f} against CBC saved "
            f"{saved['margin']:,.0f}; HiGHS expected wheat "
            f"{res['wheat_expected']:,.0f} against {saved['wheat_expected_t']:,.0f}")

# 5. The saved announced price floor plan against the rice decree.
plan, _ = m.load_plan(PROC / f"plan_v7_floor_price{v7.ANNOUNCED_ARDEB}.csv")
rice_by_state = {}
for (d, c, w), val in plan["summer"].items():
    if c == "Rice":
        rice_by_state[w] = rice_by_state.get(w, 0.0) + val
worst_rice = max(rice_by_state.values())
verdict("Announced price floor plan inside the rice decree",
        worst_rice <= m.RICE_DECREE_HA + 1e-6,
        f"largest state rice area {worst_rice:,.1f} hectares against the decree "
        f"{m.RICE_DECREE_HA:,.0f}")

# 6. Monte Carlo shares recomputed from the saved samples.
meth_path = PROC / "results_v7_methods.json"
mc_path = PROC / "montecarlo_samples_v7.csv"
if meth_path.exists() and mc_path.exists():
    meth = json.loads(meth_path.read_text())
    if "montecarlo" in meth:
        samples = pd.read_csv(mc_path)
        saved_mc = meth["montecarlo"][str(v7.ANNOUNCED_ARDEB)]
        share_t = float((samples["delivered_t"] >= v7.TARGET_T).mean())
        n = len(samples)
        worst = samples["total_cost"].sort_values().iloc[int(0.75 * n):]
        verdict("Monte Carlo target share recomputed at the announced price",
                close(share_t, saved_mc["share_reaching_target"], 1e-9),
                f"recomputed {100*share_t:.2f} percent against saved "
                f"{100*saved_mc['share_reaching_target']:.2f} percent over {n} draws")
        verdict("Monte Carlo worst quarter cost recomputed at the announced price",
                close(float(worst.mean()), saved_mc["cvar_total_cost"], 1.0),
                f"recomputed {float(worst.mean()):,.0f} against saved "
                f"{saved_mc['cvar_total_cost']:,.0f}")
    if "breakeven" in meth:
        be = meth["breakeven"]
        d = "Sharkia"
        saved_be = be["by_governorate"][d]["breakeven_ardeb_full_delivery"]
        y = float(par["yield"]["Wheat"]["expected"][d])
        direct = (be["berseem_margin_per_ha"] + be["wheat_cost_per_ha"]) / y * 0.15
        verdict("Break even spot check, Sharkia, full delivery reading",
                close(direct, saved_be, 1e-6),
                f"direct recomputation {direct:,.2f} pounds per ardeb against "
                f"saved {saved_be:,.2f}")

print(f"\n{sum(1 for _, ok, _ in VERDICTS if ok)} of {len(VERDICTS)} checks pass.")
