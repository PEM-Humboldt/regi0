import os

import pandas as pd
import pytest
from recovery.geographic import read_records

DATA_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), "data")


@pytest.fixture(scope="session")
def records():
    return read_records(
        os.path.join(DATA_FOLDER, "csv", "birds.csv"),
        "lon",
        "lat",
        drop_empty_coords=True,
        crs="epsg:4326"
    )


@pytest.fixture(scope="session")
def expected(records):
    df = pd.read_csv(os.path.join(DATA_FOLDER, "csv", "expected.csv"))
    return df.loc[records.index]
