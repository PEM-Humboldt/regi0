"""
Test cases for the bdcctools.utils.clean_text function.
"""
import pandas as pd

from bdcctools.utils import clean_text


def test_numbers():
    values = pd.Series([
        "Lonchurus lanceolatus Bloch 1788",
        "Puma concolor 17 71"
    ])
    expected = pd.Series([
        "Lonchurus lanceolatus Bloch",
        "Puma concolor"
    ])
    pd.testing.assert_series_equal(clean_text(values), expected)


def test_punctuation():
    values = pd.Series([
        "Puma concolor (Linnaeus)",
        "Estola vulgaris Galileo & Martins",
        "Petrolisthes sp. nov. aff. rufescens"
    ])
    expected = pd.Series([
        "Puma concolor Linnaeus",
        "Estola vulgaris Galileo Martins",
        "Petrolisthes sp nov aff rufescens"
    ])
    pd.testing.assert_series_equal(clean_text(values), expected)


def test_spaces():
    values = pd.Series([
        "Tremarctos ornatus ",
        " Panthera onca",
        " Cocos nucifera ",
        "Puma  concolor",
        "Norte de santander",
        "La \t Guajira",
        "Riohacha\n"
    ])
    expected = pd.Series([
        "Tremarctos ornatus",
        "Panthera onca",
        "Cocos nucifera",
        "Puma concolor",
        "Norte de santander",
        "La Guajira",
        "Riohacha"
    ])
    pd.testing.assert_series_equal(clean_text(values), expected)
