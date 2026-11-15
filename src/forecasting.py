"""Forecasting module: next season prices and yields.

Version 4 implementation, built to docs/FOUNDATIONS.md Section 6 and
docs/REASSESSMENT_AND_UPGRADE_DESIGN.md Part 2.1.

The module forecasts producer prices and national yields per crop from
historical series, scores itself with rolling origin backtests, and
hands forecast means and error spreads to the allocation model as
scenario parameters.

Feature discipline (fixed by the original scaffold): lagged target
values, a time trend, lagged fertilizer price, and lagged planted
area. No feature may use information from the season being forecast.

Fertilizer price note: the design names the World Bank Pink Sheet as
the fertilizer price source. The Pink Sheet file held in this project
(data/external/pink_sheet_crosscheck.csv) contains no fertilizer
series at all. It holds only international reference prices for wheat,
maize and milled rice for 2022 to 2025. A lagged fertilizer feature
therefore cannot be built for a backtest that starts in 2011, and this
run omits the feature as a named gap. The code path is present: if a
fertilizer series is supplied to build_features, the lagged column is
built and used. No substitute series is invented.

Hole handling (prices): rice paddy and sugar beet producer prices are
missing for 2019, 2020 and 2021 in the FAOSTAT prices domain. The
series are carried in observed year order. A lag means the previous
observed year. Missing years are never training targets and are never
scored. For rice paddy and sugar beet the step into 2022 spans the
hole in calendar time, and the report says so.

Outlier handling (yields): the direct FAOSTAT crops pull flags two
published values that stand out, maize yield in 2019 and sugar beet
yield in 2020. They are kept exactly as published. Origins whose
target year is one of those years are scored as published and count
in every headline score. A sensitivity line in the run log and the
report shows the selected model score with that single origin removed,
labelled as a sensitivity only.

Run with the project venv python:
    .venv/bin/python src/forecasting.py
Outputs:
    data/processed/forecast_prices_yields_v4.csv
    data/processed/backtest_scores_v4.csv
    data/processed/run_forecasting_v4.txt
"""

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]
EXT = ROOT / "data" / "external"
PROC = ROOT / "data" / "processed"

CROPS = ["wheat", "rice_paddy", "maize", "sugar_beet", "potatoes"]
ML_MODELS = ["ridge", "random_forest", "gradient_boosting"]
ALL_MODELS = ML_MODELS + ["naive_last", "drift"]
RANDOM_STATE = 42
MIN_TRAIN_ROWS = 8

PRICE_FIRST_TRAIN_END = 2010
YIELD_FIRST_TRAIN_END = 2000
BAND_Q_LOW = 0.10
BAND_Q_HIGH = 0.90

# Published yield outliers flagged by the crops pull provenance file.
YIELD_OUTLIER_YEARS = {"maize": 2019, "sugar_beet": 2020}


# ---------------------------------------------------------------- data

def load_price_series():
    """Return {crop: DataFrame[year, value]} for EGP per tonne prices."""
    df = pd.read_csv(EXT / "faostat_producer_prices_egypt.csv")
    df = df[df["unit"] == "EGP per tonne"].copy()
    out = {}
    for crop in CROPS:
        sub = df[df["crop"] == crop][["year", "price"]].rename(
            columns={"price": "value"}
        )
        out[crop] = sub.sort_values("year").reset_index(drop=True)
    return out


def load_yield_and_area_series():
    """Return ({crop: yield df}, {crop: {year: area harvested}})."""
    df = pd.read_csv(EXT / "faostat_crops_egypt.csv")
    yields, areas = {}, {}
    for crop in CROPS:
        y = df[(df["crop"] == crop) & (df["element"] == "Yield")][
            ["year", "value"]
        ]
        yields[crop] = y.sort_values("year").reset_index(drop=True)
        a = df[(df["crop"] == crop) & (df["element"] == "Area harvested")]
        areas[crop] = dict(zip(a["year"].astype(int), a["value"].astype(float)))
    return yields, areas


def load_area_for_prices():
    """Planted area (area harvested) by crop and calendar year."""
    _, areas = load_yield_and_area_series()
    return areas


def load_fertilizer_series():
    """Look for a fertilizer price series in the Pink Sheet file.

    Returns None when the file holds no fertilizer series, which is
    the case for the file in this project. See the module docstring.
    """
    path = EXT / "pink_sheet_crosscheck.csv"
    if not path.exists():
        return None
    df = pd.read_csv(path)
    text_cols = [c for c in df.columns if df[c].dtype == object]
    mask = pd.Series(False, index=df.index)
    for col in text_cols:
        mask = mask | df[col].astype(str).str.contains(
            "fertil", case=False, na=False
        )
    fert = df[mask]
    if fert.empty:
        return None
    return fert


# ------------------------------------------------------------ features

def build_features(series: pd.DataFrame) -> pd.DataFrame:
    """Build lag and trend features for one crop series.

    Input columns: year, value, and optionally area_lag_source as a
    dict {calendar year: area} attached by the caller in a column
    named area_prev (the planted area of the calendar year before the
    target year), and fert_prev (the fertilizer price of the calendar
    year before the target year) when a fertilizer series exists.

    Output columns: year, y, lag1, lag2, lag3, trend, area_lag1 and,
    when supplied, fert_lag1. Lags are taken in observed year order,
    so a lag is the previous observed value of the target. Rows are
    only built where three observed lags exist. No column uses the
    target season itself: trend is the target calendar year, which is
    known before the season, and area and fertilizer enter lagged by
    one calendar year.
    """
    s = series.sort_values("year").reset_index(drop=True)
    rows = []
    values = s["value"].to_numpy(dtype=float)
    years = s["year"].to_numpy(dtype=int)
    for i in range(3, len(s)):
        row = {
            "year": int(years[i]),
            "y": float(values[i]),
            "lag1": float(values[i - 1]),
            "lag2": float(values[i - 2]),
            "lag3": float(values[i - 3]),
            "trend": float(years[i]),
        }
        if "area_prev" in s.columns:
            row["area_lag1"] = s["area_prev"].iloc[i]
        if "fert_prev" in s.columns and pd.notna(s["fert_prev"].iloc[i]):
            row["fert_lag1"] = s["fert_prev"].iloc[i]
        rows.append(row)
    return pd.DataFrame(rows)


def attach_lagged_externals(series, area_by_year=None, fert_by_year=None):
    """Attach previous calendar year area and fertilizer values."""
    s = series.copy()
    if area_by_year is not None:
        s["area_prev"] = s["year"].map(
            lambda yr: area_by_year.get(int(yr) - 1, np.nan)
        )
    if fert_by_year is not None:
        s["fert_prev"] = s["year"].map(
            lambda yr: fert_by_year.get(int(yr) - 1, np.nan)
        )
    return s


def next_season_features(series, area_by_year=None, fert_by_year=None):
    """Feature row for the season after the last observed year."""
    s = series.sort_values("year").reset_index(drop=True)
    values = s["value"].to_numpy(dtype=float)
    last_year = int(s["year"].iloc[-1])
    row = {
        "year": last_year + 1,
        "lag1": float(values[-1]),
        "lag2": float(values[-2]),
        "lag3": float(values[-3]),
        "trend": float(last_year + 1),
    }
    if area_by_year is not None:
        row["area_lag1"] = area_by_year.get(last_year, np.nan)
    if fert_by_year is not None:
        row["fert_lag1"] = fert_by_year.get(last_year, np.nan)
    return pd.DataFrame([row]), last_year


# -------------------------------------------------------------- models

def make_models():
    """Fresh model instances keyed by model name (ML models only)."""
    return {
        "ridge": make_pipeline(StandardScaler(), Ridge(alpha=1.0)),
        "random_forest": RandomForestRegressor(
            n_estimators=300,
            min_samples_leaf=2,
            random_state=RANDOM_STATE,
            n_jobs=1,
        ),
        "gradient_boosting": GradientBoostingRegressor(
            n_estimators=100,
            max_depth=2,
            learning_rate=0.08,
            random_state=RANDOM_STATE,
        ),
    }


def feature_columns(feat: pd.DataFrame):
    cols = ["lag1", "lag2", "lag3", "trend"]
    if "area_lag1" in feat.columns and feat["area_lag1"].notna().all():
        cols.append("area_lag1")
    if "fert_lag1" in feat.columns and feat["fert_lag1"].notna().all():
        cols.append("fert_lag1")
    return cols


def train_models(features: pd.DataFrame, target: str = "y") -> dict:
    """Train the ridge baseline, a random forest, and gradient boosting.

    The machine learning models are fitted to the natural log of the
    target and their predictions are returned to the original scale
    before scoring (see predict_model). Prices in this project grow
    multiplicatively, and a levels fit extrapolates that growth
    explosively on refit; the log specification is the standard repair
    and it also keeps every forecast positive. The naive and drift
    lines are computed on the original scale. All scores are computed
    on the original scale, so the comparison across models is on one
    basis.

    Returns a dictionary of fitted models keyed by model name. Models
    that fail are returned with value None and the failure is recorded
    in the returned dict under the key formed by the model name plus
    the suffix _error, so callers report the failure instead of
    dropping the model silently.
    """
    cols = feature_columns(features)
    out = {}
    for name, model in make_models().items():
        try:
            model.fit(features[cols], np.log(features[target]))
            out[name] = model
        except Exception as exc:  # reported by caller, never hidden
            out[name] = None
            out[name + "_error"] = f"{type(exc).__name__}: {exc}"
    out["_feature_columns"] = cols
    return out


def predict_model(model, X):
    """Predict with a log fitted model, on the original scale."""
    return np.exp(model.predict(X))


def drift_step(train_values):
    """Mean change per observed step over the training values."""
    diffs = np.diff(np.asarray(train_values, dtype=float))
    return float(np.mean(diffs)) if len(diffs) else 0.0


# ------------------------------------------------------------ backtest

def rolling_backtest(series, first_train_end, horizon=1):
    """Rolling origin backtest with an expanding training window.

    series is a feature ready frame with year and value columns plus
    any lagged external columns attached. horizon 1 is the primary
    one step ahead evaluation. horizon 2 trains pairs whose target
    sits two observed steps after the feature row.

    Returns (predictions, failures): predictions is a long DataFrame
    with year, actual, model, forecast; failures is a list of dicts
    with crop level context added by the caller.
    """
    feat = build_features(series)
    cols = feature_columns(feat)
    s = series.sort_values("year").reset_index(drop=True)
    test_years = sorted(
        int(y) for y in feat["year"].unique() if int(y) > first_train_end
    )
    records, failures = [], []
    values_by_year = dict(zip(s["year"].astype(int), s["value"].astype(float)))
    observed_years = list(s["year"].astype(int))
    for test_year in test_years:
        j = observed_years.index(test_year)
        origin_pos = j - horizon
        if origin_pos < 3:
            continue
        # Training pairs whose target position is at or before the
        # origin position, with the target shifted by the horizon.
        # A pair whose target falls after the origin would leak, so
        # the last usable feature position is origin minus horizon
        # plus one.
        train_rows = []
        for i in range(3, origin_pos - horizon + 2):
            target_pos = i + horizon - 1
            if target_pos >= len(s):
                continue
            row = feat.iloc[i - 3].copy()  # feat row for position i
            row["y"] = float(s["value"].iloc[target_pos])
            train_rows.append(row)
        train = pd.DataFrame(train_rows)
        # Predictor row: features whose first lag is the last value
        # known at the origin, so the row for position origin plus one.
        origin_feat_row = feat.iloc[origin_pos + 1 - 3]
        actual = float(values_by_year[test_year])
        train_target_values = s["value"].iloc[: origin_pos + 1].to_numpy(
            dtype=float
        )
        if len(train) < MIN_TRAIN_ROWS:
            for name in ALL_MODELS:
                failures.append(
                    {
                        "year": test_year,
                        "model": name,
                        "reason": (
                            f"only {len(train)} training rows, below the "
                            f"minimum of {MIN_TRAIN_ROWS}"
                        ),
                    }
                )
            continue
        fitted = train_models(train, "y")
        for name in ML_MODELS:
            model = fitted.get(name)
            if model is None:
                failures.append(
                    {
                        "year": test_year,
                        "model": name,
                        "reason": fitted.get(name + "_error", "fit failed"),
                    }
                )
                continue
            try:
                pred = float(
                    predict_model(
                        model,
                        origin_feat_row[cols].to_frame().T.astype(float),
                    )[0]
                )
                records.append(
                    {"year": test_year, "actual": actual,
                     "model": name, "forecast": pred}
                )
            except Exception as exc:
                failures.append(
                    {"year": test_year, "model": name,
                     "reason": f"{type(exc).__name__}: {exc}"}
                )
        last_value = float(train_target_values[-1])
        records.append(
            {"year": test_year, "actual": actual, "model": "naive_last",
             "forecast": last_value}
        )
        records.append(
            {"year": test_year, "actual": actual, "model": "drift",
             "forecast": last_value + horizon * drift_step(train_target_values)}
        )
    return pd.DataFrame(records), failures


def score_predictions(preds: pd.DataFrame) -> pd.DataFrame:
    """RMSE, MAE, MAPE and skill against naive last value, per model."""
    rows = []
    naive_rmse = None
    per_model = {}
    for name, g in preds.groupby("model"):
        err = g["forecast"].to_numpy() - g["actual"].to_numpy()
        rmse = float(np.sqrt(np.mean(err ** 2)))
        per_model[name] = rmse
    naive_rmse = per_model.get("naive_last")
    for name in ALL_MODELS:
        g = preds[preds["model"] == name]
        if g.empty:
            rows.append(
                {"model": name, "n_test": 0, "rmse": np.nan, "mae": np.nan,
                 "mape_pct": np.nan, "skill_vs_naive": np.nan,
                 "status": "failed"}
            )
            continue
        err = g["forecast"].to_numpy() - g["actual"].to_numpy()
        act = g["actual"].to_numpy()
        rmse = float(np.sqrt(np.mean(err ** 2)))
        rows.append(
            {
                "model": name,
                "n_test": int(len(g)),
                "rmse": rmse,
                "mae": float(np.mean(np.abs(err))),
                "mape_pct": float(np.mean(np.abs(err / act)) * 100.0),
                "skill_vs_naive": (
                    rmse / naive_rmse if naive_rmse else np.nan
                ),
                "status": "ok",
            }
        )
    return pd.DataFrame(rows)


# ------------------------------------------------------------ forecast

def forecast_next(series, selected_model, area_by_year=None,
                  fert_by_year=None):
    """Retrain the selected model on all data and forecast one step.

    Naive and drift lines are computed directly from the observed
    series. ML models are refitted on every feature row.
    """
    s = series.sort_values("year").reset_index(drop=True)
    values = s["value"].to_numpy(dtype=float)
    if selected_model == "naive_last":
        return float(values[-1])
    if selected_model == "drift":
        return float(values[-1] + drift_step(values))
    feat = build_features(series)
    cols = feature_columns(feat)
    fitted = train_models(feat, "y")
    model = fitted.get(selected_model)
    if model is None:
        raise RuntimeError(
            f"selected model {selected_model} failed on the full data: "
            f"{fitted.get(selected_model + '_error')}"
        )
    nxt, _ = next_season_features(series, area_by_year, fert_by_year)
    return float(predict_model(model, nxt[cols].astype(float))[0])


def scenario_parameters(backtest: pd.DataFrame, forecasts: pd.DataFrame) -> dict:
    """Convert forecasts and backtest errors into scenario inputs.

    backtest is the one step predictions frame for the selected model
    of one crop and target. forecasts is a one row frame with the
    forecast value. Returns the expected value plus the low and high
    band states, where the band is the forecast shifted by the
    empirical 10th and 90th percentiles of the one step backtest
    residuals of the selected model.
    """
    residuals = (
        backtest["actual"].to_numpy() - backtest["forecast"].to_numpy()
    )
    fc = float(forecasts["forecast_value"].iloc[0])
    return {
        "expected": fc,
        "low": fc + float(np.quantile(residuals, BAND_Q_LOW)),
        "high": fc + float(np.quantile(residuals, BAND_Q_HIGH)),
        "residual_q10": float(np.quantile(residuals, BAND_Q_LOW)),
        "residual_q90": float(np.quantile(residuals, BAND_Q_HIGH)),
    }


# ----------------------------------------------------------------- run

def run_one(series, crop, target, first_train_end, area_by_year,
            fert_by_year, log):
    """Backtest, select, forecast. Returns dicts for scores and forecast."""
    series = attach_lagged_externals(series, area_by_year, fert_by_year)
    preds, failures = rolling_backtest(series, first_train_end, horizon=1)
    scores = score_predictions(preds)
    scores.insert(0, "target", target)
    scores.insert(0, "crop", crop)
    fail_models = set()
    if failures:
        fr = pd.DataFrame(failures)
        for name, g in fr.groupby("model"):
            ok_years = set(preds[preds["model"] == name]["year"]) if not preds.empty else set()
            if len(ok_years) == 0:
                fail_models.add(name)
        for _, r in fr.iterrows():
            log.append(
                f"  failure note: {crop} {target} year {r['year']} model "
                f"{r['model']}: {r['reason']}"
            )
    for name in fail_models:
        scores.loc[scores["model"] == name, "status"] = "failed"
    ok = scores[scores["status"] == "ok"].copy()
    selected = ok.sort_values("rmse").iloc[0]
    sel_name = selected["model"]
    sel_preds = preds[preds["model"] == sel_name]
    fc_value = forecast_next(series, sel_name, area_by_year, fert_by_year)
    last_year = int(series["year"].max())
    fc_frame = pd.DataFrame([{"forecast_value": fc_value}])
    params = scenario_parameters(sel_preds, fc_frame)
    residuals = sel_preds["actual"].to_numpy() - sel_preds["forecast"].to_numpy()
    result = {
        "crop": crop,
        "target": target,
        "last_observed_year": last_year,
        "forecast_season": last_year + 1,
        "selected_model": sel_name,
        "forecast_value": fc_value,
        "band_low": params["low"],
        "band_high": params["high"],
        "backtest_rmse": float(selected["rmse"]),
        "backtest_mae": float(selected["mae"]),
        "backtest_mape_pct": float(selected["mape_pct"]),
        "skill_vs_naive": float(selected["skill_vs_naive"]),
        "n_test": int(selected["n_test"]),
        "residual_q10": params["residual_q10"],
        "residual_q90": params["residual_q90"],
    }
    # Secondary two step ahead scores, for the report only.
    preds2, _ = rolling_backtest(series, first_train_end, horizon=2)
    scores2 = score_predictions(preds2) if not preds2.empty else pd.DataFrame()
    if not scores2.empty:
        scores2.insert(0, "target", target + " two step")
        scores2.insert(0, "crop", crop)
    # Outlier sensitivity for the selected model, yields only.
    sensitivity = None
    if target == "yield" and crop in YIELD_OUTLIER_YEARS:
        oy = YIELD_OUTLIER_YEARS[crop]
        keep = sel_preds[sel_preds["year"] != oy]
        if len(keep) < len(sel_preds) and len(keep) > 0:
            err = keep["forecast"].to_numpy() - keep["actual"].to_numpy()
            sensitivity = {
                "outlier_year": oy,
                "rmse_without_outlier_origin": float(
                    np.sqrt(np.mean(err ** 2))
                ),
                "n_without": int(len(keep)),
            }
            hit = sel_preds[sel_preds["year"] == oy]
            if not hit.empty:
                sensitivity["outlier_actual"] = float(hit["actual"].iloc[0])
                sensitivity["outlier_forecast"] = float(
                    hit["forecast"].iloc[0]
                )
    return scores, scores2, result, sensitivity, preds


def main():
    log = []
    log.append("Nile Delta forecasting module version 4 run log")
    log.append("Selection metric: lowest one step backtest RMSE per crop")
    log.append("Band: forecast plus empirical 10th and 90th percentiles of")
    log.append("the selected model one step backtest residuals")
    fert = load_fertilizer_series()
    if fert is None:
        log.append("Fertilizer feature: NOT BUILT. The Pink Sheet file in this")
        log.append("project holds no fertilizer series, only international")
        log.append("wheat, maize and milled rice reference prices for 2022 to")
        log.append("2025. Models run on lagged target values, time trend and")
        log.append("lagged planted area. This is a named gap, not a silent drop.")
        fert_by_year = None
    else:
        fert_by_year = dict(
            zip(fert["year"].astype(int), fert.iloc[:, 2].astype(float))
        )
        log.append("Fertilizer feature: built from the Pink Sheet file.")

    prices = load_price_series()
    yields, areas = load_yield_and_area_series()

    all_scores, all_forecasts, sensitivities = [], [], []
    for target, series_map, train_end in [
        ("price", prices, PRICE_FIRST_TRAIN_END),
        ("yield", yields, YIELD_FIRST_TRAIN_END),
    ]:
        for crop in CROPS:
            series = series_map[crop]
            scores, scores2, result, sens, _ = run_one(
                series, crop, target, train_end, areas[crop],
                fert_by_year, log,
            )
            all_scores.append(scores)
            if scores2 is not None and not scores2.empty:
                all_scores.append(scores2)
            all_forecasts.append(result)
            if sens is not None:
                sens.update({"crop": crop, "target": target})
                sensitivities.append(sens)
            unit = "EGP per tonne" if target == "price" else "tonnes per hectare"
            log.append("")
            log.append(f"{crop} {target} ({unit})")
            log.append(
                f"  last observed year {result['last_observed_year']}, "
                f"forecast season {result['forecast_season']}"
            )
            log.append(
                f"  selected model {result['selected_model']} on "
                f"{result['n_test']} test seasons, RMSE "
                f"{result['backtest_rmse']:.4f}, MAE "
                f"{result['backtest_mae']:.4f}, MAPE "
                f"{result['backtest_mape_pct']:.2f} percent, skill against "
                f"naive {result['skill_vs_naive']:.3f}"
            )
            log.append(
                f"  forecast {result['forecast_value']:.4f} with band "
                f"{result['band_low']:.4f} to {result['band_high']:.4f}, "
                f"printed beside its backtest RMSE "
                f"{result['backtest_rmse']:.4f} and MAPE "
                f"{result['backtest_mape_pct']:.2f} percent"
            )
    log.append("")
    log.append("Outlier sensitivity, selected model, headline scores keep the")
    log.append("published values and score those origins in full:")
    for s in sensitivities:
        log.append(
            f"  {s['crop']} yield: origin {s['outlier_year']} actual "
            f"{s['outlier_actual']:.4f}, selected model forecast "
            f"{s['outlier_forecast']:.4f}; RMSE without that single origin "
            f"{s['rmse_without_outlier_origin']:.4f} on {s['n_without']} "
            f"origins, sensitivity only"
        )

    scores_df = pd.concat(all_scores, ignore_index=True)
    fc_df = pd.DataFrame(all_forecasts)
    PROC.mkdir(parents=True, exist_ok=True)
    out_cols = [
        "crop", "target", "last_observed_year", "forecast_season",
        "selected_model", "forecast_value", "band_low", "band_high",
        "backtest_rmse", "backtest_mape_pct",
    ]
    fc_out = fc_df[out_cols]
    fc_out.to_csv(PROC / "forecast_prices_yields_v4.csv", index=False)
    scores_df.to_csv(PROC / "backtest_scores_v4.csv", index=False)
    text = "\n".join(log) + "\n"
    (PROC / "run_forecasting_v4.txt").write_text(text)
    print(text)
    return fc_df, scores_df


if __name__ == "__main__":
    main()
