"""
Test cases for the bdcctools.utils.standardize function.
"""
import pandas as pd

from bdcctools.utils import standardize_text


def test_accents():
    values = pd.Series([
        "NARIÑO",
        "Boyacá",
        "chocó",
        "GUAINÍA"
    ])
    expected = pd.Series([
        "narino",
        "boyaca",
        "choco",
        "guainia"
    ])
    pd.testing.assert_series_equal(standardize_text(values), expected)


def test_no_alteration():
    values = pd.Series([
        "vichada",
        "casanare",
        "boyaca",
        "cundinamarca"
    ])
    expected = pd.Series([
        "vichada",
        "casanare",
        "boyaca",
        "cundinamarca"
    ])
    pd.testing.assert_series_equal(standardize_text(values), expected)


def test_numbers():
    values = pd.Series([
        "Lonchurus lanceolatus Bloch 1788",
        "Puma concolor 17 71"
    ])
    expected = pd.Series([
        "lonchurus lanceolatus bloch",
        "puma concolor"
    ])
    pd.testing.assert_series_equal(standardize_text(values), expected)


def test_punctuation():
    values = pd.Series([
        "Puma concolor (Linnaeus)",
        "Estola vulgaris Galileo & Martins",
        "Petrolisthes sp. nov. aff. rufescens"
    ])
    expected = pd.Series([
        "puma concolor linnaeus",
        "estola vulgaris galileo martins",
        "petrolisthes sp nov aff rufescens"
    ])
    pd.testing.assert_series_equal(standardize_text(values), expected)
