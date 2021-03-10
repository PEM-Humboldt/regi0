"""
I/O common functions.
"""
import pathlib

import geopandas as gpd
import pandas as pd


def read_geographic_table(
    fn: str,
    lon_col: str,
    lat_col: str,
    crs: str = "epsg:4326",
) -> gpd.GeoDataFrame:
    """
    Reads tabular data (csv, txt, xls or xlsx) and converts it to a
    GeoDataFrame.

    Parameters
    ----------
    fn:      Filename with extension. Can be a relative or absolute path.
    lon_col: Name of the longitude column.
    lat_col: Name of the latitude column.
    crs:     Coordinate reference system with the corresponding EPSG code.
             Must be in the form epsg:code.

    Returns
    -------
    GeoDataFrame.
    """
    dtypes = {lon_col: float, lat_col: float}
    df = read_table(fn, dtype=dtypes)
    geometry = gpd.points_from_xy(df[lon_col], df[lat_col])
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs=crs)

    return gdf


def read_table(fn: str, **kwargs) -> pd.DataFrame:
    """
    Reads tabular data (csv, txt, xls or xlsx).

    Parameters
    ----------
    fn:     Filename with extension. Can be a relative or absolute path.
    kwargs: pandas read_csv, read_table and read_excel keyword arguments.

    Returns
    -------
    DataFrame.
    """
    ext = pathlib.Path(fn).suffix
    if ext == ".csv":
        df = pd.read_csv(fn, **kwargs)
    elif ext == ".txt":
        df = pd.read_table(fn, **kwargs)
    elif ext in (".xls", ".xlsx"):
        df = pd.read_excel(fn, **kwargs)
    else:
        raise ValueError("Input file extension is not supported.")

    return df
