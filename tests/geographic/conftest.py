"""
Configuration file for the regi0.geographic module tests.
"""
import pathlib

import pytest

from regi0.readers import read_geographic_table

DATA_FOLDER = pathlib.Path(__file__).parents[0].joinpath("data")


@pytest.fixture(scope="session")
def records():
    return read_geographic_table(
        DATA_FOLDER.joinpath("csv/birds.csv"),
        "decimalLongitude",
        "decimalLatitude",
        crs="epsg:4326",
        drop_empty_coords=True,
        reset_index=True
    )
