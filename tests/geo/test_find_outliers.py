import pandas as pd

from recovery.geo import find_outliers


def test_iqr(records, expected):
    records = find_outliers(records, "species", "elevation", "isOutlier", method="iqr")
    pd.testing.assert_series_equal(
        records["isOutlier"], expected["isOutlier1"], check_names=False
    )


def test_std(records, expected):
    records = find_outliers(records, "species", "elevation", "isOutlier", method="std")
    pd.testing.assert_series_equal(
        records["isOutlier"], expected["isOutlier1"], check_names=False
    )


def test_zscore(records, expected):
    records = find_outliers(
        records, "species", "elevation", "isOutlier", method="zscore"
    )
    pd.testing.assert_series_equal(
        records["isOutlier"], expected["isOutlier1"], check_names=False
    )


def test_std_higher_threshold(records, expected):
    records = find_outliers(
        records, "species", "elevation", "isOutlier", method="std", threshold=3.0
    )
    pd.testing.assert_series_equal(
        records["isOutlier"], expected["isOutlier2"], check_names=False
    )


def test_zscore_higher_threshold(records, expected):
    records = find_outliers(
        records, "species", "elevation", "isOutlier", method="zscore", threshold=3.0
    )
    pd.testing.assert_series_equal(
        records["isOutlier"], expected["isOutlier2"], check_names=False
    )
