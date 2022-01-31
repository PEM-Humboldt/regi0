"""
Functions to extract information from local data.
"""
import pathlib
import re
from typing import Union

import fiona
import geopandas as gpd
import numpy as np
import pandas as pd


def _extract_year(x: Union[str, pathlib.Path]) -> int:
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


def _get_nearest_year(
    dates: pd.Series,
    reference_years: Union[list, tuple],
    direction: str,
    default_year: str = None,
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
        be

        - 'backward'
        - 'nearest'
        - 'forward'
        For more information go to:
        https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.merge_asof.html
    default_year : str
        Default year to take for records that do not have a collection
        date or whose collection data did not match with any year. Can be:

        - 'last': takes the earliest year in the historical data
        - 'fist': takes the latest year in the historical data
        - 'none': skips a default year assignation. Keep in mind that
        records without a collection date won't be validated.

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

    if default_year:
        if default_year == "first":
            result.loc[result.isna()] = min(reference_years)
        elif default_year == "last":
            result.loc[result.isna()] = max(reference_years)
        else:
            raise ValueError("`default_year` must be either 'first', 'last' or 'none'.")

    return result


def _historical(
    gdf: gpd.GeoDataFrame,
    others_path: Union[str, pathlib.Path],
    date_col: str,
    direction: str = "nearest",
    default_year: str = None,
    op: str = "intersection",
    field: str = None,
    return_source: bool = False,
) -> Union[pd.Series, tuple]:
    """
    Checks whether records in gdf intersect with features in other or if
    column values from gdf match with other column values after a spatial
    join for historical data. Supposing one has two or more layers for
    different years in time, this function will match each record with
    of those layers depending on the date of collection. Then, for each
    layer, it will compare the respective records by executing one of the
    check_intersect or check_match functions.

    Parameters
    ----------
    gdf : GeoDataFrame
        GeoDataFrame with records.
    others_path : str or Path
        Folder with shapefiles or GeoPackage file with historical data.
        Shapefile names of GeoPackage layer names must have a four-digit
        year anywhere in order to extract it and match it with the
        records' collection date.
    date_col : str
        Column name with the collection date.
    direction : str
        Whether to search for prior, subsequent, or closest years. Can be
         "backward", "nearest" or "forward".
    default_year : str
        Default year to take for records that do not have a collection
        date or whose collection date did not match with any year. Can be:

        - 'first': takes the earliest year in the historical data.
        - 'last': takes the latest year in the historical data.
        - None: skips a default year assignation. Keep in mind that
        records without a collection date won't be validated.
    op : str
        Operation to execute. Can be "intersection" to execute
        check_intersection or "match" to execute check_match.
    field : str
        Field to get from layers when `op` is "match".
    return_source : bool
        Whether to return a column with layer source.

    Returns
    -------
    result : pd.Series
        Extracted values.
    source : pd.Series
        Corresponding source. Only provided if return_source is True.

    """
    if not isinstance(others_path, pathlib.Path):
        others_path = pathlib.Path(others_path)

    if others_path.is_dir():
        layers = list(others_path.glob("*.shp"))
        if not layers:
            raise Exception("`others_path` must contain shapefiles.")
        input_type = "shp"
    else:
        if others_path.suffix == ".gpkg":
            layers = fiona.listlayers(others_path)
            input_type = "gpkg"
        else:
            raise ValueError("`others_path` must be a GeoPackage file.")

    years = list(map(_extract_year, layers))
    historical_year = _get_nearest_year(
        gdf[date_col], years, direction=direction, default_year=default_year
    )

    result = pd.Series(index=gdf.index, dtype="object")
    if return_source:
        source = pd.Series(index=gdf.index, dtype="object")

    for year in historical_year.dropna().unique():
        layer = layers[years.index(year)]
        if input_type == "shp":
            other = gpd.read_file(layer)
            year_source = layer.stem
        elif input_type == "gpkg":
            other = gpd.read_file(others_path, layer=layer)
            year_source = layer

        mask = historical_year == year
        year_gdf = gdf[mask]
        if op == "intersection":
            year_result = intersects_layer(year_gdf, other)
        elif op == "match":
            year_result = get_layer_field(year_gdf, other, field)
        else:
            raise ValueError("`op` must be either 'intersection' or 'match'.")

        result.loc[mask] = year_result
        if return_source:
            source.loc[mask] = year_source

    if return_source:
        return result, source
    else:
        return result


def get_layer_field(
    gdf: gpd.GeoDataFrame,
    other: Union[str, pathlib.Path, gpd.GeoDataFrame],
    field: str,
    layer: str = None,
) -> pd.Series:
    """
    Gets the corresponding values of a specific field by performing a
    spatial join between a GeoDataFrame with records and a GeoDataFrame
    representing a vector layer.

    Parameters
    ----------
    gdf : GeoDataFrame
        GeoDataFrame with records.
    other : GeoDataFrame
        GeoDataFrame with the target layer.
    field : str
        Name of the field to extract values from.
    layer : str
        Layer name. Only has effect when other is a geopackage file.

    Returns
    -------
    pd.Series
        Extracted values.

    """
    if isinstance(other, str):
        other = pathlib.Path(other)

    if not isinstance(other, gpd.GeoDataFrame):
        other = gpd.read_file(other, layer=layer)

    join = gpd.sjoin(gdf, other, how="left", predicate="intersects")

    return join[field]


def get_layer_field_historical(
    gdf: gpd.GeoDataFrame, others_path: str, date_col: str, field: str, **kwargs
) -> Union[pd.Series, tuple]:
    """
    Gets the corresponding values of a specific field by performing a
    spatial join between a GeoDataFrame with records and multiple
    historical vector layers.

    Parameters
    ----------
    gdf : GeoDataFrame
        GeoDataFrame with records.
    others_path : str
        Path of a .gpkg file or a folder containing .shp files with the
        historical layers.
    date_col : str
        Name of the date column in `gdf` to match historical layers with.
    field : str
        Name of the field to extract values from. Must exist in all the
        historical layers.
    **kwargs
        Keyword arguments accepted by the _historical function.

    Returns
    -------
    values : pd.Series
        Extracted values.
    source : pd.Series
        Corresponding source. Only provided if return_source is True.

    """
    return _historical(gdf, others_path, date_col, op="match", field=field, **kwargs)


def intersects_layer(
    gdf: gpd.GeoDataFrame,
    other: Union[str, pathlib.Path, gpd.GeoDataFrame],
    layer: str = None,
) -> pd.Series:
    """
    Checks whether records from `gdf` intersect any feature of `other`.

    Parameters
    ----------
    gdf : GeoDataFrame
        GeoDataFrame with records.
    layer : str
        Layer name. Only has effect when other is a geopackage file.
    other : str, Path or GeoDataFrame
        GeoDataFrame with features to intersect records with.

    Returns
    -------
    pd.Series
        Boolean Series indicating whether each record intersects other.

    """
    if isinstance(other, str):
        other = pathlib.Path(other)

    if not isinstance(other, gpd.GeoDataFrame):
        other = gpd.read_file(other, layer=layer)

    # Ideally, one could check if the elements of `gdf` intersect any of
    # the features of `other` with the following line:
    # gdf.intersects(other.geometry.unary_union)
    # While this works, depending on the complexity of the geometries of
    # `other` and the number of elements of `gdf`, the execution can be
    # considerably slow. A workaround is to create a new column with a
    # constant value (e.g. 1) in `other` and do a spatial join. Elements
    # of `gdf` that have a value for that column intersect any of the
    # features in `other`.
    other = other.copy()
    other["__dummy"] = 1
    join = gpd.sjoin(gdf, other, how="left", predicate="intersects")
    intersects = join["__dummy"].notna()
    intersects.name = None

    intersects.loc[~gdf.is_valid] = pd.NA

    return intersects


def intersects_layer_historical(
    gdf: gpd.GeoDataFrame, others_path: str, date_col: str, **kwargs
) -> Union[pd.Series, tuple]:
    """
    Checks whether records from `gdf` intersect any feature of their
    corresponding historical vector layer.

    Parameters
    ----------
    gdf : GeoDataFrame
        GeoDataFrame with records.
    others_path : str
        Path of a .gpkg file or a folder containing .shp files with the
        historical layers.
    date_col : str
        Name of the date column in `gdf` to match historical layers with.
    kwargs
        Keyword arguments accepted by the _historical function.

    Returns
    -------
    intersects
        Boolean Series indicating whether each record intersects other.
    source
        Corresponding source. Only provided if return_source is True.
    """
    return _historical(gdf, others_path, date_col, op="intersection", **kwargs)
