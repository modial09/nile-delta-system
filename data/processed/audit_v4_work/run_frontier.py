import sys, time
sys.path.insert(0, ".")
from audit_load import load, DISTRICTS, WINTER, SUMMER_ALL, ALLC, STAPLES, INFLOW
from audit_model import make, solve, val
import pulp

P = load()
REF = P["reference_t"]

def margin_recompute(v, scen=None):
    """Recompute expected margin from solution values by hand."""
    rev = 0.0
    for s in (P["scenarios"] if not scen else [scen]):
        r = sum(P["price"][c][s[1]] * val(v["prod"][(d, c, s)]) for d in DISTRICTS for c in ALLC)
        rev += (1.0 if scen else P["prob"][s]) * r
    if scen:
        cost = sum(P["cost"][c] * val(v["xw"][(d, c)]) for d in DISTRICTS for c in WINTER)
        cost += sum(P["cost"][c] * val(v["xs"][(d, c, scen[0])]) for d in DISTRICTS for c in SUMMER_ALL)
    else:
        cost = sum(P["cost"][c] * val(v["xw"][(d, c)]) for d in DISTRICTS for c in WINTER)
        cost += sum(P["inflow"]["probs"][i] * P["cost"][c] * val(v["xs"][(d, c, i)])
                    for d in DISTRICTS for c in SUMMER_ALL for i in INFLOW)
    return rev - cost, rev, cost

for floor, expect in [(0.0, 429588780373), (0.70, 194764695263)]:
    t0 = time.time()
    prob, v = make(P, floor=floor, mip=True)
    st = solve(prob, gap=0.001)
    obj = val(prob.objective)
    hand, rev, cost = margin_recompute(v)
    print(f"floor {floor}: status {st} objective {obj:,.1f} builder {expect:,} diff {obj-expect:,.1f} "
          f"hand recomputed {hand:,.1f} obj minus hand {obj-hand:,.1f} ({time.time()-t0:.0f}s)")
    # abandonment inspection on this solution
    n_ab = n_kept = 0
    worst = []
    minshare_kept = 9.9
    for s in P["scenarios"]:
        for d in DISTRICTS:
            for c in ALLC:
                x = val(v["xw"][(d, c)]) if c in WINTER else val(v["xs"][(d, c, s[0])])
                if x < 1.0:
                    continue
                a = val(v["kept"][(d, c, s)])
                w = val(v["wat"][(d, c, s)])
                q = val(v["prod"][(d, c, s)])
                if a < 0.01 * x:
                    n_ab += 1
                    worst.append((s, d, c, x, a, w, q))
                else:
                    n_kept += 1
                    share = w / (P["wreq"][c] * a) if a > 0 else 0
                    minshare_kept = min(minshare_kept, share)
    print(f"  planted cells checked: abandoned {n_ab}, kept {n_kept}, min water share among kept {minshare_kept:.4f}")
    for row in worst[:8]:
        s, d, c, x, a, w, q = row
        print(f"  ABANDONED {s} {d} {c}: planted {x:,.1f} ha kept {a:.4f} water {w:,.2f} m3 output {q:.4f} t cost charged {P['cost'][c]*x:,.0f} EGP")

# Solver integrity: same 70 percent problem at tighter gap
prob, v = make(P, floor=0.70, mip=True)
st = solve(prob, gap=0.0, tl=1200)
print(f"floor 0.70 gap 0: status {st} objective {val(prob.objective):,.1f}")

# Stress: capacity and choice at 0.90 and 0.80, own code
for scale in (0.90, 0.80):
    prob, v = make(P, floor=0.0, mip=True, budget_scale=scale)
    st = solve(prob, gap=0.001)
    stap_exp = sum(P["prob"][s] * val(v["staple"][s]) for s in P["scenarios"])
    stap_min = min(val(v["staple"][s]) for s in P["scenarios"])
    planted_staple = {}
    for c in STAPLES:
        if c in WINTER:
            planted_staple[c] = sum(val(v["xw"][(d, c)]) for d in DISTRICTS)
        else:
            planted_staple[c] = sum(P["inflow"]["probs"][i] * val(v["xs"][(d, c, i)]) for d in DISTRICTS for i in INFLOW)
    print(f"stress {scale} choice: status {st} margin {val(prob.objective):,.1f} staple expected {stap_exp:,.1f} min {stap_min:,.1f} planted staples {planted_staple}")
    prob2, v2 = make(P, objective="maxmin", mip=False, budget_scale=scale)
    st2 = solve(prob2, gap=0.0)
    print(f"stress {scale} capacity LP: status {st2} t {val(v2['t']):,.1f} = {100*val(v2['t'])/REF:.2f} pct")
    # max margin LP relaxation at 0.80 with staples forced zero vs free: check no staple incentive
    prob3, v3 = make(P, floor=0.0, mip=False, budget_scale=scale)
    st3 = solve(prob3, gap=0.0)
    se3 = sum(P["prob"][s] * val(v3["staple"][s]) for s in P["scenarios"])
    print(f"stress {scale} choice LP relaxation: margin {val(prob3.objective):,.1f} staple expected {se3:,.1f}")
