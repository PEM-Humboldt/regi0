"""
Test cases for the regi0.geographic.local.get_layer_field function.
"""
import geopandas as gpd
import numpy as np
import pandas as pd

from regi0.geographic.local import get_layer_field


def test_geodataframe(records, data_path):
    countries = gpd.read_file(
        data_path.joinpath("gpkg/admin0.gpkg"), layer="admin0_2018"
    )
    result = get_layer_field(records, countries, field="ISO_A2")
    expected = pd.Series(
        [
            "CO",
            "CO",
            "CO",
            "CO",
            "CO",
            "CO",
            "CO",
            "CO",
            "CO",
            "CO",
            "CO",
            "CO",
            "CO",
            "CO",
            "CO",
            "CO",
            "CO",
            "CO",
            "VE",
            "CO",
            "VE",
            "VE",
        ]
    )
    pd.testing.assert_series_equal(result, expected, check_names=False)


def test_geojson(records, data_path):
    result = get_layer_field(
        records,
        data_path.joinpath("geojson/urban.geojson"),
        field="nom_cpob",
    )
    expected = pd.Series(
        [
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            "SAN GIL",
            np.nan,
            np.nan,
            np.nan,
            "SOATA",
            np.nan,
            np.nan,
            np.nan,
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


def test_geopackage(records, data_path):
    result = get_layer_field(
        records,
        data_path.joinpath("gpkg/admin0.gpkg"),
        layer="admin0_2018",
        field="ISO_A2",
    )
    expected = pd.Series(
        [
            "CO",
            "CO",
            "CO",
            "CO",
            "CO",
            "CO",
            "CO",
            "CO",
            "CO",
            "CO",
            "CO",
            "CO",
            "CO",
            "CO",
            "CO",
            "CO",
            "CO",
            "CO",
            "VE",
            "CO",
            "VE",
            "VE",
        ]
    )
    pd.testing.assert_series_equal(result, expected, check_names=False)


def test_shapefile(records, data_path):
    result = get_layer_field(
        records,
        data_path.joinpath("shp/admin1_2003.shp"),
        field="dptos",
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
            "SANTANDER",
            "SANTANDER",
            "BOYACA",
            "BOYACA",
            "SANTANDER",
            "SANTANDER",
            "BOYACA",
            "SANTANDER",
            "BOYACA",
            "SANTANDER",
            np.nan,
            "BOYACA",
            np.nan,
            np.nan,
        ]
    )
    pd.testing.assert_series_equal(result, expected, check_names=False)
