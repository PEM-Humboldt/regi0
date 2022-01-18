"""
Test cases for the regi0.geographic.utils.is_outlier function.
"""
import numpy as np
import pytest

from regi0.geographic._helpers import is_outlier


@pytest.fixture()
def values():
    return np.array([52, 56, 53, 57, 51, 59, 1, 99])


def test_iqr(values):
    result = is_outlier(values, method="iqr")
    expected = np.array([False, False, False, False, False, False,  True, True])
    np.testing.assert_array_equal(result, expected)


def test_std(values):
    result = is_outlier(values, method="std")
    expected = np.array([False, False, False, False, False, False,  True, False])
    np.testing.assert_array_equal(result, expected)


def test_std_smaller_threshold(values):
    result = is_outlier(values, method="std", threshold=1.0)
    expected = np.array([False, False, False, False, False, False,  True, True])
    np.testing.assert_array_equal(result, expected)


def test_std_greater_threshold(values):
    result = is_outlier(values, method="std", threshold=3.0)
    expected = np.array([False, False, False, False, False, False,  False, False])
    np.testing.assert_array_equal(result, expected)


def test_zscore(values):
    result = is_outlier(values, method="zscore")
    expected = np.array([False, False, False, False, False, False,  True, False])
    np.testing.assert_array_equal(result, expected)


def test_zscore_smaller_threshold(values):
    result = is_outlier(values, method="zscore", threshold=1.0)
    expected = np.array([False, False, False, False, False, False,  True, True])
    np.testing.assert_array_equal(result, expected)


def test_zscore_greater_threshold(values):
    result = is_outlier(values, method="zscore", threshold=3.0)
    expected = np.array([False, False, False, False, False, False,  False, False])
    np.testing.assert_array_equal(result, expected)
