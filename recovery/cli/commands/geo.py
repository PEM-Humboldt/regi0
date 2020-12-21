"""
$ recovery geo
"""

import click
import recovery.geographic
from rasterstats import point_query

from ..options import geo as opts
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
@opts.ignore
@opts.drop
@opts.quiet
def geo(
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
    ignore,
    drop,
    quiet
):

    if not quiet:
        LOGGER.info("Reading records.")
    records = recovery.geographic.read_records(
        src, lon_col, lat_col, crs=crs, drop_empty_coords=True
    )

    if not quiet:
        LOGGER.info("Validating administrative boundaries.")
    admin_paths = [admin0_path, admin1_path, admin2_path]
    admin_cols = [admin0_col, admin1_col, admin2_col]
    admin_match_fields = [admin0_match, admin1_match, admin2_match]
    keys = ["admin0", "admin1", "admin2"]
    admin_flag_names = [CONFIG.get("flagnames", key) for key in keys]
    admin_suggested_names = [CONFIG.get("suggestednames", key) for key in keys]
    admin_source_names = [CONFIG.get("sourcenames", key) for key in keys]
    for path, col_name, match_field, flag_name, suggested_name, source_name in zip(
        admin_paths,
        admin_cols,
        admin_match_fields,
        admin_flag_names,
        admin_suggested_names,
        admin_source_names
    ):
        records = recovery.geographic.check_historical(
            records,
            path,
            date_col,
            flag_name,
            direction="backward",
            round_unmatched=True,
            default_year=default_year,
            op="match",
            left_col=col_name,
            right_col=match_field,
            suggested_name=suggested_name,
            add_source=True,
            source_name=source_name,
            drop=drop,
        )

    if not quiet:
        LOGGER.info("Identifying records in urban areas.")
    records = recovery.geographic.check_historical(
        records,
        urban_path,
        date_col,
        CONFIG.get("flagnames", "urban"),
        direction="nearest",
        default_year=default_year,
        op="intersection",
        add_source=True,
        source_name=CONFIG.get("sourcenames", "urban"),
        drop=drop
    )

    if not quiet:
        LOGGER.info("Extracting elevation values and identifying outliers.")
    records[CONFIG.get("valuenames", "elevation")] = point_query(
            records.geometry, dem_path, interpolate="nearest"
    )
    records = recovery.geographic.find_outliers(
        records,
        species_col,
        CONFIG.get("valuenames", "elevation"),
        CONFIG.get("flagnames", "elevation"),
        method="iqr",
        drop=drop
    )

    if not quiet:
        LOGGER.info("Identifying spatial duplicates.")
    records = recovery.geographic.find_spatial_duplicates(
        records,
        species_col,
        CONFIG.get("flagnames", "spatialduplicate"),
        resolution=gridres,
        drop=drop,
        mark=ignore
    )

    if not quiet:
        LOGGER.info("Saving result.")
    records.drop(columns="geometry").to_csv(dst, index=False)
