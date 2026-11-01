"""Forecasting module: next season prices and yields.

The module forecasts producer prices and yields per crop from
historical series, scores itself with rolling origin backtests,
and hands forecast means and error spreads to the allocation
model as scenario parameters. A ridge regression baseline is
always trained first, so the flexible models must earn their
place on evidence.

Design reference: docs/design.md, section on the forecasting
module. No feature may use information from the season being
forecast.
"""

import pandas as pd


def build_features(series: pd.DataFrame) -> pd.DataFrame:
    """Build lag and trend features for one crop series.

    Features: lagged target values, a time trend, lagged fertilizer
    price, and lagged planted area.
    """
    raise NotImplementedError("Week 5 task: implement with the backtest harness")


def train_models(features: pd.DataFrame, target: str) -> dict:
    """Train the ridge baseline, a random forest, and gradient boosting.

    Returns a dictionary of fitted models keyed by model name.
    """
    raise NotImplementedError("Week 5 task: implement with the backtest harness")


def rolling_backtest(series: pd.DataFrame, target: str) -> pd.DataFrame:
    """Run rolling origin backtests and return per year errors.

    Each fold trains on earlier years only and forecasts the next
    season. Returns mean absolute error and mean absolute
    percentage error per model.
    """
    raise NotImplementedError("Week 5 task: implement with the backtest harness")


def scenario_parameters(backtest: pd.DataFrame, forecasts: pd.DataFrame) -> dict:
    """Convert forecasts and backtest errors into scenario inputs.

    Returns expected prices and yields plus the spread that widens
    or narrows the scenario band consumed by Problem One.
    """
    raise NotImplementedError("Week 5 task: implement after backtests run")
