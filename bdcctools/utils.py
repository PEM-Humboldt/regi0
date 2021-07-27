"""
General helper functions.
"""
import pandas as pd


def clean_text(s: pd.Series) -> pd.Series:
    """
    Removes special characters, leading, trailing and multiple whitespaces
    from text values in a pandas Series.

    Parameters
    ----------
    s: Pandas series to clean.

    Returns
    -------
    Clean Series.
    """
    s = s.replace(r"\d+|[^\w\s]+", "", regex=True)
    s = s.replace(r"\s+", " ", regex=True)
    s = s.str.strip()

    return s


def standardize_text(s: pd.Series) -> pd.Series:
    """

    Parameters
    ----------
    s
    Returns
    -------

    """
    s = clean_text(s)
    s = s.str.lower()
    s = s.str.normalize("NFKD").str.encode("ascii", errors="ignore").str.decode("utf-8")

    return s
