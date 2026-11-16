"""Decision maker input template reader for version 6.

This module sits at the data loading edge only. It reads one
optional CSV file and returns plain values. It does not build or
solve any part of the model.

Template path used by the model:
  data/external/decision_maker_input_template.csv

Rules:
  * If the file is absent, this module returns None and the model
    follows its default path with no change.
  * A blank your_value cell uses the public default.
  * A filled your_value cell replaces only that named input.
  * Water is supplied by source, as a total for the reference water
    state of normal storage and normal inflow. If all three source
    cells for a district are blank, the district keeps its public
    default total. If one or two source cells are filled, the filled
    sources are used and the blank sources are covered by one public
    default balance. The balance is the public default total minus
    the filled source total, and it is never below zero. The balance
    is not assigned to a source, because no public source split is
    held. Districts with no filled source cell are returned in a
    separate list, so the model can leave those districts on its
    exact default path.
  * A filled crop price replaces the expected price. The low and
    high price bands move by the same ratio, so the shape of the
    price band stays as published.
"""

from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
TEMPLATE_PATH = BASE_DIR / "data" / "external" / "decision_maker_input_template.csv"

WATER_SOURCES = ["canal", "reuse", "groundwater"]
SOURCE_LABEL = {
    "canal": "canal water",
    "reuse": "reuse water",
    "groundwater": "groundwater",
}
CROP_LABEL = {
    "Wheat": "Wheat",
    "Sugar beet": "Sugar beet",
    "Rice": "Rice",
    "Maize_summer": "Maize summer",
    "Maize_nili": "Maize Nili",
    "Potatoes_winter": "Potatoes winter",
    "Potatoes_summer": "Potatoes summer",
    "Potatoes_nili": "Potatoes Nili",
    "Berseem": "Berseem",
}
LABEL_TO_CROP = {v: k for k, v in CROP_LABEL.items()}


def _number(value):
    """Return a float for a filled cell, or None for a blank cell."""
    if value is None or pd.isna(value):
        return None
    text = str(value).strip()
    if text == "":
        return None
    return float(text)


def read_user_template(path, default_water_bcm):
    """Read the template and resolve water totals.

    default_water_bcm maps each district to its public default total
    in billion cubic metres. The return value holds water totals in
    cubic metres, crop cost values, crop expected price values, and
    provenance lines for the run log. It returns None when the file
    is absent.
    """
    path = Path(path)
    if not path.exists():
        return None
    frame = pd.read_csv(path)
    needed = {"input_type", "district", "crop", "source", "your_value"}
    missing = needed.difference(frame.columns)
    if missing:
        raise ValueError(f"Decision maker template is missing columns: {sorted(missing)}")

    raw_water = {}
    raw_cost = {}
    raw_price = {}
    for _, row in frame.iterrows():
        value = _number(row["your_value"])
        kind = str(row["input_type"]).strip()
        if kind == "water":
            district = str(row["district"]).strip()
            source = str(row["source"]).strip()
            raw_water[(district, source)] = value
        elif kind == "crop cost":
            crop = LABEL_TO_CROP[str(row["crop"]).strip()]
            raw_cost[crop] = value
        elif kind == "crop price":
            crop = LABEL_TO_CROP[str(row["crop"]).strip()]
            raw_price[crop] = value

    water_m3 = {}
    filled_districts = []
    provenance = []
    for district, default_bcm in default_water_bcm.items():
        values = {s: raw_water.get((district, s)) for s in WATER_SOURCES}
        filled = {s: v for s, v in values.items() if v is not None}
        if filled:
            filled_districts.append(district)
        if not filled:
            water_m3[district] = default_bcm * 1e9
            provenance.append(
                f"Water for {district}: public default total {default_bcm:.4f} "
                "billion cubic metres. All three source cells were blank."
            )
            continue
        filled_total = sum(filled.values())
        default_balance = max(default_bcm - filled_total, 0.0)
        total_bcm = filled_total + default_balance
        water_m3[district] = total_bcm * 1e9
        parts = []
        for source in WATER_SOURCES:
            if source in filled:
                parts.append(f"{SOURCE_LABEL[source]} {filled[source]:.4f} from the user")
            else:
                parts.append(f"{SOURCE_LABEL[source]} blank")
        provenance.append(
            f"Water for {district}: total {total_bcm:.4f} billion cubic metres. "
            + "; ".join(parts)
            + f"; public default balance {default_balance:.4f} billion cubic metres "
              "for the blank source cells, not assigned to a source."
        )

    return {
        "path": str(path),
        "water_m3": water_m3,
        "water_filled_districts": filled_districts,
        "cost": raw_cost,
        "price_expected": raw_price,
        "water_provenance": provenance,
    }
