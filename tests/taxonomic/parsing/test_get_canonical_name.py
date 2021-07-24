"""
Test cases for the bdcctools.taxonomic.parsing.clean_names function.
"""
import pandas as pd

from bdcctools.taxonomic.parsing import get_canonical_name


# @pytest.fixture()
# def names():
#     return pd.Series(
#         [
#             "Caluromys lanatus (Olfers, 1818)",
#             "Didelphis aliventris Lund, 1840",
#             "[Colobothea aleata Bates, 1885]",
#             "Anadenanthera pergrina (L.) Speg.",
#             "Thamnophilus doliatus Lafresnaye 1844)",
#             "Lonchurus cf lanceolatus",
#             "Caenolestes aff. convelatus",
#             "Caenolestes ? fuliginosus"
#         ]
#     )
#
#
# @pytest.fixture()
# def expected():
#     return pd.Series(
#         [
#             "Caluromys lanatus",
#             "Didelphis aliventris",
#             "Colobothea aleata",
#             "Anadenanthera pergrina",
#             "Thamnophilus doliatus",
#             "Lonchurus lanceolatus",
#             "Caenolestes convelatus",
#             "Caenolestes fuliginosus"
#         ]
#     )


def test_authors():
    names = pd.Series([
        "Caluromys lanatus (Olfers, 1818)",
        "Didelphis aliventris Lund, 1840",
        "Thamnophilus doliatus Lafresnaye 1844)",
        "Estola vulgaris Galileo & Martins, 1999"
    ])
    expected = pd.Series([
        "Caluromys lanatus",
        "Didelphis aliventris",
        "Thamnophilus doliatus",
        "Estola vulgaris"
    ])
    pd.testing.assert_series_equal(get_canonical_name(names), expected)


def test_canonical():
    names = pd.Series([
        "Panthera onca",
        "tremarctos ornatus",
        "HOMO SAPIENS",
        "Eunectes Murinus"
    ])
    expected = pd.Series([
        "Panthera onca",
        "Tremarctos ornatus",
        "Homo sapiens",
        "Eunectes murinus"
    ])


def test_qualifiers():
    names = pd.Series([
        "Caenolestes aff. convelatus Anthony, 1924",
        "Lonchurus cf. lanceolatus (Bloch 1788)",
        "Unio spp.",
        "Lekanesphaera indet.",
        "Petrolisthes sp. nov. aff. rufescens",
        "Pseudocandona ex gr. eremita",
        "Nucula sp.",
        "Agenus? album"
    ])
    expected = pd.Series([
        "Caenolestes convelatus",
        "Lonchurus lanceolatus",
        "Unio",
        "Lekanesphaera",
        "Petrolisthes rufescens",
        "Pseudocandona eremita",
        "Nucula",
        "Agenus album"
    ])
    pd.testing.assert_series_equal(get_canonical_name(names), expected)
