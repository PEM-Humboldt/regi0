"""
Test cases for the regi0.geographic.local.get_layer_field_historical function.
"""
import numpy as np
import pandas as pd

from regi0.geographic.local import get_layer_field_historical


def test_direction_backward(records, data_path):
    result = get_layer_field_historical(
        records,
        data_path.joinpath("gpkg/admin1.gpkg"),
        date_col="eventDate",
        field="dptos",
        direction="backward",
    )
    expected = pd.Series(
        [
            "BOYACA",
            "BOYACA",
            "BOYACA",
            "BOYACA",
            "SANTANDER",
            "SANTANDER",
            "SANTANDER",
            "SANTANDER",
            "SANTANDER",
            "SANTANDER",
            "BOYACA",
            np.nan,
            np.nan,
            "BOYACA",
            "BOYACA",
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
        ]
    )
    pd.testing.assert_series_equal(result, expected, check_names=False)


def test_direction_nearest(records, data_path):
    result = get_layer_field_historical(
        records,
        data_path.joinpath("gpkg/admin1.gpkg"),
        date_col="eventDate",
        field="dptos",
        direction="nearest",
    )
    expected = pd.Series(
        [
            "BOYACA",
            "BOYACA",
            "BOYACA",
            "BOYACA",
            "SANTANDER",
            "SANTANDER",
            "SANTANDER",
            "SANTANDER",
            "SANTANDER",
            "SANTANDER",
            "BOYACA",
            "BOYACA",
            np.nan,
            "BOYACA",
            "BOYACA",
            np.nan,
            np.nan,
            "SANTANDER",
            np.nan,
            np.nan,
            np.nan,
            np.nan,
        ]
    )
    pd.testing.assert_series_equal(result, expected, check_names=False)


def test_direction_forward(records, data_path):
    result = get_layer_field_historical(
        records,
        data_path.joinpath("gpkg/admin1.gpkg"),
        date_col="eventDate",
        field="dptos",
        direction="forward",
    )
    expected = pd.Series(
        [
            "BOYACA",
            "BOYACA",
            "BOYACA",
            "BOYACA",
            "SANTANDER",
            "SANTANDER",
            "SANTANDER",
            "BOYACA",
            np.nan,
            np.nan,
            np.nan,
            "BOYACA",
            np.nan,
            np.nan,
            "BOYACA",
            np.nan,
            np.nan,
            "SANTANDER",
            np.nan,
            np.nan,
            np.nan,
            np.nan,
        ]
    )
    pd.testing.assert_series_equal(result, expected, check_names=False)


def test_source(records, data_path):
    result, source = get_layer_field_historical(
        records,
        data_path.joinpath("gpkg/admin1.gpkg"),
        date_col="eventDate",
        field="dptos",
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
    pd.testing.assert_series_equal(source, expected, check_names=False)


def test_folder(records, data_path):
    result = get_layer_field_historical(
        records,
        data_path.joinpath("shp/"),
        date_col="eventDate",
        field="dptos",
        direction="nearest",
    )
    expected = pd.Series(
        [
            "BOYACA",
            "BOYACA",
            "BOYACA",
            "BOYACA",
            "SANTANDER",
            "SANTANDER",
            "SANTANDER",
            "SANTANDER",
            "SANTANDER",
            "SANTANDER",
            "BOYACA",
            "BOYACA",
            np.nan,
            "BOYACA",
            "BOYACA",
            np.nan,
            np.nan,
            "SANTANDER",
            np.nan,
            np.nan,
            np.nan,
            np.nan,
        ]
    )
    pd.testing.assert_series_equal(result, expected, check_names=False)

