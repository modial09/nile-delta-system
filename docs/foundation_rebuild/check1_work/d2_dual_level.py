"""Check 1, script D2: pin down the dual level. The build computes the dual
floor as the ceiling share minus 0.001. Reconstruct that level from the
printed ceiling tonnage and re solve the relaxation there."""
import importlib.util

import pulp

ROOT = "/home/hatch/workspace/mit-projects/nile-delta-system"
spec = importlib.util.spec_from_file_location("m", ROOT + "/src/allocation_model_v4_1.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
par = m.load_all()
ref = par["reference_t"]


def damietta(prob):
    for name, con in prob.constraints.items():
        if name.startswith("Water_") and name.endswith("_normal_expected"):
            rest = name[len("Water_"):]
            dname = rest[: -len("normal_expected") - 1].replace("_", " ")
            if dname == "Damietta":
                raw = abs(float(con.pi)) / 1000.0
                return raw / par["prob"][("normal", "expected")]
    return None


share = 9833867.0 / ref
for lvl, label in ((share - 0.001, "reconstructed exact dual level"),
                   (0.8015, "rounded 80.15 percent level")):
    prob, v = m.build(par, floor_share=lvl, relax=True)
    st = m.solve(prob, gap=0.0)
    print(f"{label}: floor {lvl:.7f} status {st} "
          f"objective {float(pulp.value(prob.objective)):,.0f} "
          f"Damietta normal expected dual {damietta(prob):,.2f}")
print("run log prints: objective 174,088,745,148 and Damietta 19.17")
