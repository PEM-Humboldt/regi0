"""
Test cases for the regi0.verification.match function.
"""
import pandas as pd
import pytest

from regi0.verification import match


@pytest.fixture
def left():
    return pd.Series([
        "Nariño",
        "Amazonas",
        "chocó",
        "Guajira",
        "Vichada",
        "BOYACÁ",
        "Santander",
        "Putumallo",
        "NORTE SANTANDER"
    ])


@pytest.fixture
def right():
    return pd.Series([
        "NARINO",
        "Amazonas",
        "Choco",
        "La Guajira",
        "Casanare",
        "boyaca",
        "Norte de santander",
        "Putumayo",
        "Norte de Santander"
    ])


def test_exact(left, right):
    expected = pd.Series([
        False,
        True,
        False,
        False,
        False,
        False,
        False,
        False,
        False
    ])
    pd.testing.assert_series_equal(
        match(left, right, preprocess=False, fuzzy=False), expected
    )


def test_preprocess(left, right):
    expected = pd.Series([
        True,
        True,
        True,
        False,
        False,
        True,
        False,
        False,
        False
    ])
    pd.testing.assert_series_equal(
        match(left, right, preprocess=True, fuzzy=False), expected
    )


def test_fuzzy_preprocess(left, right):
    expected = pd.Series([
        True,
        True,
        True,
        True,
        False,
        True,
        False,
        True,
        True
    ])
    pd.testing.assert_series_equal(
        match(left, right, preprocess=True, fuzzy=True), expected
    )
