"""
Test cases for the regi0.geographic.web.arcgis.intersects_feature_layer function.
"""
import pandas as pd
import pytest

from regi0.geographic.web.arcgis import intersects_feature_layer


def test_success(records, success):
    result = intersects_feature_layer(
        records,
        "https://foobar.com/P3ePLMYs2RVChkJx/arcgis/rest/services/service/query",
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


def test_error(records, error):
    with pytest.raises(Exception):
        intersects_feature_layer(
            records,
            "https://foobar.com/P3ePLMYs2RVChkJx/arcgis/rest/services/service/query",
        )


def test_bad_request(records, bad_request):
    with pytest.raises(Exception):
        intersects_feature_layer(
            records,
            "https://foobar.com/P3ePLMYs2RVChkJx/arcgis/rest/services/service/query",
        )
