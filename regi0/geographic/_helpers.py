"""
Helper functions for the geographic module.
"""
import pathlib
import re
from typing import Union

import numpy as np
import pandas as pd
import rasterio
from scipy import stats


def create_id_grid(
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
    arr = np.arange(height * width, dtype=np.uint32).reshape(height, width)

    memfile = rasterio.MemoryFile()
    grid = memfile.open(
        driver="MEM",
        height=height,
        width=width,
        count=1,
        crs=crs,
        transform=transform,
        dtype=rasterio.uint32,
    )
    grid.write(arr, 1)

    return grid


def extract_year(x: Union[str, pathlib.Path]) -> int:
    """
    Extracts a four-digit valid year (1900-2099) from a string or path.
    If a path is given, the year will be extracted from the stem and
    all other parts of the path will be ignored. If there are multiple
    four-digit valid years on the string, the first occurrence is
    returned.

    Parameters
    ----------
    x : str
        String to extract the year from.

    Returns
    -------
    int
        Four-digit integer representing the year.

    """
    if isinstance(x, pathlib.Path):
        x = x.stem

    expr = r"(?:19|20)\d{2}"
    matches = re.findall(expr, x)
    if matches:
        year = matches[0]
    else:
        raise Exception("The string does not have any valid year.")

    return int(year)


def get_nearest_year(
    dates: pd.Series,
    reference_years: Union[list, tuple],
    direction,
) -> pd.Series:
    """
    Get the nearest year for each row in a Series from a given list of
    years.

    Parameters
    ----------
    dates : Series
        Series with datetime-like objects.
    reference_years : list or tuple
        List of years to round each row to.
    direction : str
        Whether to search for prior, subsequent, or closest matches. Can
        be "backward", "nearest" or "forward". For more information go to:
        https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.merge_asof.html

    Returns
    -------
    Series
        Series with the nearest years.

    """
    dates = dates.copy()

    if not dates.name:
        dates.name = "__date"

    reference_years = sorted(reference_years)
    has_date = dates.notna()
    years = pd.to_datetime(dates[has_date]).dt.year
    years = years.sort_values()

    dummy_df = pd.DataFrame({years.name: reference_years, "__year": reference_years})
    result = pd.merge_asof(years, dummy_df, on=years.name, direction=direction)["__year"]

    # merge_asof result has a new index that has to be changed for the original. Also,
    # merge_asof does not work with NaN values. All dates that are NaNs are discarded in
    # the previous steps and then are added as NaNs to the result here.
    result.index = years.index
    nans = pd.Series(np.nan, index=dates[~has_date].index)
    result = result.append(nans)
    result = result.sort_index()

    return result


def is_outlier(
    values: np.ndarray, method: str = "iqr", threshold: float = 2.0
) -> np.ndarray:
    """
    Classifies outliers in an array of values.

    Parameters
    ----------
    values : ndarray
        1D NumPy array of values.
    method : str
        Method to classify outliers. Can be "std", "iqr" or "zscore".
    threshold : float
        For the "std" method is the value to multiply the standard
        deviation with. For the "zscore" method, it is the lower limit
        (negative) and the upper limit (positive) to compare Z Scores to.

    Returns
    -------
    ndarray
        1D boolean NumPy array indicating whether values are outliers.

    """
    if method == "iqr":
        iqr = stats.iqr(values, nan_policy="omit")
        q1 = np.nanpercentile(values, 25)
        q3 = np.nanpercentile(values, 75)
        lower_limit = q1 - (1.5 * iqr)
        upper_limit = q3 + (1.5 * iqr)
    elif method == "std":
        std = np.nanstd(values)
        mean = np.nanmean(values)
        lower_limit = mean - (threshold * std)
        upper_limit = mean + (threshold * std)
    elif method == "zscore":
        values = stats.zscore(values, nan_policy="omit")
        lower_limit = -threshold
        upper_limit = threshold
    else:
        raise ValueError("`method` must be one of 'std', 'iqr', 'zscore'.")

    return (values < lower_limit) | (values > upper_limit)
