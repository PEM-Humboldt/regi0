import os

import geopandas as gpd
import pandas as pd
import pytest
from recovery.geographic import check_intersection

DATA_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), "data")


@pytest.fixture(scope="module")
def other():
    return gpd.read_file(os.path.join(DATA_FOLDER, "geojson", "urban.geojson"))


def test_check_intersection(records, other, expected):
    result = check_intersection(records, other, "isUrban")
    pd.testing.assert_series_equal(
        result["isUrban"], expected["isUrban"], check_dtype=False
    )
