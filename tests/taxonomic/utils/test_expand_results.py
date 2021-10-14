"""
Test cases for the regi0.taxonomic.utils.expand_results function.
"""
import pandas as pd
import pytest

from regi0.taxonomic.utils import expand_result


@pytest.fixture()
def names():
    return pd.Series(
        [
            None,
            "Tremarctos ornatus",
            "Panthera onca",
            None,
            "Panthera onca",
            "Tremarctos ornatus",
        ]
    )


@pytest.fixture()
def df():
    return pd.DataFrame(
        {
            "kingdom": ["Animalia", "Animalia"],
            "phylum": ["Chordata", "Chordata"],
            "class": ["Mammalia", "Mammalia"],
            "order": ["Carnivora", "Carnivora"],
            "family": ["Ursidae", "Felidae"],
            "genus": ["Tremarctos", "Panthera"],
            "species": ["Tremarctos ornatus", "Panthera onca"],
        }
    )


@pytest.fixture()
def result(names, df):
    return expand_result(df, names)


def test_order(result, names):
    pd.testing.assert_series_equal(result["species"], names, check_names=False)


def test_columns(result, df):
    assert (result.columns == df.columns).all()


def test_index(result, names):
    assert (result.index == names.index).all()
