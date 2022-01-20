"""
Test cases for the regi0.geographic._helpers.get_nearest_year function.
"""
import numpy as np
import pandas as pd
import pytest

from regi0.geographic._helpers import get_nearest_year


@pytest.fixture()
def dates():
    return pd.Series(["17/08/1945", np.nan, "21/09/2011", "01/01/1984", "17/04/2009"])


@pytest.fixture()
def years():
    return [1980, 2010, 2014, 1963]


def test_direction_backwards(dates, years):
    result = get_nearest_year(dates, years, direction="backward")
    expected = pd.Series([np.nan, np.nan, 2010, 1980, 1980])
    pd.testing.assert_series_equal(result, expected)


def test_direction_nearest(dates, years):
    result = get_nearest_year(dates, years, direction="nearest")
    expected = pd.Series([1963, np.nan, 2010, 1980, 2010])
    pd.testing.assert_series_equal(result, expected)


def test_direction_forward(dates, years):
    result = get_nearest_year(dates, years, direction="forward")
    expected = pd.Series([1963, np.nan, 2014, 2010, 2010])
    pd.testing.assert_series_equal(result, expected)


def test_default_year_first(dates, years):
    result = get_nearest_year(dates, years, direction="backward", default_year="first")
    expected = pd.Series([1963, np.nan, 2010, 1980, 1980])
    pd.testing.assert_series_equal(result, expected)


def test_default_year_last(dates, years):
    result = get_nearest_year(dates, years, direction="backward", default_year="last")
    expected = pd.Series([2014, np.nan, 2010, 1980, 1980])
    pd.testing.assert_series_equal(result, expected)
