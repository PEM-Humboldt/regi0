"""
Functions to identify geographic duplicates.
"""
from typing import Union

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
import rasterstats


def _create_id_grid(
    xmin: float,
    ymin: float,
    xmax: float,
    ymax: float,
    resolution: float,
    crs: str = "epsg:4326",
) -> rasterio.io.DatasetWriter:
    """
    Creates an in-memory raster with a grid where each pixel has a unique
    ID. The unique IDs start at 0 in the upper left corner and increments
    from left to right and top to bottom. The max value for unique ID
    will be (height * width) - 1.

    Parameters
    ----------
    xmin : float
        Upper-left corner x coordinate.
    ymin : float
        Lower-right corner y coordinate.
    xmax : float
        Lower-left corner x coordinate.
    ymax : float
        Upper-left corner y coordinate.
    resolution : float
        Pixel resolution.
    crs : str
        Coordinate Reference System. Must be in the form epsg:code.

    Returns
    -------
    DatasetWriter
        In-memory raster with unique IDs.

    Notes
    -----
    Coordinates and resolution should match with the reference system
    passed in crs.

    """
    height = np.ceil((ymax - ymin) / resolution).astype(int)
    width = np.ceil((xmax - xmin) / resolution).astype(int)
    transform = rasterio.transform.from_origin(xmin, ymax, resolution, resolution)

    # The unique ID values to fill the grid with start from 1 to make sure
    # the value 0 is reserved for no-data and that the whole numeric range
    # of a 32-bit unsigned integer is available for IDs (in the very
    # unlikely case this is needed).
    arr = np.arange(1, (height * width) + 1, dtype=np.uint32).reshape(height, width)

    memfile = rasterio.MemoryFile()
    grid = memfile.open(
        driver="MEM",
        height=height,
        width=width,
        count=1,
        crs=crs,
        transform=transform,
        dtype=rasterio.uint32,
        nodata=0,
    )
    grid.write(arr, 1)

    return grid


def find_grid_duplicates(
    gdf: gpd.GeoDataFrame,
    species_col: str,
    resolution: float,
    bounds: Union[list, tuple] = None,
    keep: Union[bool, str] = False,
) -> pd.Series:
    """
    Find records of the same species that are in the same cell of a
    specific grid.

    Parameters
    ----------
    gdf : GeoDataFrame
        GeoDataFrame with records.
    species_col : str
        Column name with the species name for each record.
    resolution : float
        Grid resolution.
    bounds : list or tuple
        Grid bounds (xmin, ym, xmax, ymax). If no bounds are passed, the
        bounds from gdf will be taken.
    keep : str
        Which duplicates to mark. Can be:

        - False: mark all duplicates as True.
        - 'first': mark duplicates as True except for the first occurrence.
        - 'last': mark duplicates as True except for the last occurrence.

    Returns
    -------
    pd.Series
        Boolean Series indicating whether records are spatial duplicates.

    Notes
    -----
    bounds and resolution should match gdf coordinate reference
    system.

    """
    gdf = gdf.copy()

    if not bounds:
        bounds = gdf.geometry.total_bounds
    grid = _create_id_grid(*bounds, resolution, gdf.crs.srs)
    gdf["__grid_id"] = rasterstats.point_query(
        gdf, grid.read(1), affine=grid.transform, interpolate="nearest", nodata=0
    )
    result = gdf.duplicated(subset=[species_col, "__grid_id"], keep=keep)

    # Result for records that do not have a grid ID is left empty.
    no_grid_id = gdf["__grid_id"].isna()
    result.loc[no_grid_id] = np.nan

    return result
