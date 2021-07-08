"""
Helper functions for the taxonomic module.
"""
import pandas as pd


def clean_names(names: pd.Series) -> pd.Series:
    """

    Parameters
    ----------
    names

    Returns
    -------

    """
    exceptions = ["aff", "cf"]

    names = names.str.replace(r"[^\w\s]+", "", regex=True)
    names = names.str.replace(r"\d+", "", regex=True)
    for exception in exceptions:
        names = names.str.replace(exception, "")
    names = names.replace(r"\s+", ' ', regex=True)
    names = names.str.split(" ").str[:2].str.join(" ")

    return names


def expand_result(df: pd.DataFrame, names: pd.Series) -> pd.DataFrame:
    """
    Expands `df` rows to match `names` size by duplicating rows for
    duplicated names.

    Parameters
    ----------
    df:    pandas DataFrame to expand.
    names: pandas Series with species names.

    Returns
    -------
    Copy of `df` wih duplicated rows to match `names` size.
    """
    df = df.copy()
    names = names.copy()

    if not names.name:
        names.name = "__supplied_name"
    df["__name"] = names.dropna().unique()
    df = pd.merge(names, df, left_on=names.name, right_on="__name", how="left")
    df = df.drop(columns=[names.name, "__name"])

    return df
