"""
Test cases for the regi0.verification.match function.
"""
import numpy as np
import pandas as pd
import pytest

from regi0.verification import match


@pytest.fixture
def left():
    return pd.Series(
        [
            np.nan,
            "Nariño",
            "Amazonas",
            "chocó",
            "Guajira",
            "Vichada",
            "BOYACÁ",
            "Santander",
            "Putumallo",
            "NORTE SANTANDER",
            np.nan,
            "Roraima",
        ]
    )


@pytest.fixture
def right():
    return pd.Series(
        [
            "Santander",
            "NARINO",
            "Amazonas",
            "Choco",
            "La Guajira",
            "Casanare",
            "boyaca",
            "Norte de santander",
            "Putumayo",
            "Norte de Santander",
            np.nan,
            np.nan,
        ]
    )


def test_exact(left, right):
    result = match(left, right, preprocess=False, fuzzy=False)
    expected = pd.Series(
        [
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
            np.nan,
            np.nan,
        ]
    )
    pd.testing.assert_series_equal(result, expected, check_dtype=False)


def test_preprocess(left, right):
    result = match(left, right, preprocess=True, fuzzy=False)
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
            np.nan,
            np.nan,
        ]
    )
    pd.testing.assert_series_equal(result, expected, check_dtype=False)


def test_fuzzy_preprocess(left, right):
    result = match(left, right, preprocess=True, fuzzy=True)
    expected = pd.Series(
        [False, True, True, True, True, False, True, False, True, True, np.nan, np.nan]
    )
    pd.testing.assert_series_equal(result, expected, check_dtype=False)
