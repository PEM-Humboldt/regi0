"""
Helper functions for the taxonomic module.
"""
import pandas as pd


def expand_result(df: pd.DataFrame, names: pd.Series) -> pd.DataFrame:
    """
    Expands `df` rows to match `names` size by duplicating rows for
    duplicated names.

    Parameters
    ----------
    df : DataFrame
        DataFrame to expand.
    names : Series
        Series with species names.

    Returns
    -------
    DataFrame
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
