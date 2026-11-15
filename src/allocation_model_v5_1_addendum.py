"""Version 5.1 addendum driver: two economic runs on the version 5 build.

This file is new in the version 5.1 addendum. It changes no version 5
file and no version 5 input. It imports src/allocation_model_v5.py as
a library and calls its loader, its model builder and its solver with
two settings the version 5 modes did not combine with the full ladder:

  Run 1, mode anchor. The full guarantee ladder and the ceiling at
  district water budgets scaled to 0.90 and to 0.80 of the version 5
  anchor of 11.00 billion cubic metres, solved beside the same ladder
  at the anchor itself so the three columns stand in one record. The
  anchor column must reproduce data/processed/results_v5_main.json
  exactly, and the scaled unconstrained margins and ceilings must
  reproduce the stress figures printed in paper/Results_Note_v5.md
  Section 6, which came from the same builder at the same scales with
  no floor. The script prints those comparisons in its log.

  Run 2, mode caps. The full ladder and the ceiling under the named
  rotation and market sanity caps carried in CAP_SHARE of the version
  5 module, the same values as version 4.1 (wheat 0.50, rice 0.35,
  maize 0.40 in each season, sugar beet 0.30, potatoes 0.15 of
  district physical land in each season). The version 5 caps mode
  never solved the 65 percent rung and saved no cost column; this run
  solves every rung of the ladder and saves the cost of each rung
  against the capped unconstrained optimum. Shared rungs must
  reproduce data/processed/results_v5_caps.json, and the script
  prints that comparison in its log.

Usage, with the project venv python:
  .venv/bin/python src/allocation_model_v5_1_addendum.py anchor
  .venv/bin/python src/allocation_model_v5_1_addendum.py caps
"""

import json
import sys
import time
from pathlib import Path

import pulp

sys.path.insert(0, str(Path(__file__).resolve().parent))
import allocation_model_v5 as m

BASE_DIR = Path(__file__).resolve().parents[1]
PROC_DIR = BASE_DIR / "data" / "processed"

LEVELS = [0.0, 0.50, 0.60, 0.65, 0.70, 0.75, 0.80]

# Stress figures printed in paper/Results_Note_v5.md Section 6, from
# the version 5 stress runs at scaled budgets with no floor. Run 1
# must reproduce them at rung 0 and at the ceiling of each scale.
STRESS_REFERENCE = {
    0.90: {"margin": 520907656409.0, "ceiling_tonnes": 9295584.0},
    0.80: {"margin": 476620802204.0, "ceiling_tonnes": 8491820.0},
}


def ladder(par, levels, caps=False, budget_scale=1.0, label=""):
    """Solve the ladder at one setting. Returns one dict per level
    with the status, the expected margin and both cost columns."""
    print(f"\nFRONTIER {label} caps={caps} budget_scale={budget_scale:.2f}")
    print("Level percent | status | expected margin EGP | cost vs unconstrained EGP | cost vs next lower level EGP")
    out = {}
    unc_margin = None
    prev_margin = None
    for lv in levels:
        t0 = time.time()
        prob, v = m.build(par, floor_share=lv, caps=caps, budget_scale=budget_scale)
        st = m.solve(prob)
        if st != "Optimal":
            print(f"{lv*100:.0f} | {st} | none | none | none | seconds {time.time()-t0:.0f}")
            out[lv] = {"status": st, "margin": None,
                       "cost_vs_unconstrained": None, "cost_vs_next_lower": None,
                       "staple_min": None, "staple_expected": None}
            continue
        margin = float(pulp.value(prob.objective))
        if lv == 0:
            unc_margin = margin
        cost_unc = (unc_margin - margin) if unc_margin is not None else 0.0
        cost_prev = (prev_margin - margin) if prev_margin is not None else 0.0
        res = m.scenario_results(par, v)
        print(f"{lv*100:.0f} | {st} | {margin:,.2f} | {cost_unc:,.2f} | {cost_prev:,.2f} | seconds {time.time()-t0:.0f}")
        print(f"    expected staple tonnes {res['staple_expected']:,.0f} | minimum scenario staple tonnes {res['staple_min']:,.0f}")
        out[lv] = {"status": st, "margin": margin,
                   "cost_vs_unconstrained": cost_unc, "cost_vs_next_lower": cost_prev,
                   "staple_min": res["staple_min"], "staple_expected": res["staple_expected"]}
        prev_margin = margin
    return out


def ceiling(par, caps=False, budget_scale=1.0, label=""):
    prob, v = m.build(par, caps=caps, objective="maxstaple", budget_scale=budget_scale)
    st = m.solve(prob)
    if st != "Optimal":
        print(f"CEILING {label}: status {st}")
        return None, None
    t = float(v["t"].value())
    share = t / par["reference_t"]
    print(f"CEILING {label}: maximum held staple tonnage in every scenario {t:,.2f} tonnes, "
          f"which is {100*share:.4f} percent of the reference tonnage {par['reference_t']:,.2f}")
    return share, t


def pack(block):
    """Reshape one ladder result into the version 5 JSON style."""
    return {
        "frontier": {f"{lv:.2f}": block[lv]["margin"] for lv in LEVELS},
        "cost_vs_unconstrained": {f"{lv:.2f}": block[lv]["cost_vs_unconstrained"] for lv in LEVELS},
        "cost_vs_next_lower": {f"{lv:.2f}": block[lv]["cost_vs_next_lower"] for lv in LEVELS},
        "staple_min_tonnes": {f"{lv:.2f}": block[lv]["staple_min"] for lv in LEVELS},
        "status": {f"{lv:.2f}": block[lv]["status"] for lv in LEVELS},
    }


def anchor_mode():
    par = m.load_all()
    m.print_header(par)
    print("\n" + "=" * 76)
    print("VERSION 5.1 ADDENDUM RUN 1: THE LADDER AT SCALED WATER ANCHORS")
    print("The version 5 model and its inputs are unchanged. District water")
    print("budgets are scaled to 0.90 and to 0.80 of the version 5 anchor of")
    print("11.00 billion cubic metres, giving total anchors of 9.90 and 8.80")
    print("billion cubic metres. The ladder at the anchor itself is solved in")
    print("the same run so the three columns stand in one record, and it is")
    print("checked against data/processed/results_v5_main.json below. Rungs")
    print("above the ceiling share of their own anchor are infeasible by the")
    print("ceiling maximisation of that anchor, not by solver status alone.")
    print("=" * 76)
    results = {"run": "version 5.1 addendum run 1, ladder at scaled water anchors",
               "model": "src/allocation_model_v5.py unchanged",
               "anchor_bcm_version5": m.ANCHOR_BCM,
               "levels": LEVELS,
               "reference_tonnes": par["reference_t"]}
    blocks = {}
    for scale in (1.00, 0.90, 0.80):
        share, tonnes = ceiling(par, budget_scale=scale,
                                label=f"anchor scale {scale:.2f}")
        block = ladder(par, LEVELS, budget_scale=scale,
                       label=f"anchor scale {scale:.2f}")
        entry = pack(block)
        entry["budget_total_bcm"] = m.ANCHOR_BCM * scale
        entry["ceiling_share"] = share
        entry["ceiling_tonnes"] = tonnes
        blocks[scale] = entry
        results[f"anchor_{scale:.2f}"] = entry
    print("\nCHECKS AGAINST THE VERSION 5 RECORD")
    saved = json.loads((PROC_DIR / "results_v5_main.json").read_text())
    ok = True
    for lv in (0.0, 0.50, 0.60, 0.70, 0.75, 0.80):
        mine = blocks[1.00]["frontier"][f"{lv:.2f}"]
        theirs = saved["frontier_primary"][f"{lv:.2f}"]
        same = (mine is None and theirs is None) or (
            mine is not None and theirs is not None and abs(mine - theirs) < 0.01)
        ok = ok and same
        print(f"  anchor 1.00 level {lv*100:.0f} percent: this run {mine} | version 5 record {theirs} | match {same}")
    diff = abs(blocks[1.00]["ceiling_share"] - saved["ceiling_primary_share"])
    print(f"  anchor 1.00 ceiling share: this run {blocks[1.00]['ceiling_share']} | version 5 record "
          f"{saved['ceiling_primary_share']} | difference {diff:.2e}")
    ok = ok and diff < 1e-9
    for scale, ref in STRESS_REFERENCE.items():
        got_m = blocks[scale]["frontier"]["0.00"]
        got_c = blocks[scale]["ceiling_tonnes"]
        m_ok = got_m is not None and abs(got_m - ref["margin"]) < 1.0
        c_ok = got_c is not None and abs(got_c - ref["ceiling_tonnes"]) < 1.0
        ok = ok and m_ok and c_ok
        print(f"  anchor {scale:.2f} rung 0 margin: this run {got_m:,.2f} | Results_Note_v5 Section 6 "
              f"{ref['margin']:,.0f} | match {m_ok}")
        print(f"  anchor {scale:.2f} ceiling tonnes: this run {got_c:,.2f} | Results_Note_v5 Section 6 "
              f"{ref['ceiling_tonnes']:,.0f} | match {c_ok}")
    print(f"CHECK RESULT: {'all comparisons match' if ok else 'A COMPARISON FAILED, SEE LINES ABOVE'}")
    results["checks"] = {"anchor_1.00_reproduces_results_v5_main": True if ok else False}
    path = PROC_DIR / "results_v5_1_scaled_anchor.json"
    with open(path, "w") as fh:
        json.dump(results, fh, indent=1, default=float)
    print(f"Unrounded results written to data/processed/results_v5_1_scaled_anchor.json")


def caps_mode():
    par = m.load_all()
    m.print_header(par)
    print("\n" + "=" * 76)
    print("VERSION 5.1 ADDENDUM RUN 2: THE CAPPED PRICE LIST ON VERSION 5")
    print("The named rotation and market sanity caps of version 4.1 and of")
    print("the version 5 caps mode are applied to the version 5 build: wheat")
    print("0.50, rice 0.35, maize 0.40 in each season, sugar beet 0.30 and")
    print("potatoes 0.15 of district physical land in each season. Every rung")
    print("of the ladder is solved, including the 65 percent rung the")
    print("version 5 caps mode did not solve, and the cost of each rung is")
    print("taken against the capped unconstrained optimum of this same run.")
    print("Rungs above the capped ceiling share are infeasible by the capped")
    print("ceiling maximisation, not by solver status alone.")
    print("=" * 76)
    share, tonnes = ceiling(par, caps=True, label="with named caps")
    block = ladder(par, LEVELS, caps=True, label="with named caps")
    entry = pack(block)
    results = {"run": "version 5.1 addendum run 2, capped price list on version 5",
               "model": "src/allocation_model_v5.py unchanged",
               "caps_share_of_district_physical_land": m.CAP_SHARE,
               "levels": LEVELS,
               "reference_tonnes": par["reference_t"],
               "frontier_caps": entry["frontier"],
               "cost_vs_capped_unconstrained": entry["cost_vs_unconstrained"],
               "cost_vs_next_lower": entry["cost_vs_next_lower"],
               "staple_min_tonnes": entry["staple_min_tonnes"],
               "status": entry["status"],
               "ceiling_caps_share": share,
               "ceiling_caps_tonnes": tonnes}
    print("\nCHECKS AGAINST THE VERSION 5 CAPS RECORD")
    saved = json.loads((PROC_DIR / "results_v5_caps.json").read_text())
    ok = True
    for lv in (0.0, 0.50, 0.60, 0.70, 0.75, 0.80):
        mine = entry["frontier"][f"{lv:.2f}"]
        theirs = saved["frontier_caps"][f"{lv:.2f}"]
        same = (mine is None and theirs is None) or (
            mine is not None and theirs is not None and abs(mine - theirs) < 0.01)
        ok = ok and same
        print(f"  capped level {lv*100:.0f} percent: this run {mine} | version 5 caps record {theirs} | match {same}")
    diff = abs(share - saved["ceiling_caps_share"]) if share is not None else None
    print(f"  capped ceiling share: this run {share} | version 5 caps record "
          f"{saved['ceiling_caps_share']} | difference {diff:.2e}")
    ok = ok and diff is not None and diff < 1e-9
    print(f"CHECK RESULT: {'all comparisons match' if ok else 'A COMPARISON FAILED, SEE LINES ABOVE'}")
    results["checks"] = {"reproduces_results_v5_caps_at_shared_rungs": True if ok else False}
    path = PROC_DIR / "results_v5_1_caps.json"
    with open(path, "w") as fh:
        json.dump(results, fh, indent=1, default=float)
    print(f"Unrounded results written to data/processed/results_v5_1_caps.json")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "anchor"
    if mode == "anchor":
        anchor_mode()
    elif mode == "caps":
        caps_mode()
    else:
        print(f"unknown mode {mode}")
