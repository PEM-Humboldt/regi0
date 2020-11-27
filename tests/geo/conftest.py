import os

import pandas as pd
import pytest

from recovery.geo import read_records

DATA_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), "data")


@pytest.fixture
def records():
    return read_records(
        os.path.join(DATA_FOLDER, "birds.csv"),
        "lon",
        "lat",
        drop_empty_coords=True,
        crs="epsg:4326"
    )


@pytest.fixture
def expected(records):
    df = pd.read_csv(os.path.join(DATA_FOLDER, "expected.csv"))
    return df.loc[records.index]
