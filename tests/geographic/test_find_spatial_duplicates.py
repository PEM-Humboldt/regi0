import pandas as pd
from calidatos.geographic import find_spatial_duplicates


def test_records_bounds_high_res(records, expected):
    result = find_spatial_duplicates(
        records, "species", "isSpatialDuplicate", 0.008333333767967150002
    )
    pd.testing.assert_series_equal(
        result["isSpatialDuplicate"],
        expected["isSpatialDuplicate1"],
        check_dtype=False,
        check_names=False
    )


def test_colombia_bounds_low_res(records, expected):
    result = find_spatial_duplicates(
        records,
        "species",
        "isSpatialDuplicate",
        0.1333333402874744,
        bounds=(-78.9909352282, -4.29818694419, -66.8763258531, 12.4373031682)
    )
    pd.testing.assert_series_equal(
        result["isSpatialDuplicate"],
        expected["isSpatialDuplicate2"],
        check_dtype=False,
        check_names=False
    )


def test_mark_tail(records, expected):
    result = find_spatial_duplicates(
        records, "species", "isSpatialDuplicate", 0.008333333767967150002, mark="tail"
    )
    pd.testing.assert_series_equal(
        result["isSpatialDuplicate"],
        expected["isSpatialDuplicate3"],
        check_dtype=False,
        check_names=False
    )


def test_mark_head(records, expected):
    result = find_spatial_duplicates(
        records, "species", "isSpatialDuplicate", 0.008333333767967150002, mark="head"
    )
    pd.testing.assert_series_equal(
        result["isSpatialDuplicate"],
        expected["isSpatialDuplicate4"],
        check_dtype=False,
        check_names=False
    )
