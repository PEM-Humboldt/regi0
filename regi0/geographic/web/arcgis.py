"""
Wrappers for ArcGIS REST API calls.

API documentation can be found at: https://developers.arcgis.com/rest
"""
import json
from typing import Union

import geopandas as gpd
import pandas as pd
import requests

from ..local import get_layer_field as _get_layer_field
from ..local import intersects_layer as _intersects_layer


def _query(
    url: str,
    where: str = "1=1",
    geometry: Union[str, dict] = None,
    geometry_type: str = "esriGeometryPoint",
    in_sr: int = None,
    spatial_rel: str = "esriSpatialRelIntersects",
    out_fields: Union[list, str] = None,
    return_geometry: bool = True,
    out_sr: int = None,
    f="JSON",
) -> requests.Response:
    """
    Queries a Feature Service layer.

    Parameters
    ----------
    url : str.
        Feature Service layer. Must end with /query.
    where : str
        A WHERE clause for the query filter
    geometry : str or dict
        The geometry to apply as the spatial filter. The structure of the
        geometry is the same as the structure of the JSON geometry objects
        returned by the ArcGIS REST API. In addition to the JSON
        structures, you can specify the geometry of envelopes and points
        with a simple comma-separated syntax.
    geometry_type : str
        The type of geometry specified by the geometry parameter. The
        geometry type can be an envelope, a point, a line, or a polygon.
    in_sr : int
        The spatial reference of the input geometry. The spatial
        reference can be specified as either a well-known ID or as a
        spatial reference JSON object. If the inSR is not specified, the
        geometry is assumed to be in the spatial reference of the layer.
    spatial_rel : str
        The spatial relationship to be applied to the input geometry while
        performing the query. The supported spatial relationships include
        intersects, contains, envelope intersects, within, and so on.
    out_fields : list or str
        The list of fields to be included in the returned result set.
        This list is a comma-delimited list of field names. You can also
        specify the wildcard "*" as the value of this parameter. In this
        case, the query results include all the field values.
    return_geometry : bool
        If True, the result includes the geometry associated with each
        feature returned.
    out_sr : int
        The spatial reference of the returned geometry. The spatial
        reference can be specified as either a well-known ID or as a
        spatial reference JSON object. If outSR is not specified, the
        geometry is returned in the spatial reference of the map.
    f : str
        The response format.

    Returns
    -------
    Response
        Feature Service layer query response.

    """
    if out_fields is None:
        out_fields = []
    if isinstance(out_fields, str):
        out_fields = [out_fields]

    params = {
        "where": where,
        "geometry": json.dumps(geometry),
        "geometryType": geometry_type,
        "inSR": in_sr,
        "spatialRel": spatial_rel,
        "outFields": ",".join(out_fields),
        "returnGeometry": return_geometry,
        "outSR": out_sr,
        "f": f,
    }

    try:
        response = requests.post(url, data=params)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise Exception(f"Error calling {url}. {err}")
    if "error" in response.json():
        msg = response.json()["error"].get("message")
        raise Exception(f"Error calling {url}. {msg}")

    return response


def get_feature_layer_field(
    gdf: gpd.GeoDataFrame, url: str, field: Union[list, str], where: str = "1=1"
) -> pd.Series:
    """
    Gets the corresponding values of one or multiple fields in a Feature
    Service layer.

    Parameters
    ----------
    gdf : GeoDataFrame
        GeoDataFrame with records.
    url : str.
        Feature Service layer. Must end with /query.
    field : list or str
        Field(s) to retrieve from the layer.
    where : str
        A WHERE clause for the query filter

    Returns
    -------
    Series
        Extracted values from the Feature Service layer.

    """
    response = _query(
        url,
        where=where,
        geometry={
            "points": list(zip(gdf.geometry.x, gdf.geometry.y)),
            "spatialReference": {"wkid": gdf.crs.to_epsg()},
        },
        geometry_type="esriGeometryMultiPoint",
        spatial_rel="esriSpatialRelIntersects",
        out_fields=field,
        return_geometry=True,
        out_sr=gdf.crs.to_epsg(),
        f="GeoJSON",
    )
    other = gpd.GeoDataFrame.from_features(response.json()["features"], crs=gdf.crs)

    return _get_layer_field(gdf, other, field=field)


def intersects_feature_layer(
    gdf: gpd.GeoDataFrame, url: str, where: str = "1=1"
) -> pd.Series:
    """
    Checks whether records from gdf intersect any feature of the Feature
    Service layer.

    Parameters
    ----------
    gdf : GeoDataFrame
        GeoDataFrame with records.
    url : str.
        URL of the Feature Service layer. Must end with /query.
    where : str
        A WHERE clause for the query filter

    Returns
    -------
    Series
        Boolean Series indicating whether each record intersects any
        feature of the Feature Service layer.

    """
    response = _query(
        url,
        where=where,
        geometry={
            "points": list(zip(gdf.geometry.x, gdf.geometry.y)),
            "spatialReference": {"wkid": gdf.crs.to_epsg()},
        },
        geometry_type="esriGeometryMultiPoint",
        spatial_rel="esriSpatialRelIntersects",
        out_fields=None,
        return_geometry=True,
        out_sr=gdf.crs.to_epsg(),
        f="GeoJSON",
    )
    other = gpd.GeoDataFrame.from_features(response.json()["features"], crs=gdf.crs)

    return _intersects_layer(gdf, other)
