import os

import geopandas as gpd
import pandas as pd
import pytest

from recovery.geo import check_intersection

DATA_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), "data")


@pytest.fixture
def other():
    return gpd.read_file(os.path.join(DATA_FOLDER, "urban.geojson"))


def test_check_intersection(records, other, expected):
    records = check_intersection(records, other, "isUrban")
    pd.testing.assert_series_equal(
        records["isUrban"], expected["isUrban"], check_dtype=False
    )
