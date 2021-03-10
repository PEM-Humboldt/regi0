"""

"""
from typing import Union

import geopandas as gpd
import pandas as pd


def verify(
    df: Union[gpd.GeoDataFrame, pd.DataFrame],
    observed_col: str,
    expected: pd.Series,
    flag_name: str,
    add_suggested: bool = False,
    suggested_name: str = None,
    drop: bool = False
) -> Union[gpd.GeoDataFrame, pd.DataFrame]:
    """

    Parameters
    ----------
    df
    observed_col
    expected
    flag_name
    add_suggested
    suggested_name
    drop

    Returns
    -------

    """
    # Make sure to modify a copy of the original DataFrame instead of
    # modifying it in place.
    df = df.copy()

    df[flag_name] = df[observed_col] == expected
    if add_suggested:
        df.loc[~df[flag_name], suggested_name] = expected.loc[~df[flag_name]]

    if drop:
        df = df[~df[flag_name]]

    return df
