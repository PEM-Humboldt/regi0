"""
Test cases for the regi0.geographic.local.intersects_layer function.
"""
import geopandas as gpd
import pandas as pd

from regi0.geographic.local import intersects_layer


def test_geodataframe(records, data_path):
    countries = gpd.read_file(
        data_path.joinpath("gpkg/admin0.gpkg"), layer="admin0_2018"
    )
    result = intersects_layer(records, countries)
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
        ]
    )
    pd.testing.assert_series_equal(result, expected, check_dtype=False)


def test_geojson(records, data_path):
    result = intersects_layer(
        records,
        data_path.joinpath("geojson/urban.geojson"),
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
            True,
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
            False,
        ]
    )
    pd.testing.assert_series_equal(result, expected, check_dtype=False)


def test_geopackage(records, data_path):
    result = intersects_layer(
        records,
        data_path.joinpath("gpkg/admin0.gpkg"),
        layer="admin0_2018"
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
        ]
    )
    pd.testing.assert_series_equal(result, expected, check_dtype=False)


def test_shapefile(records, data_path):
    result = intersects_layer(
        records,
        data_path.joinpath("shp/admin1_2003.shp"),
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
            True,
            True,
            True,
            True,
            True,
            True,
            False,
            True,
            False,
            False,
        ]
    )
    pd.testing.assert_series_equal(result, expected, check_dtype=False)
