import configparser
import logging
import logging.config
import warnings

import click
from rasterstats import point_query

import recovery.geographic as rgeo

logging.config.fileConfig("config/logger.ini")
logger = logging.getLogger(__name__)

config = configparser.ConfigParser()
config.read("config/settings.ini")

warnings.filterwarnings("ignore")


@click.command()
@click.argument("src", type=str)
@click.argument("dst", type=str)
@click.option(
    "--lon_col",
    type=str,
    default=config.get("colnames", "longitude"),
    help="Longitude column.",
    show_default=True
)
@click.option(
    "--lat_col",
    type=str,
    default=config.get("colnames", "latitude"),
    help="Latitude column.",
    show_default=True
)
@click.option(
    "--crs",
    type=str,
    default="epsg:4326",
    help="Coordinate Reference System in the form epsg:code.",
    show_default=True
)
@click.option(
    "--admin0_col",
    type=str,
    default=config.get("colnames", "admin0"),
    help="Level 0 administrative division column (i.e. country).",
    show_default=True
)
@click.option(
    "--admin1_col",
    type=str,
    default=config.get("colnames", "admin1"),
    help="Level 1 administrative division column (e.g. department or state).",
    show_default=True
)
@click.option(
    "--admin2_col",
    type=str,
    default=config.get("colnames", "admin2"),
    help="Level 2 administrative division column (e.g. municipality or county).",
    show_default=True
)
@click.option(
    "--date_col",
    type=str,
    default=config.get("colnames", "date"),
    help="Collection date column.",
    show_default=True
)
@click.option(
    "--species-col",
    type=str,
    default=config.get("colnames", "species"),
    help="Species name column.",
    show_default=True
)
@click.option(
    "--default-year",
    type=str,
    default=None,
    help="Default year to take for records that do not have a collection date or whose "
         "collection data did not match with any year. Can be 'last' for the most recent"
         " year in the historical data or 'first' for the oldest year in the historical "
         "data. Do not pass this parameter to ignore the verification on records without"
         " a date.",
    show_default=True
)
@click.option(
    "--gridres",
    type=float,
    default=config.getfloat("misc", "resolution"),
    help="Resolution of the grid to identify spatial duplicated. Units must be the same "
         "as crs.",
    show_default=True
)
@click.option(
    "--ignore",
    type=str,
    default=False,
    help="What records that are spatial duplicates to ignore. Can be 'first' or 'last'. "
         "Do not pass this parameter to not ignore any record.",
    show_default=True
)
@click.option(
    "--drop",
    default=False,
    is_flag=True,
    help="Drop records with a positive flag.",
    show_default=True
)
@click.option(
    "--quiet",
    default=False,
    is_flag=True,
    help="Silence information logging.",
    show_default=True
)
def main(
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
            date_col,
            config.get("flagnames", key),
            direction="backward",
            round_unmatched=True,
            default_year=default_year,
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

    if not quiet:
        logger.info("Extracting elevation values and identifying outliers.")
    records[config.get("valuenames", "elevation")] = point_query(
            records.geometry, config.get("paths", "dem"), interpolate="nearest"
    )
    records = rgeo.find_outliers(
        records,
        species_col,
        config.get("valuenames", "elevation"),
        config.get("flagnames", "elevation"),
        method="iqr",
        drop=drop
    )

    if not quiet:
        logger.info("Identifying spatial duplicates.")
    records = rgeo.find_spatial_duplicates(
        records,
        species_col,
        config.get("flagnames", "spatialduplicate"),
        resolution=gridres,
        drop=drop,
        ignore=ignore
    )

    if not quiet:
        logger.info("Saving result.")
    records.drop(columns="geometry").to_csv(dst, index=False)
