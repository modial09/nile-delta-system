"""Check 1, script B: probabilities, reference tonnage, frontier arithmetic,
and the wait and see recompute. Uses load_all() for exact probabilities and
the per scenario margins printed in the main run log for the WS sum."""
import importlib.util
import re

ROOT = "/home/hatch/workspace/mit-projects/nile-delta-system"
spec = importlib.util.spec_from_file_location("m", ROOT + "/src/allocation_model_v4_1.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
par = m.load_all()

probs = par["inflow"]["probs"]
print("inflow probs:", {k: round(v, 8) for k, v in probs.items()})
print("sum inflow probs:", sum(probs.values()))
print("sum combined scenario probs:", sum(par["prob"].values()))
print("budgets BCM:", {k: round(v, 4) for k, v in par["inflow"]["budgets_bcm"].items()})
tb = sum(probs[i] * par["inflow"]["budgets_bcm"][i] for i in m.INFLOW_STATES)
print(f"true mean budget recomputed: {tb:.4f} BCM (note prints 10.9844)")
print(f"reference tonnage recomputed: {par['reference_t']:,.2f} (note prints 12,254,407)")
print("reference by crop:", {c: round(v, 1) for c, v in par["reference_by_crop"].items()})
print("component sum:", sum(par["reference_by_crop"].values()))

# Frontier arithmetic from the margins printed in Results Note v4.2
fr = {0.0: 403078762407, 0.50: 297739198932, 0.60: 262520406731,
      0.70: 223222240454, 0.75: 202983384826, 0.80: 175143528384}
levels = sorted(fr)
print("\nfrontier differences recomputed from printed margins:")
for a, b in zip(levels, levels[1:]):
    print(f"  vs unconstrained at {b:.2f}: {fr[0.0]-fr[b]:,} | vs next lower: {fr[a]-fr[b]:,}")
mono = all(fr[a] > fr[b] for a, b in zip(levels, levels[1:]))
print("frontier strictly decreasing in the floor:", mono)
print(f"ceiling ratio: {9833867/par['reference_t']*100:.4f} percent (note prints 80.25)")
print(f"no reserve ceiling ratio: {11144080/par['reference_t']*100:.4f} (note prints 90.94)")
print(f"scaled ceiling ratio: {9266626/par['reference_t']*100:.4f} (note prints 75.62)")
print(f"capped ceiling ratio: {9490156/par['reference_t']*100:.4f} (note prints 77.44)")
print(f"stress cap 0.90 ratio: {9049077/par['reference_t']*100:.4f} (note prints 73.84)")
print(f"stress cap 0.80 ratio: {8264287/par['reference_t']*100:.4f} (note prints 67.44)")
print(f"baseline expected share: {8908274/par['reference_t']*100:.4f} (note prints 72.69)")
print(f"baseline worst share: {7367358/par['reference_t']*100:.4f} (note prints 60.12)")
print(f"accounting difference: {403078762407-86006146997:,} (note prints 317,072,615,410)")
print(f"difference as pct of baseline: {100*(403078762407-86006146997)/86006146997:.2f} (note prints 368.66)")

# Wait and see recompute: exact probabilities times the scenario margins
# printed in the run log.
log = open(ROOT + "/data/processed/run_v4_1_main.txt").read()
ws_terms = re.findall(r"wait and see (\w+): scenario margin EGP ([\d,]+) probability", log)
ws = 0.0
for name, val in ws_terms:
    i, l = name.rsplit("_", 1)
    ws += par["prob"][(i, l)] * float(val.replace(",", ""))
print(f"\nWS recomputed from log margins and exact probs: {ws:,.0f} (log prints 198,927,633,193)")
print(f"EVPI recomputed: {ws - fr[0.80]:,.0f} (note prints 23,784,104,809)")
print(f"penalised VSS recomputed: {fr[0.80] - 167535664790:,} (note prints 7,607,863,594)")
print(f"robustness floor reference: {0.80*par['reference_t']:,.1f} (note prints 9,803,526)")
