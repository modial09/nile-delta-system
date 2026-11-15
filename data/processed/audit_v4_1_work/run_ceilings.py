import json
import sys
import time
from pathlib import Path

import pulp

sys.path.insert(0, str(Path(__file__).parent))
import au

par = au.load()
out = {}

def ceil(p, label, relax, **kw):
    t0 = time.time()
    prob, v = au.build(p, objective="maxstaple", relax=relax, **kw)
    st = au.solve(prob)
    t = float(v["t"].value()) if st == "Optimal" else None
    out[label] = {"status": st, "t": t,
                  "pct": 100 * t / par["reference_t"] if t else None,
                  "seconds": round(time.time() - t0, 1)}
    print(label, out[label], flush=True)
    return t, v, st

# Linear ceilings for every variant
ceil(par, "primary_LP", True)
par_nr = au.modified(par, land_limit={d: {p: par["physical"][d] for p in au.POOLS} for d in au.D})
ceil(par_nr, "no_reserve_LP", True)
par_sc = au.modified(par, **{"yield": par["yield_scaled"]})
ceil(par_sc, "scaled_yields_LP", True)
ceil(par, "capped_LP", True, caps=True)
par_unc = au.modified(par, land_limit=par["land_limit_uncapped"])
ceil(par_unc, "uncapped_proportional_LP", True)

# Binary confirmation of the four headline ceilings
ceil(par, "primary_MIP", False)
ceil(par_nr, "no_reserve_MIP", False)
ceil(par_sc, "scaled_yields_MIP", False)
ceil(par, "capped_MIP", False, caps=True)
ceil(par_unc, "uncapped_proportional_MIP", False)

# Which families bind at the primary ceiling: one family relaxed at a time, LP form
par_noland = au.modified(par, land_limit={d: {p: 1e12 for p in au.POOLS} for d in au.D})
ceil(par_noland, "relax_no_land_LP", True)
bud = dict(par["budget"])
for d in au.D:
    bud[(d, "dry")] = par["budget"][(d, "dry")] * 3
ceil(au.modified(par, budget=bud), "relax_triple_dry_water_LP", True)
bud2 = {k: v * 3 for k, v in par["budget"].items()}
ceil(au.modified(par, budget=bud2), "relax_triple_all_water_LP", True)
scen_no_drought = [s for s in par["scenarios"] if s[0] != "drought"]
ceil(par, "relax_drop_drought_LP", True, min_scenarios=scen_no_drought)
scen_no_dry = [s for s in par["scenarios"] if s[0] != "dry"]
ceil(par, "relax_drop_dry_LP", True, min_scenarios=scen_no_dry)
scen_exp = [s for s in par["scenarios"] if s[1] == "expected"]
ceil(par, "relax_min_expected_layer_only_LP", True, min_scenarios=scen_exp)
ceil(par, "relax_no_min_share_LP", True, min_share=0.0)

# Named sensitivities on the ceiling, LP form
for duty in (5600.0, 6600.0):
    wr = dict(par["water_req"]); wr["Sugar beet"] = duty
    ceil(au.modified(par, water_req=wr), f"beet_duty_{int(duty)}_LP", True)
for kyv in (1.00, 1.40):
    ky = dict(par["ky"]); ky["Rice"] = kyv
    ceil(au.modified(par, ky=ky), f"rice_ky_{kyv}_LP", True)

# Binding detail at the primary LP ceiling: scenario staple values, land and water use
prob, v = au.build(par, objective="maxstaple", relax=True)
st = au.solve(prob)
t = float(v["t"].value())
det = {"t": t, "scenario_staple": {}, "land_use": {}, "water_use_frac": {}}
for s in par["scenarios"]:
    det["scenario_staple"][f"{s[0]}_{s[1]}"] = sum(
        float(pulp.value(v["prod"][(d, c, s)])) for d in au.D for c in au.STAPLES)
for d in au.D:
    det["land_use"][d] = {}
    det["land_use"][d]["winter"] = (sum(float(v["xw"][(d, c)].value()) for c in au.W_CROPS),
                                    par["land_limit"][d]["winter"])
    for i in au.INF:
        det["land_use"][d][f"summer_{i}"] = (sum(float(v["xs"][(d, c, i)].value()) for c in au.S_CROPS),
                                            par["land_limit"][d]["summer"])
        det["land_use"][d][f"nili_{i}"] = (sum(float(v["xs"][(d, c, i)].value()) for c in au.N_CROPS),
                                          par["land_limit"][d]["nili"])
    for s in par["scenarios"]:
        used = sum(float(v["wat"][(d, c, s)].value()) for c in au.A_CROPS)
        det["water_use_frac"][f"{d}_{s[0]}_{s[1]}"] = used / par["budget"][(d, s[0])]
# Ceiling solution planting of rice and sugar beet (LP)
det["rice_planted_by_inflow"] = {i: sum(float(v["xs"][(d, "Rice", i)].value()) for d in au.D) for i in au.INF}
det["beet_planted"] = sum(float(v["xw"][(d, "Sugar beet")].value()) for d in au.D)
out["primary_LP_binding_detail"] = det

Path(au.BASE / "data/processed/audit_v4_1_work/ceilings.json").write_text(json.dumps(out, indent=1, default=str))
print("done")
