"""
Test cases for the regi0.geographic.outliers.find_value_outliers function.
"""
import numpy as np
import pandas as pd

from regi0.geographic.outliers import find_value_outliers


def test_iqr(records):
    result = find_value_outliers(
        records, "scientificName", "minimumElevationInMeters", method="iqr"
    )
    expected = pd.Series(
        [
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            True,
            np.nan,
            False,
            np.nan,
            np.nan,
        ]
    )
    pd.testing.assert_series_equal(result, expected)


def test_std(records):
    result = find_value_outliers(
        records, "scientificName", "minimumElevationInMeters", method="std"
    )
    expected = pd.Series(
        [
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            True,
            np.nan,
            False,
            np.nan,
            np.nan,
        ]
    )
    pd.testing.assert_series_equal(result, expected)


def test_zscore(records):
    result = find_value_outliers(
        records, "scientificName", "minimumElevationInMeters", method="zscore"
    )
    expected = pd.Series(
        [
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            True,
            np.nan,
            False,
            np.nan,
            np.nan,
        ]
    )
    pd.testing.assert_series_equal(result, expected)


def test_std_higher_threshold(records):
    result = find_value_outliers(
        records,
        "scientificName",
        "minimumElevationInMeters",
        method="std",
        threshold=3.0,
    )
    expected = pd.Series(
        [
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            np.nan,
            False,
            np.nan,
            np.nan,
        ]
    )
    pd.testing.assert_series_equal(result, expected)


def test_zscore_higher_threshold(records):
    result = find_value_outliers(
        records,
        "scientificName",
        "minimumElevationInMeters",
        method="zscore",
        threshold=3.0,
    )
    expected = pd.Series(
        [
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            np.nan,
            False,
            np.nan,
            np.nan,
        ]
    )
    pd.testing.assert_series_equal(result, expected)
