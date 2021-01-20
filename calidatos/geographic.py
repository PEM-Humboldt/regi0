"""
Functions for geographic verifications.
"""

import glob
import os
from typing import Union

import fiona
import geopandas as gpd
import pandas as pd
from rasterstats import point_query

from calidatos.util import get_nearest_year, extract_year, create_id_grid, is_outlier


def check_historical(
    gdf: gpd.GeoDataFrame,
    others_path: str,
    date_col: str,
    flag_name: str,
    direction: str = "nearest",
    round_unmatched: bool = False,
    default_year: str = "none",
    op: str = "intersection",
    left_col: str = None,
    right_col: str = None,
    suggested_name: str = None,
    add_source: bool = False,
    source_name: str = None,
    drop: bool = False,
) -> gpd.GeoDataFrame:
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
    gdf:             GeoDataframe with records.
    others_path:     Folder with shapefiles or GeoPackage file with
                     historical data. Shapefile names of GeoPackage layer
                     names must have a four-digit year anywhere in order to
                     extract it and match it with the records collection
                     date.
    date_col:        Column name with the collection date.
    flag_name:       Column name for the flag (whether records intersect the
                     features or whether values match depending on op).
    direction:       Whether to search for prior, subsequent, or closest
                     years. Can be "backward", "nearest" or "forward".
    round_unmatched: Whether to round unmatched rows to the nearest year
                     using a different direction than the one specified.
    default_year:    Default year to take for records that do not have
                     a collection date or whose collection data did not
                     match with any year. Can be "last" for the most recent
                     year in the historical data, "fist" for the oldest
                     year in the historical data or "none" to skip a default
                     year assignation. Keep in mind that records without
                     a collection date won't be validated.
    op:              Operation to execute. Can be "intersection" to execute
                     check_intersection or "match" to execute check_match.
    left_col:        Column name in gdf with the values to match.
    right_col:       Column name in other with the values to match. Will
                     only be used if op is "match".
    flag_name:       Column name for the flag (whether values match). Will
                     only be used if op is "match".
    suggested_name:  Column name for the suggestion if values do not match.
                     Will only be used if op is "match".
    add_source:      Whether to add a column with the source layer of
                     comparison for each record.
    source_name:     Column for the source name.
    drop:            Whether to drop records that do not intersect or
                     match.

    Returns
    -------
    Original GeoDataFrame (gdf) with extra columns.
    """
    gdf = gdf.copy()

    if os.path.isdir(others_path):
        layers = glob.glob(os.path.join(others_path, "*.shp"))
        if not layers:
            raise Exception("`others_path` must contain shapefiles.")
        input_type = "shp"
    else:
        if others_path.endswith(".gpkg"):
            layers = fiona.listlayers(others_path)
            input_type = "gpkg"
        else:
            raise ValueError("`others_path` must be a GeoPackage.")

    years = list(map(extract_year, layers))
    gdf["__year"] = get_nearest_year(
        gdf[date_col], years, direction=direction, round_unmatched=round_unmatched
    )
    if default_year == "last":
        gdf["__year"] = gdf["__year"].fillna(max(years))
    elif default_year == "first":
        gdf["__year"] = gdf["__year"].fillna(min(years))
    elif default_year == "none":
        pass
    else:
        raise ValueError("`default_year` must be either 'first', 'last' or 'none'.")

    for year in gdf["__year"].dropna().unique():

        layer = layers[years.index(year)]
        if input_type == "shp":
            other = gpd.read_file(layer)
            source = os.path.splitext(os.path.basename(layer))[0]
        elif input_type == "gpkg":
            other = gpd.read_file(others_path, layer=layer)
            source = layer

        year_gdf = gdf[gdf["__year"] == year]
        if op == "intersection":
            year_gdf = check_intersection(year_gdf, other, flag_name, drop)
        elif op == "match":
            year_gdf = check_match(
                year_gdf, other, left_col, right_col, flag_name, suggested_name, drop
            )
        else:
            raise ValueError("`op` must be either 'intersection' or 'match'.")
        if add_source:
            year_gdf[source_name] = source
        gdf.loc[year_gdf.index, year_gdf.columns] = year_gdf

    gdf.loc[gdf["__year"].isna(), flag_name] = pd.NA

    gdf = gdf.drop(columns=["__year"])

    return gdf


def check_intersection(
    gdf: gpd.GeoDataFrame, other: gpd.GeoDataFrame, flag_name: str, drop: bool = False
) -> gpd.GeoDataFrame:
    """
    Checks whether records in gdf intersect with features in other.

    Parameters
    ----------
    gdf:       GeoDataFrame with the records.
    other:     GeoDataframe with features of interest.
    flag_name: Column name for the flag (whether records intersect the
               features).
    drop:      Whether to drop records that do not intersect the features.

    Returns
    -------
    Original GeoDataFrame (gdf) with an extra column.

    """
    # Ideally, one could check if the records intersect any of the
    # features with the following line:
    # gdf.intersects(other.geometry.unary_union)
    # While this works, depending on the complexity of the geometries of
    # other and the number of records, the execution can be considerably
    # slow. A workaround is to create a new column with a constant value
    # (e.g. 1) in other and do a spatial join. Records that have a value
    # for that column intersect any of the features. On the contrary,
    # records that do not intersect any of the features will not have a
    # value.
    gdf = gdf.copy()

    other["__dummy"] = 1
    gdf = gpd.sjoin(gdf, other[["__dummy", "geometry"]], how="left", op="intersects")
    gdf[flag_name] = gdf["__dummy"].notna()

    # GeoPandas adds an index_right automatically when doing a left spatial join.
    gdf = gdf.drop(columns=["index_right", "__dummy"])

    if drop:
        gdf = gdf[gdf[flag_name]]

    return gdf


def check_match(
    gdf: gpd.GeoDataFrame,
    other: gpd.GeoDataFrame,
    left_col: str,
    right_col: str,
    flag_name: str,
    suggested_name: str,
    drop: bool = False,
) -> gpd.GeoDataFrame:
    """
    Checks if column values from gdf match with other column values after
    a spatial join.

    Parameters
    ----------
    gdf:            GeoDataFrame with the records.
    other:          GeoDataframe with features of interest.
    left_col:       Column name in gdf with the values to match.
    right_col:      Column name in other with the values to match.
    flag_name:      Column name for the flag (whether values match).
    suggested_name: Column name for the suggestion if values do not match.
    drop:           Whether to drop records that do not match.

    Returns
    -------
    Original GeoDataFrame (gdf) with two extra columns.
    """
    gdf = gdf.copy()

    gdf = gpd.sjoin(gdf, other[[right_col, "geometry"]], how="left", op="intersects")

    is_valid = gdf[left_col] == gdf[right_col]
    gdf[flag_name] = is_valid
    gdf.loc[~is_valid, suggested_name] = gdf.loc[~is_valid, right_col]

    # Flag for records that did not get a match is left empty because one cannot
    # be sure the flag is positive or negative.
    gdf.loc[gdf[right_col].isna(), flag_name] = pd.NA

    # GeoPandas adds an index_right automatically when doing a left spatial join.
    gdf = gdf.drop(columns=["index_right", right_col])

    if drop:
        gdf = gdf[is_valid]

    return gdf


def find_outliers(
    gdf: gpd.GeoDataFrame,
    species_col: str,
    value_col: str,
    flag_name: str,
    method: str = "std",
    threshold: float = 2.0,
    drop: bool = False,
) -> gpd.GeoDataFrame:
    """
    Finds outlier records based on values of a specific column.

    Parameters
    ----------
    gdf:         GeoDataframe with records.
    species_col: Column name with the species name for each record.
    value_col:   Column name with values to find outliers from.
    flag_name:   Column name for the flag (whether records are outliers).
    method:      Method to find outliers. Can be "std" for Standard
                 Deviation, "iqr" for Interquartile Range or "zscore" for
                 Z Score. For more details on the implementations, take
                 a look at the code of the is_outlier function.
    threshold:   For the "std" method is the value to multiply the
                 standard deviation with. For the "zscore" method, it is
                 the lower limit (negative) and the upper limit (positive)
                 to compare Z Scores to.
    drop:        Whether to drop outlier records.

    Returns
    -------
    Original GeoDataFrame (gdf) with an extra column.
    """
    gdf = gdf.copy()
    for species in gdf[species_col].unique():
        mask = gdf[species_col] == species
        values = gdf.loc[mask, value_col]
        gdf.loc[mask, flag_name] = is_outlier(values, method, threshold)

        # Flag for records that do not have a value is left empty. This is
        # done here instead of returning the respective nan values in the
        # is_outlier function because numpy cannot combine Boolean and
        # nan values in a single array.
        gdf.loc[mask & gdf[value_col].isna(), flag_name] = pd.NA

    if drop:
        gdf = gdf[~gdf[flag_name]]

    return gdf


def find_spatial_duplicates(
    gdf: gpd.GeoDataFrame,
    species_col: str,
    flag_name: str,
    resolution: float,
    bounds: Union[list, tuple] = None,
    mark: str = "all",
    drop: bool = False
) -> gpd.GeoDataFrame:
    """
    Find records of the same species that are in the same cell of a
    specific grid.

    Parameters
    ----------
    gdf:         GeoDataframe with records.
    species_col: Column name with the species name for each record.
    flag_name:   Column name for the flag (whether records are spatial
                 duplicates).
    resolution:  Grid resolution.
    bounds:      Grid bounds (xmin, ym, xmax, ymax). If no bounds are
                 passed, the bounds from gdf will be taken.
    mark:        What duplicates to mark. Can be "head", to mark all
                 bur the last, "tail" to mark all but the first, or
                 "all".
    drop:        Whether to drop records that are spatial duplicates.

    Returns
    -------
    Original GeoDataFrame (gdf) with an extra column.

    Notes
    -----
    bounds and resolution should match gdf coordinate reference system.
    """
    gdf = gdf.copy()

    if not bounds:
        bounds = gdf.geometry.total_bounds

    grid = create_id_grid(*bounds, resolution, gdf.crs.srs)
    ids = point_query(
        gdf, grid.read(1), affine=grid.transform, interpolate="nearest", nodata=-9999
    )
    gdf["__grid_id"] = ids

    subset = [species_col, "__grid_id"]
    if mark == "all":
        keep = False
    elif mark == "head":
        keep = "last"
    elif mark == "tail":
        keep = "first"
    else:
        raise ValueError("Mark must be one of 'head', 'tail' or 'all'.")
    gdf[flag_name] = gdf.duplicated(subset, keep=keep)

    # Flag for records that do not have a grid ID is left empty.
    no_grid_id = gdf["__grid_id"].isna()
    gdf.loc[no_grid_id, flag_name] = pd.NA

    if drop:
        gdf = gdf[~gdf[flag_name]]

    gdf = gdf.drop(columns=["__grid_id"])

    return gdf


def read_records(
    fn: str,
    lon_col: str,
    lat_col: str,
    drop_empty_coords=False,
    crs: str = "epsg:4326",
) -> gpd.GeoDataFrame:
    """
    Converts tabular data (CSV or XLSX) to a GeoDataFrame.

    Parameters
    ----------
    fn:                 Filename with extension. Can be a relative or
                        absolute path.
    lon_col:            Name of the longitude column.
    lat_col:            Name of the latitude column.
    drop_empty_coords:  Whether to drop rows with no values in longitude
                        or latitude.
    crs:                Coordinate reference system with the
                        corresponding EPSG code. Must be in the form
                        epsg:code.

    Returns
    -------
    GeoDataFrame with the records.
    """
    dtypes = {lon_col: float, lat_col: float}
    input_ext = os.path.splitext(fn)[1]
    if input_ext == ".csv":
        records = pd.read_csv(fn, dtype=dtypes)
    elif input_ext == ".xlsx":
        records = pd.read_excel(fn, dtype=dtypes)
    else:
        raise ValueError("Input file extension is not supported.")

    if drop_empty_coords:
        records = records.dropna(how="any", subset=[lon_col, lat_col])

    geometry = gpd.points_from_xy(records[lon_col], records[lat_col])
    records = gpd.GeoDataFrame(records, geometry=geometry, crs=crs)

    return records
