"""Problem One: allocation of land and water under uncertainty.

A two stage stochastic linear program. Stage one plants hectares
by crop and district before the inflow is known. Stage two
allocates water under the scenario that occurs. The objective is
expected farm margin with a shortfall penalty that reflects yield
loss. Dual values on the district water constraints are a primary
output: they state the money value of one more cubic metre of
water in each district.

Design reference: docs/design.md, Problem One section.
"""

import pandas as pd


def build_deterministic_model(data: dict) -> object:
    """Build the single scenario linear program.

    The deterministic core ships first, in weeks 3 to 4, and is
    validated against the actual cropping pattern before the
    stochastic version is attempted.
    """
    raise NotImplementedError("Weeks 3 to 4 task: formulation and baseline run")


def build_stochastic_model(data: dict, scenarios: dict) -> object:
    """Build the extensive form across low, expected, and high inflow.

    Scenario prices and yields come from the forecasting module.
    Scenario probabilities are declared judgment and are stress
    tested in the sensitivity runs.
    """
    raise NotImplementedError("Week 6 task: extensive form and stress tests")


def extract_shadow_prices(solved_model: object) -> pd.DataFrame:
    """Return the water value map: dual value per district constraint."""
    raise NotImplementedError("Weeks 3 to 4 task: dual extraction after first solve")


def information_values(solved_model: object) -> dict:
    """Return the expected value of perfect information and the
    value of the stochastic solution, both stated in money."""
    raise NotImplementedError("Week 6 task: compute after stochastic solve")
