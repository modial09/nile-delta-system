"""Independent check routine for version 6.

Written separately from allocation_model_v6.py. It recomputes the
headline numbers by paths the build did not use: the cost bridge is
recomputed from the workbook file itself; the scenario rule is
recomputed from the inflow series file; the headline capped
problem and the capped ceiling are replayed under HiGHS, a
different solver from the CBC the build used; the saved headline
plan is checked against the rice decree directly from its file;
the Monte Carlo hold share is recomputed from the saved samples.

Usage: .venv/bin/python src/check_v6.py
Writes its verdicts to the console; the run is captured into
docs/foundation_rebuild/CheckV6_Independent_Verification.md by the
verification pass.
"""

import json
import sys
from pathlib import Path

import openpyxl
import pandas as pd
import pulp

sys.path.insert(0, str(Path(__file__).resolve().parent))
import allocation_model_v5 as m5
import allocation_model_v6 as m

BASE = m.BASE_DIR
PROC = m.PROC_DIR
EXT = m.EXT_DIR
VERDICTS = []


def verdict(name, ok, detail):
    VERDICTS.append((name, ok, detail))
    print(f"{'PASS' if ok else 'FAIL'} | {name} | {detail}")


def close(a, b, tol):
    return abs(a - b) <= tol


# 1. The cost bridge, recomputed from the workbook.
wb = openpyxl.load_workbook(BASE.parent.parent / "user" / "files" / "Egypt_Pakistan_Farm_Costs.xlsx",
                            data_only=True)
ws = wb["Annual indicators"]
cpi = {int(r[0]): float(r[5]) for r in ws.iter_rows(min_row=2, values_only=True) if r[0]}
factor = cpi[2025] / cpi[2022]
verdict("CPI bridge factor", close(factor, m.CPI_FACTOR_2022_2025, 1e-9),
        f"workbook factor {factor:.6f} against model {m.CPI_FACTOR_2022_2025:.6f}")
wsb = wb["Crop budgets"]
arc = {}
for r in wsb.iter_rows(min_row=2, values_only=True):
    if r[0] == "Wheat" and r[1] == "Egypt":
        arc[r[2]] = float(r[4])
wheat_cost = arc["2024/25"] / 0.42
verdict("Wheat cost on the ARC bridge", close(wheat_cost, m.COST_2025["Wheat"], 1e-6),
        f"ARC 2024/25 {arc['2024/25']:,.0f} per feddan gives {wheat_cost:,.2f} per hectare; "
        f"model carries {m.COST_2025['Wheat']:,.2f}")
bad = []
for c in m.ALL_CROPS:
    if c == "Wheat":
        continue
    expect = m5.COST_2022[c] * factor if c != "Berseem" else (9792.0 / 0.42) * factor
    if not close(expect, m.COST_2025[c], 1e-4):
        bad.append(c)
verdict("All other crop costs on the CPI bridge", not bad,
        "every non wheat cost equals its 2022 value times the workbook factor"
        if not bad else f"mismatch on {bad}")

# 2. Scenario rule recomputed from the inflow series file.
flows = pd.read_csv(EXT / "nile_inflow_aswan_series.csv")["flow_billion_cubic_metres"].astype(float)
mean_flow = float(flows.mean())
lo, hi = 0.85 * mean_flow, 1.08 * mean_flow
ratios = {"dry": float(flows[flows < lo].mean() / mean_flow),
          "normal": float(flows[(flows >= lo) & (flows <= hi)].mean() / mean_flow),
          "high": float(flows[flows > hi].mean() / mean_flow)}
par = m.load_all()
bad = []
for w in m.WATER_STATES:
    f = min(1.05, max(0.70, ratios[w[1]] + m.STORAGE_ADJ[w[0]]))
    if not close(f, par["inflow"]["release_factors"][w], 1e-9):
        bad.append(w)
verdict("Release rule factors", not bad,
        "all nine factors recompute from the series and the stated rule" if not bad else f"mismatch {bad}")
verdict("Scenario weights sum to one", close(sum(par["prob"].values()), 1.0, 1e-12),
        f"sum {sum(par['prob'].values()):.12f}")

# 3. Berseem study area total.
expect_b = 1_253_666.0 * 0.6824 * 0.42
verdict("Berseem study area construction", close(expect_b, par["berseem_total_ha"], 1e-6),
        f"{expect_b:,.1f} hectares against model {par['berseem_total_ha']:,.1f}")

# 4. Ladder arithmetic from the saved results files.
caps = json.loads((PROC / "results_v6_caps.json").read_text())
fr = caps["frontier_caps"]
levels = sorted(float(k) for k in fr)
margins = [fr[f"{lv:.2f}"]["margin"] for lv in levels if fr[f"{lv:.2f}"]]
mono = all(margins[i] > margins[i + 1] for i in range(len(margins) - 1))
verdict("Capped ladder strictly falling", mono,
        "margins " + ", ".join(f"{x:,.0f}" for x in margins))
ceil = caps["ceiling_caps_cover"]
top = max(lv for lv in levels if fr[f"{lv:.2f}"])
verdict("Capped ceiling above the top rung", ceil is not None and ceil >= top,
        f"ceiling cover {100*ceil:.2f} percent, top feasible rung {100*top:.0f} percent")
verdict("Cover and months conversion", close(top * 12, m.months_of(top * m.WHEAT_CONSUMPTION_T), 1e-9),
        f"at {100*top:.0f} percent cover the stock unit is {top*12:.2f} months")

# 5. The saved headline plan against the rice decree, from its file.
plan, plan_cover = m.load_plan(PROC / f"plan_v6_caps_cover{int(round(top*100))}.csv")
rice_by_state = {}
for (d, c, w), val in plan["summer"].items():
    if c == "Rice":
        rice_by_state[w] = rice_by_state.get(w, 0.0) + val
worst_rice = max(rice_by_state.values())
verdict("Headline plan inside the rice decree", worst_rice <= m.RICE_DECREE_HA + 1e-6,
        f"largest state rice area {worst_rice:,.1f} hectares against the decree {m.RICE_DECREE_HA:,.0f}")

# 6. HiGHS replays of the headline capped problem and the ceiling.
prob_h, v_h = m.build(par, floor_cover=top, caps=True)
prob_h.solve(pulp.HiGHS(msg=False))
st_h = pulp.LpStatus[prob_h.status]
obj_h = float(pulp.value(prob_h.objective)) if st_h == "Optimal" else None
saved = fr[f"{top:.2f}"]["margin"]
verdict("HiGHS replay of the headline capped rung",
        obj_h is not None and close(obj_h, saved, max(1.0, 1e-6 * abs(saved))),
        f"HiGHS {obj_h:,.0f} against CBC saved {saved:,.0f}" if obj_h is not None else f"HiGHS status {st_h}")
prob_c, v_c = m.build(par, caps=True, objective="maxstaple")
prob_c.solve(pulp.HiGHS(msg=False))
st_c = pulp.LpStatus[prob_c.status]
if st_c == "Optimal":
    t_h = float(v_c["t"].value())
    verdict("HiGHS replay of the capped ceiling",
            close(t_h / m.WHEAT_CONSUMPTION_T, ceil, 1e-4),
            f"HiGHS ceiling cover {100*t_h/m.WHEAT_CONSUMPTION_T:.2f} percent against CBC {100*ceil:.2f}")
else:
    verdict("HiGHS replay of the capped ceiling", False, f"HiGHS status {st_c}")

# 7. DRO ordering, from the saved dro results if present.
dro_path = PROC / "results_v6_dro.json"
if dro_path.exists():
    dro = json.loads(dro_path.read_text())["dro"]
    ok = all(v["robust_worst"] >= v["nominal_worst"] - 1.0
             and v["robust_expected"] <= v["nominal_expected"] + 1.0 for v in dro.values())
    verdict("DRO ordering", ok,
            "at every level the robust plan holds a worst case at least as high as the "
            "nominal plan and an expected margin no higher" if ok else "ordering violated")

# 8. Monte Carlo hold share recomputed from the saved samples.
mc_path = PROC / "montecarlo_samples_v6.csv"
meth_path = PROC / "results_v6_methods.json"
if mc_path.exists() and meth_path.exists():
    df = pd.read_csv(mc_path)
    meth = json.loads(meth_path.read_text())
    if "montecarlo" in meth:
        floor_t = meth["montecarlo"]["floor_t"]
        share = float((df["wheat_capacity_t"] >= floor_t).mean())
        verdict("Monte Carlo hold share recomputed",
                close(share, meth["montecarlo"]["capacity_hold_share"], 1e-9),
                f"recomputed {100*share:.1f} percent against saved "
                f"{100*meth['montecarlo']['capacity_hold_share']:.1f} percent")

# 9. Decision maker template isolation. The blank shipped template
# must reproduce the no template parameters exactly, and one filled
# cell must change only its named input.
import shutil
import tempfile

par_none = m.load_all(user_template_path=None)
par_blank = m.load_all()
verdict("Blank template equals the no template path",
        par_none["budget"] == par_blank["budget"]
        and par_none["cost"] == par_blank["cost"]
        and par_none["price"] == par_blank["price"],
        "budgets, costs and prices are identical with the blank shipped "
        "template and with no template at all")
tmp = Path(tempfile.mkdtemp())
one = tmp / "one_cell.csv"
shutil.copy(m.TEMPLATE_PATH if hasattr(m, "TEMPLATE_PATH") else
            BASE / "data" / "external" / "decision_maker_input_template.csv", one)
frame = pd.read_csv(one)
mask = (frame["input_type"] == "crop cost") & (frame["crop"] == "Wheat")
frame.loc[mask, "your_value"] = 99999.0
frame.to_csv(one, index=False)
par_one = m.load_all(user_template_path=one)
verdict("One filled template cell changes only its named input",
        par_one["cost"]["Wheat"] == 99999.0
        and all(par_one["cost"][c] == par_none["cost"][c] for c in par_none["cost"] if c != "Wheat")
        and par_one["budget"] == par_none["budget"]
        and par_one["price"] == par_none["price"],
        "a filled Wheat cost cell changed the Wheat cost and nothing else")

print(f"\n{sum(1 for _, ok, _ in VERDICTS if ok)} of {len(VERDICTS)} checks pass.")
