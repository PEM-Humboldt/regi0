"""
Configuration file for the regi0.geographic module tests.
"""
import pathlib

import pytest

from regi0.readers import read_geographic_table


@pytest.fixture(scope="session")
def data_path():
    return pathlib.Path(__file__).parents[0].joinpath("data").resolve()


@pytest.fixture(scope="session")
def records(data_path):
    return read_geographic_table(
        data_path.joinpath("csv/birds.csv"),
        "decimalLongitude",
        "decimalLatitude",
        crs="epsg:4326",
        drop_empty_coords=True,
        reset_index=True
    )
