"""

"""
import pandas as pd


def expand_result(names: pd.Series, df: pd.DataFrame):
    """

    Parameters
    ----------
    names
    df

    Returns
    -------

    """
    names = names.copy()
    df = df.copy()

    if not names.name:
        names.name = "__supplied_name"
    df["__name"] = names.dropna().unique()
    df = pd.merge(names, df, left_on=names.name, right_on="__name", how="left")
    df = df.drop(columns=[names.name, "__name"])

    return df
