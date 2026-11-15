import json
import sys
import time
from pathlib import Path

import pulp

sys.path.insert(0, str(Path(__file__).parent))
import au

par = au.load()
out = {}
REF = par["reference_t"]

# Wait and see: twelve deterministic solves at the 80 percent floor
ws = 0.0
ws_per = {}
for s in par["scenarios"]:
    price_o = {c: {l: par["price"][c][s[1]] for l in au.LAY} for c in au.A_CROPS}
    yld_o = {c: {l: par["yield"][c][s[1]] for l in au.LAY} for c in au.A_CROPS}
    p_s = au.modified(par, price=price_o, **{"yield": yld_o})
    prob, v = au.build(p_s, floor=0.80, single=s)
    st = au.solve(prob)
    if st != "Optimal":
        ws_per[f"{s[0]}_{s[1]}"] = {"status": st}
        continue
    plan = au.plan_of(v)
    m, stap = au.scenario_margin_staple(par, v, s, plan)
    ws_per[f"{s[0]}_{s[1]}"] = {"status": st, "margin": m}
    ws += par["prob"][s] * m
    print("WS", s, round(m), flush=True)
out["ws_per"] = ws_per
out["ws"] = ws
rp = 175143528383.6324  # my own scaled frontier solve at 80 percent, run_frontier_scaled.py
out["rp_mine_scaled"] = rp
out["evpi_mine"] = ws - rp

# Expected value problem at true means
true_budget = sum(par["inflow"]["probs"][i] * par["inflow"]["budgets_bcm"][i] for i in au.INF)
out["true_mean_budget"] = true_budget
mean_price = {c: sum(au.LPROB[l] * par["price"][c][l] for l in au.LAY) for c in au.A_CROPS}
mean_yield = {c: {d: sum(au.LPROB[l] * par["yield"][c][l][d] for l in au.LAY) for d in au.D}
              for c in au.A_CROPS}
out["mean_price"] = mean_price
price_o = {c: {l: mean_price[c] for l in au.LAY} for c in au.A_CROPS}
yld_o = {c: {l: mean_yield[c] for l in au.LAY} for c in au.A_CROPS}
tot_phys = sum(par["physical"].values())
bud = {(d, i): true_budget * 1e9 * par["physical"][d] / tot_phys for d in au.D for i in au.INF}
p_m = au.modified(par, price=price_o, budget=bud, **{"yield": yld_o})
s0 = ("normal", "expected")
prob, v = au.build(p_m, floor=0.80, single=s0)
st = au.solve(prob)
out["ev_solve_status"] = st
ev_single = au.plan_of(v)
ev_plan = {"winter": ev_single["winter"],
           "summer": {(d, c, i): ev_single["summer"][(d, c, "normal")]
                      for d in au.D for c in au.L_CROPS for i in au.INF}}
# (a) no floor evaluation
ev_eval = au.evaluate_plan(par, ev_plan)
out["ev_no_floor_margin"] = sum(par["prob"][s] * r["margin"] for s, r in ev_eval.items() if "margin" in r)
print("EV no floor margin", out["ev_no_floor_margin"], flush=True)
# (b) floor failure pattern by staple maximisation
mx = au.max_staple_plan(par, ev_plan, bound="cell")
floor_t = 0.80 * REF
out["ev_max_staple"] = {f"{s[0]}_{s[1]}": val for s, val in mx.items()}
fails = [f"{s[0]}_{s[1]}" for s, val in mx.items() if val is None or val < floor_t - 0.1]
holds = [f"{s[0]}_{s[1]}" for s, val in mx.items() if val is not None and val >= floor_t - 0.1]
out["ev_fails"] = fails
out["ev_holds"] = holds
print("EV fails", fails, flush=True)
# (c) penalised evaluation
pen_total = 0.0
pen_per = {}
for s in par["scenarios"]:
    prob2, v2 = au.build(par, floor=0.80, fixed=ev_plan, single=s, penalise=25000.0)
    st2 = au.solve(prob2)
    if st2 != "Optimal":
        pen_per[f"{s[0]}_{s[1]}"] = {"status": st2}
        continue
    obj = float(pulp.value(prob2.objective))
    short = float(v2["shortfall"][s].value())
    pen_per[f"{s[0]}_{s[1]}"] = {"penalised_margin": obj, "shortfall": short}
    pen_total += par["prob"][s] * obj
out["penalised_per"] = pen_per
out["penalised_eev"] = pen_total
out["penalised_vss_mine"] = rp - pen_total
print("penalised EEV", pen_total, flush=True)

# Stress pairs
for scale in (0.90, 0.80):
    prob, v = au.build(par, floor=0.0, budget_scale=scale)
    st = au.solve(prob)
    m = float(pulp.value(prob.objective)) if st == "Optimal" else None
    stap_exp = 0.0
    stap_min = None
    planted_staple = 0.0
    if st == "Optimal":
        for s in par["scenarios"]:
            sv = sum(float(pulp.value(v["prod"][(d, c, s)])) for d in au.D for c in au.STAPLES)
            stap_exp += par["prob"][s] * sv
            stap_min = sv if stap_min is None else min(stap_min, sv)
        planted_staple = sum(float(v["xw"][(d, "Wheat")].value()) for d in au.D)
        for c in ("Rice", "Maize_summer"):
            planted_staple += sum(par["inflow"]["probs"][i] * float(v["xs"][(d, c, i)].value())
                                  for d in au.D for i in au.INF)
    prob2, v2 = au.build(par, objective="maxstaple", budget_scale=scale)
    st2 = au.solve(prob2)
    cap = float(v2["t"].value()) if st2 == "Optimal" else None
    out[f"stress_{scale}"] = {"margin_status": st, "margin": m, "staple_expected": stap_exp,
                              "staple_min": stap_min, "planted_staple_ha_weighted": planted_staple,
                              "capacity_status": st2, "capacity_t": cap,
                              "capacity_pct": 100 * cap / REF if cap else None}
    print("stress", scale, out[f"stress_{scale}"], flush=True)

# Baseline evaluation
base_plan = {"winter": {(d, c): par["baseline"][c][d] for d in au.D for c in au.W_CROPS},
             "summer": {(d, c, i): par["baseline"][c][d] for d in au.D for c in au.L_CROPS for i in au.INF}}
bev = au.evaluate_plan(par, base_plan)
out["baseline"] = {"per": {f"{s[0]}_{s[1]}": r for s, r in bev.items()},
                    "margin": sum(par["prob"][s] * r["margin"] for s, r in bev.items() if "margin" in r),
                    "staple_expected": sum(par["prob"][s] * r["staple"] for s, r in bev.items() if "staple" in r),
                    "staple_min": min(r["staple"] for r in bev.values() if "staple" in r)}
print("baseline", out["baseline"]["margin"], out["baseline"]["staple_expected"], out["baseline"]["staple_min"], flush=True)

Path(au.BASE / "data/processed/audit_v4_1_work/info_stress.json").write_text(json.dumps(out, indent=1, default=str))
print("done")
