"""Auditor's own formulation. Water carried in cubic metres (the builder
carries thousands) so scaling differs by construction. PuLP with CBC.
MIP mode uses binary keep variables exactly as the foundation words
abandonment; LP mode drops the binary linkage (partial keep allowed)."""
import pulp
from audit_load import (DISTRICTS, WINTER, SUMMER_ALL, SUMMER_TRUE, NILI, ALLC,
                        STAPLES, INFLOW, LAYERS, LAYER_P, MINV)

CAPS = {"Wheat": 0.50, "Sugar beet": 0.30, "Potatoes_winter": 0.15,
        "Rice": 0.35, "Maize_summer": 0.40, "Maize_nili": 0.40,
        "Potatoes_summer": 0.15, "Potatoes_nili": 0.15}


def make(P, floor=0.0, caps=False, mip=True, budget_scale=1.0, budget_mult=None,
         land=None, land3=False, objective="margin", fixed=None, scen=None,
         price=None, yld=None, drop_inflow=None, layers_only=None,
         wreq_mult=None, no_min_share=False):
    """land: custom {d:{'winter':..,'summer':..}} ; land3: separate nili pool,
    land dict then needs 'nili'. budget_mult: {inflow: factor} overrides scale.
    drop_inflow: set of inflow states exempt from the min/floor (relaxation).
    layers_only: restrict scenario layers for floor/min purposes."""
    land = land or P["land_limit"]
    price = price or P["price"]
    yld = yld or P["yield"]
    wreq = {c: P["wreq"][c] * (wreq_mult or {}).get(c, 1.0) for c in ALLC}
    scens = [scen] if scen else P["scenarios"]
    prob = pulp.LpProblem("audit", pulp.LpMaximize)
    cat = "Binary" if mip else "Continuous"
    xw, xs = {}, {}
    inflows_used = [scen[0]] if scen else INFLOW
    for d in DISTRICTS:
        for c in WINTER:
            xw[(d, c)] = fixed["winter"][(d, c)] if fixed else pulp.LpVariable(f"xw|{d}|{c}", lowBound=0)
        for c in SUMMER_ALL:
            for i in inflows_used:
                xs[(d, c, i)] = fixed["summer"][(d, c, i)] if fixed else pulp.LpVariable(f"xs|{d}|{c}|{i}", lowBound=0)
    if not fixed:
        for d in DISTRICTS:
            prob += pulp.lpSum(xw[(d, c)] for c in WINTER) <= land[d]["winter"]
            for i in inflows_used:
                if land3:
                    prob += pulp.lpSum(xs[(d, c, i)] for c in SUMMER_TRUE) <= land[d]["summer"]
                    prob += pulp.lpSum(xs[(d, c, i)] for c in NILI) <= land[d]["nili"]
                else:
                    prob += pulp.lpSum(xs[(d, c, i)] for c in SUMMER_ALL) <= land[d]["summer"]
            if caps:
                for c in WINTER:
                    prob += xw[(d, c)] <= CAPS[c] * P["physical"][d]
                for c in SUMMER_ALL:
                    for i in inflows_used:
                        prob += xs[(d, c, i)] <= CAPS[c] * P["physical"][d]
    kept, wat, prod = {}, {}, {}
    staple, terms = {}, []
    tot_p = sum(P["prob"][s] for s in scens)
    for (i, l) in scens:
        ps = P["prob"][(i, l)] / tot_p
        fac = (budget_mult or {}).get(i, budget_scale)
        for d in DISTRICTS:
            ws = []
            for c in ALLC:
                x = xw[(d, c)] if c in WINTER else xs[(d, c, i)]
                a = pulp.LpVariable(f"a|{d}|{c}|{i}|{l}", lowBound=0)
                w = pulp.LpVariable(f"w|{d}|{c}|{i}|{l}", lowBound=0)
                kept[(d, c, (i, l))], wat[(d, c, (i, l))] = a, w
                prob += a <= x
                if mip:
                    k = pulp.LpVariable(f"k|{d}|{c}|{i}|{l}", cat="Binary")
                    # Tight per cell big M: for a fixed plan the planted
                    # area itself; otherwise the district physical area.
                    big = max(float(x), 1.0) if fixed else P["physical"][d]
                    prob += a <= big * k
                    prob += a >= x - big * (1 - k)
                prob += w <= wreq[c] * a
                if not no_min_share:
                    prob += w >= MINV * wreq[c] * a
                y = yld[c][l][d]
                q = y * (1 - P["ky"][c]) * a + y * P["ky"][c] / wreq[c] * w
                prod[(d, c, (i, l))] = q
                terms.append(ps * price[c][l] * q)
                ws.append(w)
            prob += pulp.lpSum(ws) <= P["budget"][(d, i)] * fac
        staple[(i, l)] = pulp.lpSum(prod[(d, c, (i, l))] for d in DISTRICTS for c in STAPLES)
    pcost = pulp.lpSum(P["cost"][c] * xw[(d, c)] for d in DISTRICTS for c in WINTER)
    if scen:
        pcost += pulp.lpSum(P["cost"][c] * xs[(d, c, scen[0])] for d in DISTRICTS for c in SUMMER_ALL)
    else:
        pcost += pulp.lpSum(P["inflow"]["probs"][i] * P["cost"][c] * xs[(d, c, i)]
                            for d in DISTRICTS for c in SUMMER_ALL for i in INFLOW)
    margin = pulp.lpSum(terms) - pcost
    if objective == "margin":
        if floor > 0:
            for s in scens:
                if drop_inflow and s[0] in drop_inflow:
                    continue
                if layers_only and s[1] not in layers_only:
                    continue
                prob += staple[s] >= floor * P["reference_t"]
        prob += margin
    elif objective == "maxmin":
        t = pulp.LpVariable("t", lowBound=0)
        for s in scens:
            if drop_inflow and s[0] in drop_inflow:
                continue
            if layers_only and s[1] not in layers_only:
                continue
            prob += staple[s] >= t
        prob += t
        return prob, {"xw": xw, "xs": xs, "kept": kept, "wat": wat, "prod": prod, "t": t, "staple": staple}
    elif objective == "maxexp":
        prob += pulp.lpSum((P["prob"][s] / tot_p) * staple[s] for s in scens)
    return prob, {"xw": xw, "xs": xs, "kept": kept, "wat": wat, "prod": prod, "staple": staple}


def solve(prob, gap=0.001, tl=900):
    prob.solve(pulp.PULP_CBC_CMD(msg=False, timeLimit=tl, gapRel=gap))
    return pulp.LpStatus[prob.status]


def val(v):
    return float(pulp.value(v))
