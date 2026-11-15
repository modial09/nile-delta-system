import sys, time
sys.path.insert(0, ".")
from audit_load import load, DISTRICTS, WINTER, SUMMER_ALL, SUMMER_TRUE, NILI, INFLOW
from audit_model import make, solve, val
import pulp

P = load()
REF = P["reference_t"]
print(f"reference {REF:,.2f}")

def ceil(label, mip=True, **kw):
    t0 = time.time()
    prob, v = make(P, objective="maxmin", mip=mip, **kw)
    st = solve(prob, gap=0.0 if not mip else 0.0005)
    if st != "Optimal":
        print(f"{label}: status {st} ({time.time()-t0:.0f}s)")
        return None
    t = val(v["t"])
    print(f"{label}: {t:,.1f} t = {100*t/REF:.4f} percent ({time.time()-t0:.0f}s) status {st}")
    return t

# Base ceiling, LP relaxation and MIP
ceil("ceiling LP (partial keep allowed)", mip=False)
ceil("ceiling MIP (binary abandonment)", mip=True)

# Infeasibility of 80 percent floor as margin problem, LP and MIP status
for mip in (False, True):
    prob, v = make(P, floor=0.80, mip=mip)
    st = solve(prob)
    print(f"floor 80 percent {'MIP' if mip else 'LP'}: status {st}")

# Relaxations, LP for speed (LP and MIP base compared above)
INF = {d: {"winter": 1e9, "summer": 1e9} for d in DISTRICTS}
ceil("relax land removed LP", mip=False, land=INF)
ceil("relax dry water x3 LP", mip=False, budget_mult={"dry": 3.0})
ceil("relax all water x3 LP", mip=False, budget_scale=3.0)
ceil("relax drought state dropped from min LP", mip=False, drop_inflow={"drought"})
ceil("relax dry state dropped from min LP", mip=False, drop_inflow={"dry"})
ceil("relax min only in expected layer LP", mip=False, layers_only={"expected"})
ceil("relax min share 0.30 removed LP", mip=False, no_min_share=True)
# expected staple instead of every scenario minimum
prob, v = make(P, objective="maxexp", mip=False)
st = solve(prob, gap=0.0)
exp_t = sum(P["prob"][s] * val(v["staple"][s]) for s in P["scenarios"])
mn = min(val(v["staple"][s]) for s in P["scenarios"])
print(f"max expected staple LP: expected {exp_t:,.1f} = {100*exp_t/REF:.2f} pct, its own minimum scenario {mn:,.1f} = {100*mn/REF:.2f} pct")

# Capped ceiling
ceil("ceiling capped LP", mip=False, caps=True)
ceil("ceiling capped MIP", mip=True, caps=True)

# Alternative reserve constructions
base = P["baseline"]; phys = P["physical"]; ann = P["annual"]
# Alt A: equal split of annual unmodeled between the two pools
landA = {}
for d in DISTRICTS:
    w = sum(base[c][d] for c in WINTER); s = sum(base[c][d] for c in SUMMER_ALL)
    un = ann[d] - (w + s)
    landA[d] = {"winter": phys[d] - un / 2, "summer": phys[d] - un / 2}
ceil("Alt A equal split reserve LP", mip=False, land=landA)
# Alt B: three pools, Nili separate, split by true season modeled shares
landB = {}
for d in DISTRICTS:
    w = sum(base[c][d] for c in WINTER); s = sum(base[c][d] for c in SUMMER_TRUE); n = sum(base[c][d] for c in NILI)
    un = ann[d] - (w + s + n); tot = w + s + n
    landB[d] = {"winter": phys[d] - un * w / tot, "summer": phys[d] - un * s / tot, "nili": phys[d] - un * n / tot}
ceil("Alt B three pools (Nili separate) LP", mip=False, land=landB, land3=True)
# Alt C: builder split but reserve capped so the baseline pattern fits (limit at least observed modeled)
landC = {}
for d in DISTRICTS:
    landC[d] = {"winter": max(P["land_limit"][d]["winter"], P["reserve"][d]["w_obs"]),
                "summer": max(P["land_limit"][d]["summer"], P["reserve"][d]["s_obs"])}
ceil("Alt C reserve capped at baseline fit LP", mip=False, land=landC)
# Alt D: no reserve at all (upper bound of the reserve choice)
landD = {d: {"winter": phys[d], "summer": phys[d]} for d in DISTRICTS}
ceil("Alt D no reserve LP", mip=False, land=landD)
# Alt E: published yields (no forecast scaling) in the numerator, reference unchanged
from audit_load import GROUP
puby = {}
for c in P["published"]:
    f = P["yield_fc"][GROUP[c]]
    ratio = {"low": f["low"] / f["forecast"], "expected": 1.0, "high": f["high"] / f["forecast"]}
    puby[c] = {l: {d: P["published"][c][d] * ratio[l] for d in DISTRICTS} for l in ["low", "expected", "high"]}
ceil("Alt E published yields unscaled LP", mip=False, yld=puby)
for d in DISTRICTS:
    print(f"land {d}: builder W {P['land_limit'][d]['winter']:,.0f} S {P['land_limit'][d]['summer']:,.0f} | "
          f"AltA W {landA[d]['winter']:,.0f} S {landA[d]['summer']:,.0f} | AltB W {landB[d]['winter']:,.0f} S {landB[d]['summer']:,.0f} N {landB[d]['nili']:,.0f}")
