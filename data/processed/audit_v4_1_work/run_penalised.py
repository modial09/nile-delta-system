import json, sys
from pathlib import Path
import pulp
sys.path.insert(0, str(Path(__file__).parent))
import au

par = au.load()
# Rebuild the EV plan exactly as in run_info_stress.py
true_budget = sum(par["inflow"]["probs"][i] * par["inflow"]["budgets_bcm"][i] for i in au.INF)
mean_price = {c: sum(au.LPROB[l] * par["price"][c][l] for l in au.LAY) for c in au.A_CROPS}
mean_yield = {c: {d: sum(au.LPROB[l] * par["yield"][c][l][d] for l in au.LAY) for d in au.D} for c in au.A_CROPS}
price_o = {c: {l: mean_price[c] for l in au.LAY} for c in au.A_CROPS}
yld_o = {c: {l: mean_yield[c] for l in au.LAY} for c in au.A_CROPS}
tot_phys = sum(par["physical"].values())
bud = {(d, i): true_budget * 1e9 * par["physical"][d] / tot_phys for d in au.D for i in au.INF}
p_m = au.modified(par, price=price_o, budget=bud, **{"yield": yld_o})
prob, v = au.build(p_m, floor=0.80, single=("normal", "expected"))
st = au.solve(prob)
ev_single = au.plan_of(v)
ev_plan = {"winter": ev_single["winter"],
           "summer": {(d, c, i): ev_single["summer"][(d, c, "normal")] for d in au.D for c in au.L_CROPS for i in au.INF}}
pen_total = 0.0
per = {}
for s in par["scenarios"]:
    prob2, v2 = au.build(par, floor=0.80, fixed=ev_plan, single=s, penalise=25000.0, bound="cell")
    st2 = au.solve(prob2)
    if st2 != "Optimal":
        per[f"{s[0]}_{s[1]}"] = {"status": st2}
        continue
    obj = float(pulp.value(prob2.objective))
    short = float(v2["shortfall"][s].value())
    m_before, stap = au.scenario_margin_staple(par, v2, s, ev_plan)
    per[f"{s[0]}_{s[1]}"] = {"status": st2, "penalised_margin": obj, "shortfall": short, "margin_before_penalty": m_before}
    pen_total += par["prob"][s] * obj
    print(s, round(obj), "shortfall", round(short), "margin_before", round(m_before), flush=True)
out = {"penalised_eev": pen_total, "per": per,
       "penalised_vss_mine": 175143528383.6324 - pen_total}
Path(au.BASE/"data/processed/audit_v4_1_work/penalised.json").write_text(json.dumps(out, indent=1))
print("penalised EEV", pen_total, "VSS mine", out["penalised_vss_mine"])
