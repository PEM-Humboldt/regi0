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
    bounds
    resolution
    crs

    Returns
    -------

    """
    nrows = int((ymax - ymin) // resolution)
    ncols = int((xmax - xmin) // resolution)

    arr = np.arange(nrows * ncols, dtype=np.uint32).reshape(nrows, ncols)

    memfile = rasterio.MemoryFile()
    transform = rasterio.transform.from_bounds(xmin, ymin, xmax, ymax, ncols, nrows)
    grid = memfile.open(
        driver="MEM",
        height=ncols,
        width=nrows,
        count=1,
        crs=crs,
        transform=transform,
        dtype=rasterio.uint32,
    )
    grid.write(arr, 1)

    return grid


def _get_most_recent_year(
    dates: pd.Series, unique_years: list, round_unmatched=False
) -> pd.Series:
    """

    Parameters
    ----------
    dates
    unique_years
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
    result = pd.merge_asof(years, dummy_df, on=years.name)["__year"]

    if round_unmatched:
        result[result.isna()] = min(unique_years)

    result.index = years.index
    result = result.sort_index()

    return result.astype(int)
