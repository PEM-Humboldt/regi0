"""
Test cases for the regi0.geographic.local.find_spatial_duplicates function.
"""
import pandas as pd

from regi0.geographic.local import find_spatial_duplicates


def test_records_bounds_high_res(records):
    result = find_spatial_duplicates(
        records,
        "scientificName",
        resolution=0.008333333767967150002,
    )
    expected = pd.Series(
        [
            True,
            True,
            True,
            True,
            True,
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
            True,
            False,
            False,
            False,
            False,
            False,
        ]
    )
    pd.testing.assert_series_equal(result, expected, check_dtype=False)


def test_other_bounds_low_res(records):
    result = find_spatial_duplicates(
        records,
        "scientificName",
        resolution=0.1333333402874744,
        bounds=(-78.9909352282, -4.29818694419, -66.8763258531, 12.4373031682),
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
            False,
            False,
            True,
            True,
            True,
            False,
            False,
            True,
            True,
            True,
            False,
            True,
            False,
            False,
            True,
        ]
    )
    pd.testing.assert_series_equal(result, expected, check_dtype=False)


def test_keep_first(records):
    result = find_spatial_duplicates(
        records, "scientificName", resolution=0.008333333767967150002, keep="first"
    )
    expected = pd.Series(
        [
            False,
            True,
            True,
            True,
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
            True,
            False,
            False,
            False,
            False,
            False,
        ]
    )
    pd.testing.assert_series_equal(result, expected, check_dtype=False)


def test_keep_last(records):
    result = find_spatial_duplicates(
        records, "scientificName", resolution=0.008333333767967150002, keep="last"
    )
    expected = pd.Series(
        [
            True,
            True,
            True,
            True,
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
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
        ]
    )
    pd.testing.assert_series_equal(result, expected, check_dtype=False)
