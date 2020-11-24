import re

import numpy as np
import pandas as pd
import rasterio
from scipy import stats


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
    xmin:       Upper-left corner x coordinate.
    ymin:       Lower-right corner y coordinate.
    xmax:       Lower-left corner x coordinate.
    ymax:       Upper-left corner y coordinate.
    resolution: Pixel resolution.
    crs:        Coordinate Reference System. Must be in the form
                epsg:code.

    Returns
    -------
    In-memory raster with unique IDs.

    Notes
    -----
    Coordinates and resolution should agree with the reference system
    passed in crs.
    """
    height = np.ceil((ymax - ymin) / resolution).astype(np.int)
    width = np.ceil((xmax - xmin) / resolution).astype(np.int)
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


def _extract_year(string: str) -> int:
    """
    Extracts a four-digit valid year (1900-2099) from a string. If there
    are multiple four-digit valid years on the string, the first
    ocurrence is returned.

    Parameters
    ----------
    string: String to extract the year from.

    Returns
    -------
    Four-digit integer representing the year.

    Notes
    -----
    Regex expression was taken from:
    https://stackoverflow.com/a/49853325/7144368

    Examples
    --------
    >>> _extract_year("admin2_2014.shp")
    2014
    >>> _extract_year("v0001popc2017")
    2017
    >>> _extract_year("human_footprint_1970_1990.tif")
    1970
    >>> _extract_year("ne_10m_admin_o_countries.shp")
    Exception: The string does not have any valid year.
    """
    expr = r"(?:19|20)\d{2}"
    matches = re.findall(expr, string)
    if matches:
        year = matches[0]
    else:
        raise Exception("The string does not have any valid year.")

    return int(year)


def _get_nearest_year(
    dates: pd.Series,
    reference_years: list,
    direction: str = "backward",
    round_unmatched=True,
) -> pd.Series:
    """
    Get the nearest year for each row in a Series from a given list of
    years.

    Parameters
    ----------
    dates:           Series with datetime-like objects.
    reference_years: List of years to round each row to.
    direction:       Whether to search for prior, subsequent, or closest
                     matches. Can be "backward", "nearest" or "forward".
                     For more information go to:
                     https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.merge_asof.html
    round_unmatched: Whether to round unmatched rows to the nearest year
                     using a different direction than the one specified.

    Returns
    -------
    Series with the nearest years.

    Notes
    -----
    This function is based on the answer given on:
    https://stackoverflow.com/a/64881346/7144368

    Examples
    --------
    >>> dates = pd.Series(
    ...     ["17/08/1945", np.nan, "21/09/2011", "01/01/1984", "17/04/2009"],
    ...     name="date"
    ... )
    >>> dates
    0    17/08/1945
    1           NaN
    2    21/09/2011
    3    01/01/1984
    4    17/04/2009
    Name: date, dtype: object
    >>> reference_years = [1963, 1980, 2010, 2014]
    >>> _get_nearest_year(dates, reference_years)
    0    1963.0
    1       NaN
    2    2010.0
    3    1980.0
    4    1980.0
    dtype: float64
    >>> _get_nearest_year(dates, reference_years, round_unmatched=False)
    0       NaN
    1       NaN
    2    2010.0
    3    1980.0
    4    1980.0
    dtype: float64
    >>> _get_nearest_year(dates, reference_years, direction="nearest")
    0    1963.0
    1       NaN
    2    2010.0
    3    1980.0
    4    2010.0
    dtype: float64
    """
    reference_years = sorted(reference_years)
    has_date = dates.notna()
    years = pd.to_datetime(dates[has_date]).dt.year
    years = years.sort_values()

    dummy_df = pd.DataFrame({years.name: reference_years, "__year": reference_years})
    result = pd.merge_asof(years, dummy_df, on=years.name, direction=direction)["__year"]

    if round_unmatched:
        if direction == "backward":
            result[result.isna()] = min(reference_years)
        elif direction == "forward":
            result[result.isna()] = max(reference_years)

    # merge_asof result has a new index that has to be changed for the original. Also,
    # merge_asof does not work with NaN values. All dates that are NaNs are discarded in
    # the previous steps and then are added as NaNs to the result here.
    result.index = years.index
    nans = pd.Series(np.nan, index=dates[~has_date].index)
    result = result.append(nans)
    result = result.sort_index()

    return result


def _is_outlier(
    values: np.ndarray, method: str = "std", threshold: float = 3.0
) -> np.ndarray:
    """
    Classifies outliers in an array of values.

    Parameters
    ----------
    values:     1D NumPy array of values.
    method:     Method to classify outliers. Can be "std", "iqr" or
                "zscore".
    threshold:  For the "std" method is the value to multiply the
                standard deviation with. For the "zscore" method, it is
                the lower limit (negative) and the upper limit (positive)
                to compare Z Scores to.

    Returns
    -------
    Boolean NumPy array.

    Examples
    --------
    >>> values = np.array([52, 56, 53, 57, 51, 59, 1, 99])
    >>> _is_outlier(values)
    array([False, False, False, False, False, False,  True, False])
    >>> _is_outlier(values, method="iqr")
    array([False, False, False, False, False, False,  True,  True])
    >>> _is_outlier(values, method="zscore")
    array([False, False, False, False, False, False,  True, False])
    """
    if method == "std":
        std = np.nanstd(values)
        mean = np.nanmean(values)
        lower_limit = mean - (threshold * std)
        upper_limit = mean + (threshold * std)

    elif method == "iqr":
        iqr = stats.iqr(values, nan_policy="omit")
        q1 = np.nanpercentile(values, 25)
        q3 = np.nanpercentile(values, 75)
        lower_limit = q1 - (1.5 * iqr)
        upper_limit = q3 + (1.5 * iqr)

    elif method == "zscore":
        values = stats.zscore(values, nan_policy="omit")
        lower_limit = -threshold
        upper_limit = threshold

    else:
        raise ValueError("`method` must be one of 'std', 'iqr', 'zscore'.")

    return (values < lower_limit) | (values > upper_limit)
