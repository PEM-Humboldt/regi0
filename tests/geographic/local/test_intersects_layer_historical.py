"""
Test cases for the regi0.geographic.local.intersects_layer_historical function.
"""
import numpy as np
import pandas as pd

from regi0.geographic.local import intersects_layer_historical


def test_direction_backward(records, data_path):
    result = intersects_layer_historical(
        records,
        data_path.joinpath("gpkg/admin1.gpkg"),
        date_col="eventDate",
        direction="backward",
    )
    expected = pd.Series(
        [
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            np.nan,
            np.nan,
            True,
            True,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
        ]
    )
    pd.testing.assert_series_equal(result, expected)


def test_direction_nearest(records, data_path):
    result = intersects_layer_historical(
        records,
        data_path.joinpath("gpkg/admin1.gpkg"),
        date_col="eventDate",
        direction="nearest",
    )
    expected = pd.Series(
        [
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            np.nan,
            True,
            True,
            np.nan,
            np.nan,
            True,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
        ]
    )
    pd.testing.assert_series_equal(result, expected)


def test_direction_forward(records, data_path):
    result = intersects_layer_historical(
        records,
        data_path.joinpath("gpkg/admin1.gpkg"),
        date_col="eventDate",
        direction="forward",
    )
    expected = pd.Series(
        [
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            np.nan,
            np.nan,
            np.nan,
            True,
            np.nan,
            np.nan,
            True,
            np.nan,
            np.nan,
            True,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
        ]

    )
    pd.testing.assert_series_equal(result, expected)


def test_source(records, data_path):
    result, source = intersects_layer_historical(
        records,
        data_path.joinpath("gpkg/admin1.gpkg"),
        date_col="eventDate",
        direction="forward",
        return_source=True
    )
    expected = pd.Series(
        [
            "admin1_2011",
            "admin1_2011",
            "admin1_2011",
            "admin1_2011",
            "admin1_2003",
            "admin1_2003",
            "admin1_2003",
            "admin1_2003",
            np.nan,
            np.nan,
            np.nan,
            "admin1_1973",
            np.nan,
            np.nan,
            "admin1_2011",
            np.nan,
            np.nan,
            "admin1_1973",
            np.nan,
            np.nan,
            np.nan,
            np.nan,
        ]
    )
    pd.testing.assert_series_equal(source, expected)


def test_folder(records, data_path):
    result = intersects_layer_historical(
        records,
        data_path.joinpath("shp/"),
        date_col="eventDate",
        direction="nearest",
    )
    expected = pd.Series(
        [
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            np.nan,
            True,
            True,
            np.nan,
            np.nan,
            True,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
        ]
    )
    pd.testing.assert_series_equal(result, expected)
