"""Version 5.2 addendum driver: the capped ladder at scaled water anchors.

This file is new in the version 5.2 addendum. It changes no existing
file and no existing input. It imports src/allocation_model_v5.py as
a library, unchanged, and reuses the ladder, ceiling and packing
helpers of src/allocation_model_v5_1_addendum.py unchanged.

The version 5.1 addendum solved two combinations separately: the
relaxed ladder at district water budgets scaled to 0.90 and to 0.80
of the version 5 anchor of 11.00 billion cubic metres, and the capped
ladder at the full anchor under the named rotation and market sanity
caps in CAP_SHARE (wheat 0.50, rice 0.35, maize 0.40 in each season,
sugar beet 0.30, potatoes 0.15 of district physical land in each
season). This driver solves the combination the addendum did not:
the capped ladder at the two scaled anchors, 9.90 and 8.80 billion
cubic metres. The cost of each rung is taken against the capped
unconstrained optimum at the same anchor, and every figure is
compared in the output record against the capped ladder at the full
anchor in data/processed/results_v5_1_caps.json.

Usage, with the project venv python:
  .venv/bin/python src/allocation_model_v5_2_capped_scaled.py

Outputs:
  data/processed/results_v5_2_capped_scaled.json (unrounded results)
  data/processed/run_v5_2_capped_scaled.txt (this run log)
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import allocation_model_v5 as m
import allocation_model_v5_1_addendum as add

BASE_DIR = Path(__file__).resolve().parents[1]
PROC_DIR = BASE_DIR / "data" / "processed"
LEVELS = add.LEVELS
SCALES = (0.90, 0.80)


class Tee:
    """Write stdout to the terminal and to the run log at once."""

    def __init__(self, *streams):
        self.streams = streams

    def write(self, data):
        for s in self.streams:
            s.write(data)

    def flush(self):
        for s in self.streams:
            s.flush()


def main():
    log_path = PROC_DIR / "run_v5_2_capped_scaled.txt"
    log_fh = open(log_path, "w")
    sys.stdout = Tee(sys.__stdout__, log_fh)
    try:
        par = m.load_all()
        m.print_header(par)
        print("\n" + "=" * 76)
        print("VERSION 5.2 ADDENDUM: THE CAPPED LADDER AT SCALED WATER ANCHORS")
        print("The version 5 model and its inputs are unchanged. The named")
        print("rotation and market sanity caps of the version 5.1 caps run are")
        print("applied at district water budgets scaled to 0.90 and to 0.80 of")
        print("the version 5 anchor of 11.00 billion cubic metres, giving total")
        print("anchors of 9.90 and 8.80 billion cubic metres. The cost of each")
        print("rung is taken against the capped unconstrained optimum at the")
        print("same anchor. Rungs above the capped ceiling share of their own")
        print("anchor are infeasible by the ceiling maximisation of that")
        print("anchor, not by solver status alone.")
        print("=" * 76)

        full = json.loads((PROC_DIR / "results_v5_1_caps.json").read_text())
        full_frontier = full["frontier_caps"]
        full_cost = full["cost_vs_capped_unconstrained"]
        full_ceiling_share = full["ceiling_caps_share"]
        full_ceiling_tonnes = full["ceiling_caps_tonnes"]

        results = {
            "run": "version 5.2 addendum, capped ladder at scaled water anchors",
            "model": "src/allocation_model_v5.py unchanged",
            "caps_share_of_district_physical_land": m.CAP_SHARE,
            "anchor_bcm_version5": m.ANCHOR_BCM,
            "levels": LEVELS,
            "reference_tonnes": par["reference_t"],
            "full_anchor_reference": {
                "source": "data/processed/results_v5_1_caps.json",
                "budget_total_bcm": m.ANCHOR_BCM,
                "frontier_caps": full_frontier,
                "cost_vs_capped_unconstrained": full_cost,
                "ceiling_caps_share": full_ceiling_share,
                "ceiling_caps_tonnes": full_ceiling_tonnes,
            },
        }

        for scale in SCALES:
            share, tonnes = add.ceiling(
                par, caps=True, budget_scale=scale,
                label=f"with named caps, anchor scale {scale:.2f}")
            block = add.ladder(
                par, LEVELS, caps=True, budget_scale=scale,
                label=f"with named caps, anchor scale {scale:.2f}")
            entry = add.pack(block)
            comparison = {"margin_delta_vs_full_anchor": {},
                          "cost_delta_vs_full_anchor": {}}
            for lv in LEVELS:
                key = f"{lv:.2f}"
                mine_margin = entry["frontier"][key]
                mine_cost = entry["cost_vs_unconstrained"][key]
                comparison["margin_delta_vs_full_anchor"][key] = (
                    None if mine_margin is None else mine_margin - full_frontier[key])
                comparison["cost_delta_vs_full_anchor"][key] = (
                    None if mine_cost is None or full_cost[key] is None
                    else mine_cost - full_cost[key])
            comparison["ceiling_share_delta_vs_full_anchor"] = (
                None if share is None else share - full_ceiling_share)
            comparison["ceiling_tonnes_delta_vs_full_anchor"] = (
                None if tonnes is None else tonnes - full_ceiling_tonnes)
            results[f"anchor_{scale:.2f}"] = {
                "budget_total_bcm": m.ANCHOR_BCM * scale,
                "frontier_caps": entry["frontier"],
                "cost_vs_capped_unconstrained_same_anchor": entry["cost_vs_unconstrained"],
                "cost_vs_next_lower": entry["cost_vs_next_lower"],
                "staple_min_tonnes": entry["staple_min_tonnes"],
                "status": entry["status"],
                "ceiling_caps_share": share,
                "ceiling_caps_tonnes": tonnes,
                "comparison_vs_full_anchor": comparison,
            }
            print(f"\nCOMPARISON, anchor scale {scale:.2f} against the capped ladder "
                  f"at the full anchor (results_v5_1_caps.json)")
            print(f"  capped ceiling: this anchor {share} ({tonnes} tonnes) | "
                  f"full anchor {full_ceiling_share} ({full_ceiling_tonnes} tonnes)")
            for lv in LEVELS:
                key = f"{lv:.2f}"
                print(f"  level {lv*100:.0f} percent: margin this anchor "
                      f"{entry['frontier'][key]} | full anchor {full_frontier[key]} | "
                      f"cost this anchor {entry['cost_vs_unconstrained'][key]} | "
                      f"full anchor {full_cost[key]}")

        path = PROC_DIR / "results_v5_2_capped_scaled.json"
        with open(path, "w") as fh:
            json.dump(results, fh, indent=1, default=float)
        print(f"\nUnrounded results written to data/processed/results_v5_2_capped_scaled.json")
    finally:
        sys.stdout = sys.__stdout__
        log_fh.close()


if __name__ == "__main__":
    main()
