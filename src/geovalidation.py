import os

import geopandas
import pandas as pd


def drop_empty_coords(
    gdf: geopandas.geodataframe.GeoDataFrame, longitude_col: str, latitude_col: str
) -> geopandas.geodataframe.GeoDataFrame:
    """

    Parameters
    ----------
    gdf

    Returns
    -------

    """
    mask = ~gdf[longitude_col].isna() & ~gdf[latitude_col].isna()
    return gdf[mask]


def read_input(input: str, dtypes: dict, ) -> geopandas.geodataframe.GeoDataFrame:
    """

    Parameters
    ----------
    input

    Returns
    -------

    """
    dtypes = {longitude_col: float, latitude_col: float}

    input_ext = os.path.splitext(input)[1]
    if input_ext == ".csv":
        records = pd.read_csv(input, dtype=dtypes)
    elif input_ext == ".xlsx":
        records = pd.read_excel(input, dtype=dtypes)
    else:
        pass

    records = drop_empty_coords(records, longitude_col, latitude_col)

    geometry = geopandas.points_from_xy(records[longitude_col], records[latitude_col])

    return geopandas.GeoDataFrame(records, geometry=geometry)
