"""
$ recovery geo
"""

import click
import recovery.geographic
from rasterstats import point_query

from ..options import common as common_opts
from ..options import geo as geo_opts
from ..util.config import CONFIG
from ..util.logger import LOGGER


@click.command(
    short_help="Performs a complete geographic verification on a set of records."
)
@click.argument("src", type=click.Path(exists=True))
@click.argument("dst", type=click.Path(exists=False))
@geo_opts.lon_col
@geo_opts.lat_col
@geo_opts.crs
@geo_opts.admin0_col
@geo_opts.admin1_col
@geo_opts.admin2_col
@geo_opts.date_col
@geo_opts.species_col
@geo_opts.default_year
@geo_opts.gridres
@geo_opts.ignore
@geo_opts.drop
@common_opts.quiet
def geo(
    src,
    dst,
    lon_col,
    lat_col,
    crs,
    admin0_col,
    admin1_col,
    admin2_col,
    date_col,
    species_col,
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
    for key, admin_col in zip(
        ["admin0", "admin1", "admin2"], [admin0_col, admin1_col, admin2_col]
    ):
        records = recovery.geographic.check_historical(
            records,
            CONFIG.get("paths", key),
            date_col,
            CONFIG.get("flagnames", key),
            direction="backward",
            round_unmatched=True,
            default_year=default_year,
            op="match",
            left_col=admin_col,
            right_col=CONFIG.get("matchnames", key),
            suggested_name=CONFIG.get("suggestednames", key),
            add_source=True,
            source_name=CONFIG.get("sourcenames", key),
            drop=drop,
        )

    if not quiet:
        LOGGER.info("Identifying records in urban areas.")
    records = recovery.geographic.check_historical(
        records,
        CONFIG.get("paths", "urban"),
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
            records.geometry, CONFIG.get("paths", "dem"), interpolate="nearest"
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
        ignore=ignore
    )

    if not quiet:
        LOGGER.info("Saving result.")
    records.drop(columns="geometry").to_csv(dst, index=False)
