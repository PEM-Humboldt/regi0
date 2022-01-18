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
    drop_empty_coords: bool = False,
    reset_index: bool = True
) -> gpd.GeoDataFrame:
    """
    Reads tabular data (csv, txt, xls or xlsx) and converts it to a
    GeoDataFrame.

    Parameters
    ----------
    fn : str
        Filename with extension. Can be a relative or absolute path.
    lon_col : str
        Name of the longitude column.
    lat_col : str
        Name of the latitude column.
    crs : str
        Coordinate reference system with the corresponding EPSG code.
        Must be in the form epsg:code.
    drop_empty_coords : bool
        Whether to remove rows with missing or incomplete coordinates.
    reset_index : bool
        Whether to reset the result's index after removing rows with
        missing or incomplete coordinates. Only has effect when
        drop_empty_coords is True.

    Returns
    -------
    gpd.GeoDataFrame
        GeoDataFrame with the records.

    """
    dtypes = {lon_col: float, lat_col: float}
    df = read_table(fn, dtype=dtypes)
    geometry = gpd.points_from_xy(df[lon_col], df[lat_col])
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs=crs)

    if drop_empty_coords:
        gdf = gdf.dropna(how="any", subset=[lon_col, lat_col])
    if reset_index:
        gdf = gdf.reset_index()

    return gdf


def read_table(fn: str, **kwargs) -> pd.DataFrame:
    """
    Reads tabular data (csv, txt, xls or xlsx).

    Parameters
    ----------
    fn : str
        Filename with extension. Can be a relative or absolute path.
    **kwargs
        pandas read_csv, read_table and read_excel keyword arguments.

    Returns
    -------
    pd.DataFrame
        DataFrame with the tabular data.

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


def write_table(df: pd.DataFrame, fn: str, **kwargs) -> None:
    """
    Writes tabular data (csv, txt, xls or xlsx) to disk.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to write to disk.
    fn : str
        Filename with extension. Can be a relative or absolute path.
    **kwargs
        Keyword arguments for pandas read_csv, read_table and read_excel
        functions.

    Returns
    -------
    None

    """
    ext = pathlib.Path(fn).suffix
    if ext == ".csv":
        df.to_csv(fn, **kwargs)
    elif ext in (".xls", ".xlsx"):
        df.to_excel(fn, **kwargs)
    else:
        raise ValueError("Input file extension is not supported.")