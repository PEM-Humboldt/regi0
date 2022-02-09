"""
Test cases for the regi0.geographic.web.arcgis.get_feature_layer_field function.
"""
import numpy as np
import pandas as pd
import pytest

from regi0.geographic.web.arcgis import get_feature_layer_field


def test_success(records, success):
    result = get_feature_layer_field(
        records,
        "https://foobar.com/P3ePLMYs2RVChkJx/arcgis/rest/services/service/query",
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


def test_error(records, error):
    with pytest.raises(Exception):
        get_feature_layer_field(
            records,
            "https://foobar.com/P3ePLMYs2RVChkJx/arcgis/rest/services/service/query",
            field="dptos",
        )


def test_bad_request(records, error):
    with pytest.raises(Exception):
        get_feature_layer_field(
            records,
            "https://foobar.com/P3ePLMYs2RVChkJx/arcgis/rest/services/service/query",
            field="dptos",
        )
