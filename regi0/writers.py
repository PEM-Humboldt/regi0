"""
Functions to write results to disk.
"""
import pathlib
from typing import Union

import pandas as pd


def write_table(df: pd.DataFrame, path: Union[str, pathlib.Path], **kwargs) -> None:
    """
    Writes tabular data (csv, txt, xls or xlsx) to disk.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to write to disk.
    path : str or Path
        Filename with extension. Can be a relative or absolute path.
    **kwargs
        Keyword arguments for pandas read_csv, read_table and read_excel
        functions.

    Returns
    -------
    None

    """
    ext = pathlib.Path(path).suffix
    if ext == ".csv":
        df.to_csv(path, **kwargs)
    elif ext in (".xls", ".xlsx"):
        df.to_excel(path, **kwargs)
    else:
        raise ValueError("Input file extension is not supported.")
