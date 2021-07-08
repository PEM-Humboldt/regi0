"""
Test cases for the bdcctools.taxonomic.utils.clean_names function.
"""
import pandas as pd
import pytest

from bdcctools.taxonomic.utils import clean_names


@pytest.fixture()
def names():
    return pd.Series(
        [
            "Caluromys lanatus (Olfers, 1818)",
            "Didelphis aliventris Lund, 1840",
            "[Colobothea aleata Bates, 1885]",
            "Anadenanthera pergrina (L.) Speg.",
            "Thamnophilus doliatus Lafresnaye 1844)",
            "Lonchurus cf lanceolatus",
            "Caenolestes aff. convelatus",
            "Caenolestes ? fuliginosus"
        ]
    )


@pytest.fixture()
def expected():
    return pd.Series(
        [
            "Caluromys lanatus",
            "Didelphis aliventris",
            "Colobothea aleata",
            "Anadenanthera pergrina",
            "Thamnophilus doliatus",
            "Lonchurus lanceolatus",
            "Caenolestes convelatus",
            "Caenolestes fuliginosus"
        ]
    )


def test_clean(names, expected):
    pd.testing.assert_series_equal(clean_names(names), expected)
