"""
Functions for local geographic verifications.
"""
import pathlib
from typing import Union

import fiona
import geopandas as gpd
import numpy as np
import pandas as pd
from rasterstats import point_query

from . import _helpers


def _historical(
    gdf: gpd.GeoDataFrame,
    others_path: Union[str, pathlib.Path],
    date_col: str,
    direction: str = "nearest",
    round_unmatched: bool = False,
    default_year: str = "none",
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
        year anywhere in order to extract it and match it with the records
        collection date.
    date_col : str
        Column name with the collection date.
    direction : str
        Whether to search for prior, subsequent, or closest years. Can be
         "backward", "nearest" or "forward".
    round_unmatched : bool
        Whether to round unmatched rows to the nearest year using a
        different direction than the one specified.
    default_year : str
        Default year to take for records that do not have a collection
        date or whose collection data did not match with any year. Can be
        "last" for the most recent year in the historical data, "fist" for
        the oldest year in the historical data or "none" to skip a default
        year assignation. Keep in mind that records without a collection
        date won't be validated.
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

    years = list(map(_helpers.extract_year, layers))
    historical_year = _helpers.get_nearest_year(
        gdf[date_col], years, direction=direction, round_unmatched=round_unmatched
    )
    if default_year == "last":
        historical_year = historical_year.fillna(max(years))
    elif default_year == "first":
        historical_year = historical_year.fillna(min(years))
    elif default_year == "none":
        pass
    else:
        raise ValueError("`default_year` must be either 'first', 'last' or 'none'.")

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
    predicate: str = "intersects",
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
    predicate : str
        Spatial join operation accepted by the GeoDataFrame's sjoin
        method.

    Returns
    -------
    pd.Series
        Extracted values.

    """
    if isinstance(other, str):
        other = pathlib.Path(other)

    if not isinstance(other, gpd.GeoDataFrame):
        other = gpd.read_file(other, layer=layer)

    join = gpd.sjoin(gdf, other, how="left", op=predicate)

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

    other = other.copy()

    # Ideally, one could check if the elements of `gdf` intersect any of
    # the features of `other` with the following line:
    # gdf.intersects(other.geometry.unary_union)
    # While this works, depending on the complexity of the geometries of
    # `other` and the number of elements of `gdf`, the execution can be
    # considerably slow. A workaround is to create a new column with a
    # constant value (e.g. 1) in `other` and do a spatial join. Elements
    # of `gdf` that have a value for that column intersect any of the
    # features in `other`.
    other["__dummy"] = 1
    join = gpd.sjoin(gdf, other, how="left", op="intersects")
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


def find_outliers(
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
        result.loc[mask] = _helpers.is_outlier(values, method, threshold)
        # Result for records that do not have a value is left empty. This
        # is done here instead of returning the respective nan values in
        # the is_outlier function because numpy cannot combine Boolean and
        # nan values in a single array (while pandas allows it).
        result.loc[mask & gdf[value_col].isna()] = np.nan

    return result


def find_spatial_duplicates(
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
    grid = _helpers.create_id_grid(*bounds, resolution, gdf.crs.srs)
    gdf["__grid_id"] = point_query(
        gdf, grid.read(1), affine=grid.transform, interpolate="nearest", nodata=-9999
    )
    result = gdf.duplicated(subset=[species_col, "__grid_id"], keep=keep)

    # Result for records that do not have a grid ID is left empty.
    no_grid_id = gdf["__grid_id"].isna()
    result.loc[no_grid_id] = np.nan

    return result
