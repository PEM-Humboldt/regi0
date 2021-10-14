"""
Scientific name parsing functions.
"""
import pandas as pd

from regi0.taxonomic.constants.qualifiers import QUALIFIERS
from regi0.utils import clean_text


def get_canonical_name(names: pd.Series) -> pd.Series:
    """
    Extracts the canonical name (genus and specific epithet) of a Series
    of scientific names. It does this by removing special characters,
    numbers and Open Nomenclature qualifiers (such as aff. or cf.) and
    then taking the first two words.

    Parameters
    ----------
    names
        Series with the scientific names.

    Returns
    -------
    pd.Series
        Series with the extracted canonical names.

    """
    names = clean_text(names)
    names = names.str.capitalize()

    qualifiers = pd.Series(sum(QUALIFIERS.values(), []))
    qualifiers = qualifiers.str.replace(".", "", regex=False)
    qualifiers = pd.unique(qualifiers.str.split(" ", expand=True).stack())
    names = names.str.split(" ", expand=True).replace(qualifiers, pd.NA)
    names = names.apply(lambda x: x.str.cat(sep=" "), axis=1)
    names = clean_text(names)

    return names.str.split(" ").str[:2].str.join(" ")
