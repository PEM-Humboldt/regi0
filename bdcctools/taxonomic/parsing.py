"""
Scientific name parsing functions.
"""
import pandas as pd

from bdcctools.taxonomic.constants.qualifiers import QUALIFIERS
from bdcctools.utils import clean_text


def get_canonical_name(names: pd.Series) -> pd.Series:
    """

    Parameters
    ----------
    names

    Returns
    -------

    """
    names = clean_text(names)
    names = names.str.capitalize()

    qualifiers = pd.Series(sum(QUALIFIERS.values(), []))
    qualifiers = qualifiers.str.replace(".", "", regex=False)
    qualifiers = pd.unique(qualifiers.str.split(" ", expand=True).stack())
    names = names.str.split(" ", expand=True).replace(qualifiers, "")
    names = names.fillna("")
    names = names.apply(lambda x: " ".join(x), axis=1)
    names = clean_text(names)

    return names.str.split(" ").str[:2].str.join(" ")
