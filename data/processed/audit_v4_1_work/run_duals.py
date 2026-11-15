import json
import re
import sys
from pathlib import Path

import pulp

sys.path.insert(0, str(Path(__file__).parent))
import au

par = au.load()
out = {}

ceil_share = 9833866.8 / par["reference_t"]
for label, fl in [("ceil_minus_0.001", ceil_share - 0.001), ("labelled_0.8015", 0.8015)]:
    prob, v = au.build(par, floor=fl, relax=True)
    st = au.solve(prob)
    obj = float(pulp.value(prob.objective)) if st == "Optimal" else None
    duals = {}
    for name, con in prob.constraints.items():
        if name.startswith("Water_"):
            rest = name[len("Water_"):]
            for s in par["scenarios"]:
                sk = f"{s[0]}_{s[1]}"
                if rest.endswith("_" + sk):
                    dname = rest[: -len(sk) - 1].replace("_", " ")
                    raw = abs(float(con.pi)) if con.pi is not None else 0.0
                    duals[(dname, s[0], s[1])] = raw / par["prob"][s]
    ranges = {}
    for (i, l) in [("dry", "expected"), ("normal", "expected"), ("high", "expected"), ("dry", "low")]:
        vals = {d: duals.get((d, i, l), 0.0) for d in au.D}
        binding = {d: x for d, x in vals.items() if x > 0.01}
        ranges[f"{i}_{l}"] = {"values": vals, "min_binding": min(binding.values()) if binding else None,
                              "max_binding": max(binding.values()) if binding else None,
                              "n_binding": len(binding),
                              "argmin": min(binding, key=binding.get) if binding else None,
                              "argmax": max(binding, key=binding.get) if binding else None}
    out[label] = {"floor": fl, "status": st, "objective": obj, "ranges": ranges}
    print(label, fl, st, obj)
    for k, r in ranges.items():
        print("   ", k, r["min_binding"], r["max_binding"], r["n_binding"], r["argmin"], r["argmax"])

# Raw to conditional conversion on the log table itself
log = (au.BASE / "data/processed/run_v4_1_main.txt").read_text()
rows = re.findall(r"^(.+?) \| (\w+)_(\w+) \| ([\d.]+) \| ([\d.]+)$", log, flags=re.M)
maxgap = 0.0
n = 0
for dname, i, l, raw, cond in rows:
    p = par["prob"][(i, l)]
    expect = float(raw) / p
    gap = abs(expect - float(cond))
    maxgap = max(maxgap, gap)
    n += 1
out["log_conversion"] = {"cells": n, "max_gap_pounds_per_m3": maxgap}
print("log conversion cells", n, "max gap", maxgap)

Path(au.BASE / "data/processed/audit_v4_1_work/duals.json").write_text(json.dumps(out, indent=1, default=str))
print("done")
