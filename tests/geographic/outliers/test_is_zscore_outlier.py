"""
Test cases for the regi0.geographic.outliers._is_zscore_outlier function.
"""
import numpy as np
import pytest

from regi0.geographic.outliers import _is_zscore_outlier


@pytest.fixture()
def values():
    return np.array([52, 56, 53, 57, 51, 59, 1, 99])


def test_zscore(values):
    result = _is_zscore_outlier(values)
    expected = np.array([False, False, False, False, False, False,  True, False])
    np.testing.assert_array_equal(result, expected)


def test_zscore_smaller_threshold(values):
    result = _is_zscore_outlier(values, threshold=1.0)
    expected = np.array([False, False, False, False, False, False,  True, True])
    np.testing.assert_array_equal(result, expected)


def test_zscore_greater_threshold(values):
    result = _is_zscore_outlier(values, threshold=3.0)
    expected = np.array([False, False, False, False, False, False,  False, False])
    np.testing.assert_array_equal(result, expected)
