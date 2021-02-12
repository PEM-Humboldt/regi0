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
    df = df.copy()

    if not names.name:
        names.name = "__supplied_name"
    df["name"] = names.dropna().unique()
    df = pd.merge(names, df, left_on=names.name, right_on="name")
    df = df.drop(columns=[names.name, "name"])

    return df
