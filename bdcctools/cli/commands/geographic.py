"""
$ bdcctools geographic
"""

import click
from bdcctools.geographic.local import (
    get_layer_field_historical,
    intersects_layer_historical,
    find_outliers,
    find_spatial_duplicates
)
from bdcctools.io import read_geographic_table
from bdcctools.utils import verify
from rasterstats import point_query

from ..options import geographic as opts
from ..util.geoconfig import CONFIG
from ..util.logger import LOGGER


@click.command(
    short_help="Performs a complete geographic verification on a set of records."
)
@click.argument("src", type=click.Path(exists=True))
@click.argument("dst", type=click.Path(exists=False))
@opts.crs
@opts.lon_col
@opts.lat_col
@opts.date_col
@opts.admin0_col
@opts.admin1_col
@opts.admin2_col
@opts.species_col
@opts.admin0_path
@opts.admin1_path
@opts.admin2_path
@opts.urban_path
@opts.dem_path
@opts.admin0_match
@opts.admin1_match
@opts.admin2_match
@opts.default_year
@opts.gridres
@opts.mark
@opts.drop
@opts.quiet
def geographic(
    src,
    dst,
    crs,
    lon_col,
    lat_col,
    date_col,
    admin0_col,
    admin1_col,
    admin2_col,
    species_col,
    admin0_path,
    admin1_path,
    admin2_path,
    urban_path,
    dem_path,
    admin0_match,
    admin1_match,
    admin2_match,
    default_year,
    gridres,
    mark,
    drop,
    quiet
):

    if not quiet:
        LOGGER.info(f"Reading records from {src}.")
    records = read_geographic_table(src, lon_col, lat_col, crs=crs)

    # 1. Removal of records with incomplete or missing coordinates.
    if not quiet:
        LOGGER.info("Removing missing or incomplete coordinates.")
    records = records.dropna(how="any", subset=[lon_col, lat_col])

    # 2. Administrative boundaries verification.
    if not quiet:
        LOGGER.info("Validating administrative boundaries.")
    admin_paths = [admin0_path, admin1_path, admin2_path]
    admin_fields = [admin0_match, admin1_match, admin2_match]
    admin_cols = [admin0_col, admin1_col, admin2_col]
    keys = ["admin0", "admin1", "admin2"]
    for path, field, col, key in zip(admin_paths, admin_fields, admin_cols, keys):
        expected, source = get_layer_field_historical(
            records,
            path,
            date_col,
            field,
            direction="backward",
            round_unmatched=True,
            default_year=default_year,
            return_source=True
        )
        flag_name = CONFIG.get("flagnames", key)
        suggested_name = CONFIG.get("suggestednames", key)
        records = verify(
            records, col, expected, flag_name, True, suggested_name, drop=drop
        )
        records[CONFIG.get("sourcenames", key)] = source

    # 3. Urban limits verification.
    if not quiet:
        LOGGER.info("Identifying records in urban areas.")
    intersects, source = intersects_layer_historical(
        records,
        urban_path,
        date_col,
        direction="nearest",
        default_year=default_year,
        return_source=True,
    )
    records[CONFIG.get("flagnames", "urban")] = intersects
    records[CONFIG.get("sourcenames", "urban")] = source
    if drop:
        records = records[~records[CONFIG.get("flagnames", "urban")]]

    # 4. Elevation consistency
    if not quiet:
        LOGGER.info("Extracting elevation values and identifying outliers.")
    values = point_query(records.geometry, dem_path, interpolate="nearest")
    records[CONFIG.get("valuenames", "elevation")] = values
    is_outlier = find_outliers(
        records, species_col, CONFIG.get("valuenames", "elevation"), method="iqr"
    )
    records[CONFIG.get("flagnames", "elevation")] = is_outlier
    if drop:
        records = records[~records[CONFIG.get("flagnames", "elevation")]]

    # 5. Spatial duplicates
    if not quiet:
        LOGGER.info("Identifying spatial duplicates.")
    is_duplicate = find_spatial_duplicates(records, species_col, gridres, mark=mark)
    records[CONFIG.get("flagnames", "spatialduplicate")] = is_duplicate
    if drop:
        records = records[~records[CONFIG.get("flagnames", "spatialduplicate")]]

    if not quiet:
        LOGGER.info(f"Saving results to {dst}.")
    records.drop(columns="geometry").to_csv(dst, index=False)
