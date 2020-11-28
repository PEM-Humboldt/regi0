import os

import pandas as pd
import pytest

from recovery.geographic import check_historical

DATA_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), "data")


@pytest.fixture(scope="module")
def kwargs():
    return dict(
        date_col="earliestDateCollected",
        flag_name="correctDepartment",
        direction="backward",
        op="match",
        left_col="adm1",
        right_col="dptos",
        suggested_name="suggestedDepartment"
    )


@pytest.fixture(scope="module")
def result_gpkg(records, kwargs):
    return check_historical(
        records, os.path.join(DATA_FOLDER, "gpkg", "admin1.gpkg"), **kwargs
    )


@pytest.fixture(scope="module")
def result_shp(records, kwargs):
    return check_historical(records, os.path.join(DATA_FOLDER, "shp"), **kwargs)


def test_flag_gpkg(result_gpkg, expected):
    pd.testing.assert_series_equal(
        result_gpkg["correctDepartment"],
        expected["correctDepartment"],
        check_dtype=False
    )


def test_suggestion_gpkg(result_gpkg, expected):
    pd.testing.assert_series_equal(
        result_gpkg["suggestedDepartment"], expected["suggestedDepartment"]
    )


def test_flag_shp(result_shp, expected):
    pd.testing.assert_series_equal(
        result_shp["correctDepartment"],
        expected["correctDepartment"],
        check_dtype=False
    )


def test_suggestion_shp(result_shp, expected):
    pd.testing.assert_series_equal(
        result_shp["suggestedDepartment"], expected["suggestedDepartment"]
    )


def test_direction_nearest(records, kwargs, expected):
    new_kwargs = kwargs.copy()
    new_kwargs.update(
        dict(direction="nearest", add_source=True, source_name="sourceDepartment")
    )
    result = check_historical(
        records, os.path.join(DATA_FOLDER, "gpkg", "admin1.gpkg"), **new_kwargs
    )
    pd.testing.assert_series_equal(
        result["sourceDepartment"], expected["sourceDepartment1"], check_names=False
    )


def test_direction_forward(records, kwargs, expected):
    new_kwargs = kwargs.copy()
    new_kwargs.update(
        dict(direction="forward", add_source=True, source_name="sourceDepartment")
    )
    result = check_historical(
        records, os.path.join(DATA_FOLDER, "gpkg", "admin1.gpkg"), **new_kwargs
    )
    pd.testing.assert_series_equal(
        result["sourceDepartment"], expected["sourceDepartment2"], check_names=False
    )
