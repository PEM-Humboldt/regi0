import pandas as pd
from bdcctools.geographic import find_outliers


def test_iqr(records, expected):
    result = find_outliers(records, "species", "elevation", "isOutlier", method="iqr")
    pd.testing.assert_series_equal(
        result["isOutlier"], expected["isOutlier1"], check_names=False
    )


def test_std(records, expected):
    result = find_outliers(records, "species", "elevation", "isOutlier", method="std")
    pd.testing.assert_series_equal(
        result["isOutlier"], expected["isOutlier1"], check_names=False
    )


def test_zscore(records, expected):
    result = find_outliers(
        records, "species", "elevation", "isOutlier", method="zscore"
    )
    pd.testing.assert_series_equal(
        result["isOutlier"], expected["isOutlier1"], check_names=False
    )


def test_std_higher_threshold(records, expected):
    result = find_outliers(
        records, "species", "elevation", "isOutlier", method="std", threshold=3.0
    )
    pd.testing.assert_series_equal(
        result["isOutlier"], expected["isOutlier2"], check_names=False
    )


def test_zscore_higher_threshold(records, expected):
    result = find_outliers(
        records, "species", "elevation", "isOutlier", method="zscore", threshold=3.0
    )
    pd.testing.assert_series_equal(
        result["isOutlier"], expected["isOutlier2"], check_names=False
    )
