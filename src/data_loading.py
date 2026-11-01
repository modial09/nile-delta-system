"""Data loading for the Nile Delta system.

Every loader reads one raw file from data/raw and returns a tidy
pandas DataFrame. No cleaning logic lives outside this module and
the notebooks that call it, so every number in the paper can be
traced to a file and a transformation.
"""

from pathlib import Path

import pandas as pd

RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"


def load_faostat_crops(path: Path) -> pd.DataFrame:
    """Load FAOSTAT crops and livestock production data for Egypt.

    Returns columns for crop, year, area harvested, yield, and
    production, with units stated in the design document.
    """
    raise NotImplementedError("Week 1 task: implement after the FAOSTAT pull")


def load_faostat_prices(path: Path) -> pd.DataFrame:
    """Load FAOSTAT producer prices for Egypt by crop and year."""
    raise NotImplementedError("Week 1 task: implement after the FAOSTAT pull")


def load_district_land(path: Path) -> pd.DataFrame:
    """Load cropped area by governorate and crop from CAPMAS releases."""
    raise NotImplementedError("Week 1 task: implement after the CAPMAS pull")
