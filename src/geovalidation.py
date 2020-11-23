import glob
import os
from typing import Union

import fiona
import geopandas as gpd
import pandas as pd
from rasterstats import point_query

from _utils import _get_nearest_year, _extract_year, _create_id_grid, _is_outlier


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

    Parameters
    ----------
    gdf
    other
    left_col
    right_col
    flag_name
    suggested_name
    drop

    Returns
    -------

    """
    gdf = gpd.sjoin(gdf, other[[right_col, "geometry"]], how="left", op="intersects")

    is_valid = gdf[left_col] == gdf[right_col]
    gdf[flag_name] = is_valid
    gdf.loc[~is_valid, suggested_name] = gdf.loc[~is_valid, right_col]

    gdf = gdf.drop(columns=[right_col])

    if drop:
        gdf = gdf[is_valid]

    return gdf


def check_intersection(
    gdf: gpd.GeoDataFrame, other: gpd.GeoDataFrame, flag_name: str, drop: bool = False
) -> gpd.GeoDataFrame:
    """

    Parameters
    ----------
    gdf
    other
    flag_name
    drop

    Returns
    -------

    """
    other["__dummy"] = 1
    gdf = gpd.sjoin(gdf, other[["__dummy", "geometry"]], how="left", op="intersects")
    gdf[flag_name] = gdf["__dummy"].notna()

    gdf = gdf.drop(columns=["__dummy"])

    if drop:
        gdf = gdf[gdf[flag_name]]

    return gdf


def check_historical(
    gdf: gpd.GeoDataFrame,
    others_path: str,
    date_col: str,
    flag_name: str,
    direction: str = "nearest",
    default_year: str = "last",
    op: str = "intersection",
    left_col: str = None,
    right_col: str = None,
    suggested_name: str = None,
    add_source: bool = False,
    source_name: str = None,
    drop: bool = False,
) -> gpd.GeoDataFrame:
    """

    Parameters
    ----------
    gdf
    others_path
    date_col
    flag_name
    direction
    default_year
    op
    left_col
    right_col
    suggested_name
    add_source
    source_name
    drop

    Returns
    -------

    """
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

    years = list(map(_extract_year, layers))
    gdf["__year"] = _get_nearest_year(gdf[date_col], years, direction=direction)
    if default_year == "last":
        gdf["__year"] = gdf["__year"].fillna(max(years))
    elif default_year == "first":
        gdf["__year"] = gdf["__year"].fillna(min(years))
    else:
        raise ValueError("`default_year` must be either 'first' or 'last'")

    for year in gdf["__year"].unique():

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

    gdf = gdf.drop(columns=["__year"])

    return gdf


def find_outliers(
    gdf: gpd.GeoDataFrame,
    species_col: str,
    value_col: str,
    flag_name: str,
    method: str = "std",
    threshold: float = 3.0,
    drop: bool = False
) -> gpd.GeoDataFrame:
    """

    Parameters
    ----------
    gdf
    species_col
    value_col
    flag_name
    method
    threshold
    drop

    Returns
    -------

    """
    for species in gdf[species_col].unique():
        mask = gdf[species_col] == species
        values = gdf.loc[mask, value_col]
        gdf.loc[mask, flag_name] = _is_outlier(values, method, threshold)

    if drop:
        gdf = gdf[~gdf[flag_name]]

    return gdf


def find_spatial_duplicates(
    gdf: gpd.GeoDataFrame,
    species_col: str,
    flag_name: str,
    resolution: float,
    bounds: Union[list, tuple] = None,
    crs: str = "epsg:4326",
    drop: bool = False,
    keep: str = "first",
) -> gpd.GeoDataFrame:
    """

    Parameters
    ----------
    gdf
    species_col
    flag_name
    resolution
    bounds
    crs
    drop
    keep

    Returns
    -------

    """
    if not bounds:
        bounds = gdf.geometry.total_bounds

    grid = _create_id_grid(*bounds, resolution, crs)
    ids = point_query(gdf, grid.read(1), affine=grid.transform, interpolate="nearest")
    gdf["__grid_id"] = ids
    has_grid_id = gdf["__grid_id"].notna()

    subset = [species_col, "__grid_id"]
    gdf.loc[has_grid_id, flag_name] = gdf[has_grid_id].duplicated(subset, keep=False)

    if drop:
        to_keep = ~gdf.duplicated(subset, keep=keep) | gdf["__grid_id"].isna()
        gdf = gdf[to_keep]

    return gdf


def table_to_gdf(
    fn: str,
    lon_col: str,
    lat_col: str,
    drop_empty_coords=False,
    crs: str = "epsg:4326",
) -> gpd.GeoDataFrame:
    """

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
    records = gpd.GeoDataFrame(records, geometry=geometry)
    records.crs = crs

    return records
