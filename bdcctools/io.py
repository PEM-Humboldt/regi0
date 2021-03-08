"""
I/O common functions.
"""
import pathlib

import pandas as pd


def read_table(fn: str) -> pd.DataFrame:
    """

    Parameters
    ----------
    fn

    Returns
    -------

    """
    ext = pathlib.Path(fn).suffix
    if ext == ".csv":
        df = pd.read_csv(fn)
    elif ext == ".txt":
        df = pd.read_table(fn)
    elif ext in (".xls", ".xlsx"):
        df = pd.read_excel(fn)

    return df
