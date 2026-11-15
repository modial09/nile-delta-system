"""Plan precision recovery for version 4.1.

Written as a separate script so that src/allocation_model_v4_1.py
stays unchanged. The method, in full:

  Step one. For a given floor level, solve the original mixed
  integer problem with CBC exactly as the model code solves it
  (model.build plus model.solve). From that solve, capture the
  keep binary value for every governorate, activity and scenario.
  Binaries are exact 0 or 1, so the CBC solution file truncation
  that rounded the planted areas does not touch them.

  Step two. Rebuild the same problem as a linear program (the
  model build with relax=True, so every keep variable is
  continuous), fix every keep variable to its captured value by
  setting its lower and upper bounds equal to that value, and
  solve the linear program with HiGHS through the PuLP HiGHS
  interface. HiGHS returns variable values through its API at
  full float precision, bypassing the CBC solution file, which
  carries about 8 significant figures.

  Step three. Read the winter and late planting areas from the
  HiGHS solution and save them with the model save_plan function,
  which writes float_format %.17g, with the same columns and the
  same row order as the files it replaces.

An optional raised floor variant is supported for the recovery
linear program only: its floor share is lifted so that the floor
tonnage rises by a stated number of tonnes. The mixed integer
step always runs at the original floor. No model parameter,
tolerance, objective or constraint in the model file is changed
by this script, and no run log is touched.
"""

import json
import sys
import time
from pathlib import Path

import pulp

BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE_DIR / "src"))

import allocation_model_v4_1 as model  # noqa: E402

PROC_DIR = BASE_DIR / "data" / "processed"

LEVELS = [
    (0.50, "plan_v4_1_floor50.csv"),
    (0.60, "plan_v4_1_floor60.csv"),
    (0.70, "plan_v4_1_floor70.csv"),
    (0.75, "plan_v4_1_floor75.csv"),
    (0.80, "plan_v4_1_floor80.csv"),
    (0.80, "plan_v4_1_robust_plan.csv"),
]


def capture_keep_values(par, floor_share):
    """Solve the original mixed integer problem with CBC, exactly
    as the model code does, and return the keep binary values keyed
    by solver variable name, plus the CBC objective value."""
    prob, _vars = model.build(par, floor_share=floor_share)
    status = model.solve(prob)
    if status != "Optimal":
        raise RuntimeError(f"CBC status {status} at floor {floor_share}")
    keep = {}
    for var in prob.variables():
        if var.name.startswith("k_"):
            keep[var.name] = 1.0 if float(var.value()) > 0.5 else 0.0
    if len(keep) != 768:
        raise RuntimeError(f"expected 768 keep variables, found {len(keep)}")
    return keep, float(pulp.value(prob.objective))


def recover_plan(par, floor_share, keep, raise_tonnes=0.0):
    """Rebuild the problem as a linear program with every keep
    variable fixed to its captured value, solve it with HiGHS, and
    return the plan plus the HiGHS objective value."""
    lp_floor_share = floor_share + (raise_tonnes / par["reference_t"])
    prob, vars_ = model.build(par, floor_share=lp_floor_share, relax=True)
    fixed_count = 0
    for var in prob.variables():
        if var.name.startswith("k_"):
            value = keep[var.name]
            var.lowBound = value
            var.upBound = value
            fixed_count += 1
    if fixed_count != len(keep):
        raise RuntimeError(f"fixed {fixed_count} keep variables, captured {len(keep)}")
    prob.solve(pulp.HiGHS(msg=False))
    status = pulp.LpStatus[prob.status]
    if status != "Optimal":
        raise RuntimeError(f"HiGHS status {status} at floor {floor_share}")
    plan = model.plan_of(vars_)
    return plan, float(pulp.value(prob.objective))


def main():
    raise_map = {}
    if len(sys.argv) > 1:
        # Optional argument form: floor80:0.25 lifts the recovery
        # linear program floor for that level by 0.25 tonnes.
        for item in sys.argv[1:]:
            name, _, tonnes = item.partition(":")
            raise_map[name] = float(tonnes)
    par = model.load_all()
    print(f"reference tonnage {par['reference_t']!r}")
    summary = {}
    for floor_share, filename in LEVELS:
        t0 = time.time()
        keep, cbc_objective = capture_keep_values(par, floor_share)
        raise_tonnes = raise_map.get(filename, 0.0)
        plan, lp_objective = recover_plan(par, floor_share, keep,
                                          raise_tonnes=raise_tonnes)
        out_path = PROC_DIR / filename
        model.save_plan(plan, out_path, floor_share)
        variant = "raised" if raise_tonnes else "plain"
        summary[filename] = {
            "floor_share": floor_share,
            "variant": variant,
            "raise_tonnes": raise_tonnes,
            "keep_ones": int(sum(keep.values())),
            "cbc_objective": cbc_objective,
            "highs_lp_objective": lp_objective,
            "path": str(out_path),
            "seconds": time.time() - t0,
        }
        print(f"{filename}: floor {floor_share} variant {variant} "
              f"keep ones {int(sum(keep.values()))} of {len(keep)} "
              f"CBC objective {cbc_objective!r} "
              f"HiGHS LP objective {lp_objective!r} "
              f"seconds {time.time() - t0:.1f}")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
