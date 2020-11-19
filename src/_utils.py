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


def _get_nearest_year(
    dates: pd.Series,
    unique_years: list,
    direction: str = "nearest",
    round_unmatched=False
) -> pd.Series:
    """

    Parameters
    ----------
    dates
    unique_years
    direction
    round_unmatched

    Returns
    -------

    Notes
    -----
    This function is based on the answer given on:
    https://stackoverflow.com/a/64881346/7144368
    """

    years = pd.to_datetime(dates).dt.year
    years = years.sort_values()

    dummy_df = pd.DataFrame({years.name: unique_years, "__year": unique_years})
    result = pd.merge_asof(years, dummy_df, on=years.name, direction=direction)

    if round_unmatched:
        if direction == "backward":
            result[result.isna()] = min(unique_years)
        elif direction == "forward":
            result[result.isna()] = max(unique_years)

    result.index = years.index
    result = result.sort_index()

    return result["__year"].astype(int)
