"""
Test cases for the regi0.geographic.outliers._is_iqr_outlier function.
"""
import numpy as np
import pytest

from regi0.geographic.outliers import _is_iqr_outlier


@pytest.fixture()
def values():
    return np.array([52, 56, 53, 57, 51, 59, 1, 99])


def test_iqr(values):
    result = _is_iqr_outlier(values)
    expected = np.array([False, False, False, False, False, False,  True, True])
    np.testing.assert_array_equal(result, expected)
