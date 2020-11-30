import configparser
import logging
import logging.config

import click

import recovery.geographic as rgeo

logging.config.fileConfig("config/logger.ini")
logger = logging.getLogger(__name__)

config = configparser.ConfigParser()
config.read("config/settings.ini")


@click.command()
@click.argument("src", type=str)
@click.option(
    "--lon_col",
    type=str,
    default=config.get("colnames", "longitude"),
    help="Longitude column."
)
@click.option(
    "--lat_col",
    type=str,
    default=config.get("colnames", "latitude"),
    help="Latitude column."
)
@click.option(
    "--crs",
    type=str,
    default="epsg:4326",
    help="Coordinate Reference System (epsg:code)."
)
@click.option(
    "--admin0_col",
    type=str,
    default=config.get("colnames", "admin0"),
    help="Level 0 administrative division column (i.e. country).",
)
@click.option(
    "--admin1_col",
    type=str,
    default=config.get("colnames", "admin1"),
    help="Level 1 administrative division column (e.g. department or state).",
)
@click.option(
    "--admin2_col",
    type=str,
    default=config.get("colnames", "admin2"),
    help="Level 2 administrative division column (e.g. municipality or county).",
)
@click.option(
    "--date_col",
    type=str,
    default=config.get("colnames", "date"),
    help="Collection date column."
)
@click.option(
    "--default-year",
    type="str",
    default=None,
    help=""
)
@click.option(
    "--drop", default=False, is_flag=True, help="Drop records with a positive flag."
)
@click.option(
    "--quiet", default=False, is_flag=True, help="Silence information logging."
)
def main(
    src,
    lon_col,
    lat_col,
    crs,
    admin0_col,
    admin1_col,
    admin2_col,
    date_col,
    default_year,
    drop,
    quiet,
):

    if not quiet:
        logger.info("Reading records.")
    records = rgeo.read_records(src, lon_col, lat_col, crs=crs, drop_empty_coords=True)

    if not quiet:
        logger.info("Validating administrative boundaries.")
    for key, admin_col in zip(
        ["admin0", "admin1", "admin2"], [admin0_col, admin1_col, admin2_col]
    ):
        records = rgeo.check_historical(
            records,
            config.get("paths", key),
            config.date_col,
            config.get("flagnames", key),
            direction="backward",
            round_unmatched=True,
            default_year="last",
            op="match",
            left_col=admin_col,
            right_col=config.get("matchnames", key),
            suggested_name=config.get("suggestednames", key),
            add_source=True,
            source_name=config.get("sourcenames", key),
            drop=drop,
        )

    if not quiet:
        logger.info("Identifying records in urban areas.")
    records = rgeo.check_historical(
        records,
        config.get("paths", "urban"),
        date_col,
        config.get("flagnames", "urban"),
        direction="nearest",
        default_year=default_year,
        op="intersection",
        add_source=True,
        source_name=config.get("sourcenames", "urban"),
        drop=drop
    )
