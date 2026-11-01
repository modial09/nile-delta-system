"""Problem Two: fertilizer distribution on the real road network.

Demand by district comes from Problem One: planted hectares times
published application rates. Distances come from SCGraph on its
world highways geograph. The working solution uses a nearest
neighbour construction with local improvement; an exact solve on
the smallest instance measures the heuristic gap.

This layer ships only if the core allocation work is finished and
written. Design reference: docs/design.md, Problem Two section.
"""

import pandas as pd


def district_demand(allocation: pd.DataFrame, rates: pd.DataFrame) -> pd.DataFrame:
    """Convert planted hectares by crop and district into tons of
    fertilizer demand by district and nutrient."""
    raise NotImplementedError("Weeks 7 to 8 task: implement after Problem One solves")


def distance_matrix(depots: list, points: list) -> pd.DataFrame:
    """Compute pairwise road distances with SCGraph.

    Sample distances must be validated against known road
    distances before any route result is reported.
    """
    raise NotImplementedError("Weeks 7 to 8 task: SCGraph geograph integration")


def plan_routes(demand: pd.DataFrame, distances: pd.DataFrame, capacity: float) -> dict:
    """Plan capacitated delivery routes and report cost per ton,
    total kilometres, and the gap against the nearest depot rule."""
    raise NotImplementedError("Weeks 7 to 8 task: heuristic then exact check")
