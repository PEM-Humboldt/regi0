"""
Functions to identify geographic outliers.
"""
import geopandas as gpd
import numpy as np
import pandas as pd
from scipy import stats


def _is_iqr_outlier(values: np.ndarray) -> np.ndarray:
    """
    Classifies outliers in an array of values using an Interquartile
    Range method.

    Parameters
    ----------
    values : ndarray
        1D array of values.

    Returns
    -------
    ndarray
        1D boolean array indicating whether values are outliers.

    """
    iqr = stats.iqr(values, nan_policy="omit")
    q1 = np.nanpercentile(values, 25)
    q3 = np.nanpercentile(values, 75)

    return (values < q1 - (1.5 * iqr)) | (values > q3 + (1.5 * iqr))


def _is_std_outlier(values: np.ndarray, threshold: float = 2.0) -> np.ndarray:
    """
    Classifies outliers in an array of values using a standard deviation
    method.

    Parameters
    ----------
    values : ndarray
        1D array of values.
    threshold : float
        Value to multiply the standard deviation with

    Returns
    -------
    ndarray
        1D boolean array indicating whether values are outliers.

    """
    std = np.nanstd(values)
    mean = np.nanmean(values)

    return (values < mean - (threshold * std)) | (values > mean + (threshold * std))


def _is_zscore_outlier(values: np.ndarray, threshold: float = 2.0) -> np.ndarray:
    """
    Classifies outliers in an array of values using a Z Score method.

    Parameters
    ----------
    values : ndarray
        1D array of values.
    threshold : float
        Lower limit (negative) and the upper limit (positive) to compare
        Z Scores to.

    Returns
    -------
    ndarray
        1D boolean array indicating whether values are outliers.

    """
    values = stats.zscore(values, nan_policy="omit")

    return (values < -threshold) | (values > threshold)


def find_value_outliers(
    gdf: gpd.GeoDataFrame,
    species_col: str,
    value_col: str,
    method: str = "std",
    threshold: float = 2.0,
) -> pd.Series:
    """
    Finds outlier records based on values of a specific column.

    Parameters
    ----------
    gdf : GeoDataFrame
        GeoDataframe with records.
    species_col : str
        Column name with the species name for each record.
    value_col : str
        Column name with values to find outliers from.
    method : str
        Method to find outliers. Can be "std" for Standard Deviation,
        "iqr" for Interquartile Range or "zscore" for Z Score.
    threshold
        For the "std" method is the value to multiply the standard
        deviation with. For the "zscore" method, it is the lower limit
        (negative) and the upper limit (positive) to compare Z Scores to.

    Returns
    -------
    pd.Series
        Boolean Series indicating whether values are outliers.

    """
    result = pd.Series(index=gdf.index, dtype=bool)
    for species in gdf[species_col].unique():
        mask = gdf[species_col] == species
        values = gdf.loc[mask, value_col]
        if method == "iqr":
            is_outlier = _is_iqr_outlier(values)
        elif method == "std":
            is_outlier = _is_std_outlier(values, threshold)
        elif method == "zscore":
            is_outlier = _is_zscore_outlier(values, threshold)
        else:
            raise ValueError("method must be one of ['iqr', 'std', 'zscore']")

        result.loc[mask] = is_outlier

        # Result for records that do not have a value is left empty. This
        # is done here instead of returning the respective nan values in
        # the is_outlier function because numpy cannot combine Boolean and
        # nan values in a single array (while pandas allows it).
        result.loc[mask & gdf[value_col].isna()] = np.nan

    return result
