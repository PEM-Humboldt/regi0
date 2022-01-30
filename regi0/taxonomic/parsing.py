"""
Scientific name parsing functions.
"""
import pandas as pd

from ._constants.qualifiers import qualifiers
from .._helpers import clean_text


def get_canonical_name(names: pd.Series) -> pd.Series:
    """
    Extracts the canonical name (genus and specific epithet) of a Series
    of scientific names. It does this by removing special characters,
    numbers and Open Nomenclature qualifiers (such as aff. or cf.) and
    then taking the first two words.

    Parameters
    ----------
    names : Series
        Series with the scientific names.

    Returns
    -------
    Series
        Series with the extracted canonical names.

    """
    names = clean_text(names)
    names = names.str.capitalize()

    abbreviations = pd.Series(sum(qualifiers.values(), []))
    abbreviations = abbreviations.str.replace(".", "", regex=False)
    abbreviations = pd.unique(abbreviations.str.split(" ", expand=True).stack())
    names = names.str.split(" ", expand=True).replace(abbreviations, pd.NA)
    names = names.apply(lambda x: x.str.cat(sep=" "), axis=1)
    names = clean_text(names)

    return names.str.split(" ").str[:2].str.join(" ")
