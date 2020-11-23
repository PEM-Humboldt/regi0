import re

import numpy as np
import pandas as pd
import rasterio


def _create_id_grid(
    xmin: float,
    ymin: float,
    xmax: float,
    ymax: float,
    resolution: float,
    crs: str = "epsg:4326",
) -> rasterio.io.DatasetWriter:
    """

    Parameters
    ----------
    xmin
    ymin
    xmax
    ymax
    resolution
    crs

    Returns
    -------

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

    Parameters
    ----------
    string

    Returns
    -------

    Notes
    -----
    Regex expression was taken from: https://stackoverflow.com/a/49853325/7144368.
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
    direction: str = "nearest",
    round_unmatched=True
) -> pd.Series:
    """

    Parameters
    ----------
    dates
    reference_years
    direction
    round_unmatched

    Returns
    -------

    Notes
    -----
    This function is based on the answer given on:
    https://stackoverflow.com/a/64881346/7144368
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

    result.index = years.index
    nans = pd.Series(np.nan, index=dates[~has_date].index)
    result = result.append(nans)
    result = result.sort_index()

    return result
