"""Independent loading for the v4 audit. Written from the raw CSVs only.
No import of src/allocation_model_v4.py anywhere in this audit."""
import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parents[3]
EXT = BASE / "data" / "external"
PROC = BASE / "data" / "processed"

DISTRICTS = ["Beheira", "Sharkia", "Dakahlia", "Kafr El Sheikh",
             "Gharbia", "Menoufia", "Qalyubia", "Damietta"]
WINTER = ["Wheat", "Sugar beet", "Potatoes_winter"]
SUMMER_ALL = ["Rice", "Maize_summer", "Maize_nili", "Potatoes_summer", "Potatoes_nili"]
SUMMER_TRUE = ["Rice", "Maize_summer", "Potatoes_summer"]
NILI = ["Maize_nili", "Potatoes_nili"]
ALLC = WINTER + SUMMER_ALL
STAPLES = ["Wheat", "Rice", "Maize_summer"]
GROUP = {"Wheat": "wheat", "Sugar beet": "sugar_beet", "Potatoes_winter": "potatoes",
         "Rice": "rice_paddy", "Maize_summer": "maize", "Maize_nili": "maize",
         "Potatoes_summer": "potatoes", "Potatoes_nili": "potatoes"}
COST = {"Wheat": 37742.86, "Sugar beet": 39454.76, "Rice": 41850.00,
        "Maize_summer": 37671.43, "Maize_nili": 37888.10,
        "Potatoes_summer": 86657.14, "Potatoes_nili": 54176.19,
        "Potatoes_winter": 86657.14}
WREQ = {"Wheat": 5126.0, "Rice": 16600.0, "Maize_summer": 9305.0,
        "Maize_nili": 7433.0, "Sugar beet": 6100.0,
        "Potatoes_winter": 4079.0, "Potatoes_summer": 6145.0, "Potatoes_nili": 6145.0}
KY = {"Wheat": 1.05, "Rice": 1.20, "Maize_summer": 1.25, "Maize_nili": 1.25,
      "Sugar beet": 1.00, "Potatoes_winter": 1.10, "Potatoes_summer": 1.10,
      "Potatoes_nili": 1.10}
INFLOW = ["dry", "normal", "high", "drought"]
LAYERS = ["low", "expected", "high"]
LAYER_P = {"low": 0.25, "expected": 0.50, "high": 0.25}
ANCHOR = 11.00
MINV = 0.30


def amap(df, crop, season, year):
    sub = df[(df.crop == crop) & (df.season == season) & (df.agricultural_year == year)]
    out = {}
    for d in DISTRICTS:
        r = sub[sub.governorate == d]
        v = float(r.area_hectares.iloc[0]) if len(r) else 0.0
        out[d] = 0.0 if pd.isna(v) else v
    return out


def ymap(df, crop, season, year):
    sub = df[(df.crop == crop) & (df.season == season) & (df.agricultural_year == year)]
    out = {}
    for d in DISTRICTS:
        r = sub[sub.governorate == d]
        out[d] = float(r.yield_tons_per_hectare.iloc[0]) if len(r) else float("nan")
    return out


def load():
    P = {}
    area = pd.read_csv(EXT / "capmas_governorate_area.csv")
    yld = pd.read_csv(EXT / "capmas_governorate_yield.csv")
    tot = pd.read_csv(EXT / "capmas_governorate_total_cropped_area.csv")
    nili = pd.read_csv(EXT / "nili_maize_governorate_2020_2021.csv")
    pot = pd.read_csv(EXT / "potato_season_split.csv")
    fc = pd.read_csv(PROC / "forecast_prices_yields_v4.csv")
    inflow = pd.read_csv(EXT / "nile_inflow_aswan_series.csv")

    pr = tot[(tot.agricultural_year == "2020/2021") & (tot.measure == "cultivated_area")]
    P["physical"] = {d: float(pr.loc[pr.governorate == d, "area_hectares"].iloc[0]) for d in DISTRICTS}
    ar = tot[(tot.agricultural_year == "2020/2021") & (tot.measure == "total_cropped_area")]
    P["annual"] = {d: float(ar.loc[ar.governorate == d, "area_hectares"].iloc[0]) for d in DISTRICTS}

    base = {}
    base["Wheat"] = amap(area, "wheat", "winter", "2020/2021")
    base["Sugar beet"] = amap(area, "sugar_beet", "winter", "2020/2021")
    base["Rice"] = amap(area, "rice", "summer", "2020/2021")
    base["Maize_summer"] = amap(area, "maize", "summer", "2020/2021")
    nm = nili[nili.crop == "maize"]
    base["Maize_nili"] = {}
    for d in DISTRICTS:
        r = nm[nm.governorate == d]
        v = float(r.area_hectares.iloc[0]) if len(r) else 0.0
        base["Maize_nili"][d] = 0.0 if pd.isna(v) else v
    for crop, season in [("Potatoes_winter", "winter"), ("Potatoes_summer", "summer"), ("Potatoes_nili", "nili")]:
        sub = pot[pot.season == season]
        base[crop] = {}
        for d in DISTRICTS:
            r = sub[sub.governorate == d]
            v = float(r.area_hectares.iloc[0]) if len(r) else 0.0
            base[crop][d] = 0.0 if pd.isna(v) else v
    P["rice_menoufia_raw"] = base["Rice"]["Menoufia"]
    if base["Rice"]["Menoufia"] == 0.0:
        f = area[(area.crop == "rice") & (area.season == "summer")
                 & (area.agricultural_year == "2019/2020") & (area.governorate == "Menoufia")]
        base["Rice"]["Menoufia"] = float(f.area_hectares.iloc[0])
    P["baseline"] = base
    P["potato_years"] = sorted(pot.agricultural_year.unique().tolist())

    pub = {}
    pub["Wheat"] = ymap(yld, "wheat", "winter", "2020/2021")
    pub["Sugar beet"] = ymap(yld, "sugar_beet", "winter", "2020/2021")
    pub["Rice"] = ymap(yld, "rice", "summer", "2020/2021")
    pub["Maize_summer"] = ymap(yld, "maize", "summer", "2020/2021")
    pub["Maize_nili"] = {}
    for d in DISTRICTS:
        r = nm[nm.governorate == d]
        pub["Maize_nili"][d] = float(r.yield_tons_per_hectare.iloc[0]) if len(r) else float("nan")
    for crop, season in [("Potatoes_winter", "winter"), ("Potatoes_summer", "summer"), ("Potatoes_nili", "nili")]:
        sub = pot[pot.season == season]
        pub[crop] = {}
        for d in DISTRICTS:
            r = sub[sub.governorate == d]
            pub[crop][d] = float(r.yield_tons_per_hectare.iloc[0]) if len(r) else float("nan")
    fills = []
    for crop in ALLC:
        known = [d for d in DISTRICTS if not pd.isna(pub[crop][d])]
        ws = sum(base[crop][d] for d in known)
        fv = (sum(pub[crop][d] * base[crop][d] for d in known) / ws) if ws > 0 else sum(pub[crop][d] for d in known) / len(known)
        for d in DISTRICTS:
            if pd.isna(pub[crop][d]):
                pub[crop][d] = fv
                fills.append((crop, d, fv))
    P["published"] = pub
    P["fills"] = fills

    pf, yf = {}, {}
    for _, r in fc.iterrows():
        e = {"forecast": float(r.forecast_value), "low": float(r.band_low), "high": float(r.band_high),
             "rmse": float(r.backtest_rmse), "mape": float(r.backtest_mape_pct), "model": r.selected_model}
        (pf if r.target == "price" else yf)[r.crop] = e
    P["price_fc"], P["yield_fc"] = pf, yf
    P["price"] = {c: {"low": pf[GROUP[c]]["low"], "expected": pf[GROUP[c]]["forecast"], "high": pf[GROUP[c]]["high"]} for c in ALLC}
    P["yield"] = {}
    P["yield_scale"] = {}
    for c in ALLC:
        f = yf[GROUP[c]]
        ws = sum(base[c].values())
        wm = sum(pub[c][d] * base[c][d] for d in DISTRICTS) / ws if ws > 0 else sum(pub[c].values()) / 8
        sc = f["forecast"] / wm
        P["yield_scale"][c] = sc
        P["yield"][c] = {st: {d: pub[c][d] * sc * ({"low": f["low"] / f["forecast"], "expected": 1.0, "high": f["high"] / f["forecast"]}[st]) for d in DISTRICTS} for st in LAYERS}

    P["reference_t"] = sum(base[c][d] * pub[c][d] for c in STAPLES for d in DISTRICTS)
    P["reference_by_crop"] = {c: sum(base[c][d] * pub[c][d] for d in DISTRICTS) for c in STAPLES}

    # builder reserve construction, replayed
    res, lim = {}, {}
    for d in DISTRICTS:
        w = sum(base[c][d] for c in WINTER)
        s = sum(base[c][d] for c in SUMMER_ALL)
        un = P["annual"][d] - (w + s)
        rw = un * w / (w + s)
        rs = un * s / (w + s)
        res[d] = {"winter": rw, "summer": rs, "unmod": un, "w_obs": w, "s_obs": s}
        lim[d] = {"winter": P["physical"][d] - rw, "summer": P["physical"][d] - rs}
    P["reserve"], P["land_limit"] = res, lim

    flows = inflow.flow_billion_cubic_metres.astype(float)
    mf = float(flows.mean())
    lo, hi = 0.85 * mf, 1.08 * mf
    bands = {"dry": flows[flows < lo], "normal": flows[(flows >= lo) & (flows <= hi)], "high": flows[flows > hi]}
    ratios = {k: float(v.mean() / mf) for k, v in bands.items()}
    counts = {k: int(len(v)) for k, v in bands.items()}
    wr = flows.rolling(10).mean().dropna() / mf
    dr = float(wr.min())
    dprob = float((wr <= dr + 1e-12).mean())
    probs = {k: counts[k] / len(flows) * (1 - dprob) for k in bands}
    probs["drought"] = dprob
    ratios["drought"] = dr
    P["inflow"] = {"mean": mf, "ratios": ratios, "counts": counts, "probs": probs,
                   "budgets": {s: ANCHOR * ratios[s] for s in INFLOW}, "nwin": int(len(wr)),
                   "n_at_below": int((wr <= dr + 1e-12).sum())}
    tp = sum(P["physical"].values())
    P["budget"] = {(d, s): P["inflow"]["budgets"][s] * 1e9 * P["physical"][d] / tp for d in DISTRICTS for s in INFLOW}
    P["scenarios"] = [(i, l) for i in INFLOW for l in LAYERS]
    P["prob"] = {(i, l): probs[i] * LAYER_P[l] for (i, l) in P["scenarios"]}
    P["cost"], P["wreq"], P["ky"] = dict(COST), dict(WREQ), dict(KY)
    P["flows"] = flows
    return P


if __name__ == "__main__":
    P = load()
    print("physical total", sum(P["physical"].values()))
    print("annual total", sum(P["annual"].values()))
    print("potato years in split file", P["potato_years"])
    print("Menoufia rice raw 2020/2021 area", P["rice_menoufia_raw"], "filled area", P["baseline"]["Rice"]["Menoufia"])
    print("reference", P["reference_t"], P["reference_by_crop"])
    print("fills", P["fills"])
    print("yield scales", {k: round(v, 4) for k, v in P["yield_scale"].items()})
    print("inflow", P["inflow"])
    print("true mean budget", sum(P["inflow"]["probs"][s] * P["inflow"]["budgets"][s] for s in INFLOW))
    for d in DISTRICTS:
        r = P["reserve"][d]
        print(f"{d}: phys {P['physical'][d]:,.1f} w_obs {r['w_obs']:,.1f} w_lim {P['land_limit'][d]['winter']:,.1f} "
              f"w_slack {P['land_limit'][d]['winter']-r['w_obs']:,.1f} | s_obs(pooled) {r['s_obs']:,.1f} s_lim {P['land_limit'][d]['summer']:,.1f} "
              f"s_slack {P['land_limit'][d]['summer']-r['s_obs']:,.1f} | unmod {r['unmod']:,.1f}")
    print("observed totals by crop", {c: round(sum(P["baseline"][c].values()), 1) for c in ALLC})
    print("mean prices", {c: round(sum(LAYER_P[l] * P["price"][c][l] for l in LAYERS), 2) for c in ALLC})
