"""
Test cases for the bdcctools.verification.verify function.
"""
import pandas as pd
import pytest

from bdcctools.verification import verify


@pytest.fixture
def df():
    return pd.DataFrame({
        "species": ["Tremarctos ornatus", "Panthera onca", "Lupus canis"],
        "admin0": ["Colombia", "Mexico", "Venezuela"]
    })


@pytest.fixture
def countries():
    return pd.Series(["Colombia", "Mexico", "Canada"])


def test_flag(df, countries):
    df = verify(df, "admin0", countries, "correct_country", drop=False)
    expected = pd.Series([True, True, False])
    pd.testing.assert_series_equal(df["correct_country"], expected, check_names=False)


def test_suggestions(df, countries):
    df = verify(
        df,
        "admin0",
        countries,
        "correct_country",
        add_suggested=True,
        suggested_name="suggested_country",
        drop=False
    )
    expected = pd.Series([pd.NA, pd.NA, "Canada"])
    pd.testing.assert_series_equal(df["suggested_country"], expected, check_names=False)


def test_drop(df, countries):
    df = verify(df, "admin0", countries, "correct_country", drop=True)
    expected = pd.Series(["Tremarctos ornatus", "Panthera onca"])
    pd.testing.assert_series_equal(df["species"], expected, check_names=False)
