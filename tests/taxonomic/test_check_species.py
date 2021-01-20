import pandas as pd
import pytest
from calidatos.taxonomic import check_species


@pytest.fixture(scope="module")
def result(records):
    return check_species(
        records,
        "acceptedNameUsage",
        "acceptedName",
        add_suggested=True,
        suggested_name="suggestedName"
    )


def test_flag(result, expected):
    pd.testing.assert_series_equal(result["acceptedName"], expected["acceptedName"])


def test_suggested(result, expected):
    pd.testing.assert_series_equal(result["suggestedName"], expected["suggestedName"])
