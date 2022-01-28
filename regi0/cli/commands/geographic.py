"""
$ regi0 geo
"""
import pathlib
import sys

import click
import regi0

from ..utils.config import config
from ..utils.logger import logger


@click.command()
@click.argument("input", type=click.Path(exists=True))
@click.argument("output", type=click.Path(exists=False))
@click.option(
    "-a",
    "--admin",
    type=click.Choice(["country", "stateProvince", "county"]),
    multiple=True,
    help="Administrative divisions to verify.",
)
@click.option(
    "-u",
    "--urban",
    default=False,
    is_flag=True,
    help="Verify urban limits.",
    show_default=True,
)
@click.option(
    "-d",
    "--duplicates",
    default=False,
    is_flag=True,
    help="Identify duplicate records.",
    show_default=True,
)
@click.option(
    "-r",
    "--remove",
    default=False,
    is_flag=True,
    help="Remove records with positive flags.",
    show_default=True,
)
@click.option(
    "-q",
    "--quiet",
    default=False,
    is_flag=True,
    help="Silence information logging.",
    show_default=True,
)
def geo(input, output, admin, urban, duplicates, remove, quiet):
    """
    Executes a flexible _geographic verification workflow on a set of
    biological records.
    """
    if not config.sections():
        logger.error("No configuration file found. Please run regi0 setup first.")
        sys.exit()

    if not quiet:
        logger.info(f"Reading records from {pathlib.Path(input).resolve()}.")
    records = regi0.read_geographic_table(
        input,
        config.get("colnames", "longitude"),
        config.get("colnames", "latitude"),
        crs=config.get("misc", "crs"),
        drop_empty_coords=True,
        reset_index=True,
    )

    admin_map = {"country": "admin0", "stateProvince": "admin1", "county": "admin2"}
    for name, level in admin_map.items():
        if name in admin:
            if not quiet:
                logger.info(f"Verifying {name} divisions.")
            values, source = regi0.geographic.get_layer_field_historical(
                records,
                config.get("paths", level),
                config.get("colnames", "date"),
                config.get("attributes", level),
                direction=config.get("misc", "direction"),
                return_source=True,
            )
            records = regi0.verify(
                records,
                config.get("colnames", level),
                values,
                config.get("flagnames", level),
                add_suggested=True,
                suggested_name=config.get("suggestednames", level),
                add_source=True,
                source=source,
                source_name=config.get("sourcenames", level),
                drop=remove,
                preprocess=config.get("verification", "preprocess"),
                fuzzy=config.get("verification", "fuzzy"),
                threshold=config.getfloat("verification", "threshold"),
            )

    if urban:
        if not quiet:
            logger.info("Verifying urban limits.")
        flagname = config.get("flagnames", "urban")
        records[flagname] = regi0.geographic.intersects_layer(
            records, config.get("paths", "urban")
        )
        if remove:
            records = records[~records[flagname]]

    if duplicates:
        if not quiet:
            logger.info("Identifying duplicate records.")

        bounds = config.get("duplicates", "bounds")
        if bounds:
            bounds = list(map(lambda x: float(x), bounds.split(",")))
        else:
            bounds = None

        try:
            keep = config.getboolean("duplicates", "keep")
        except ValueError:
            keep = config.get("duplicates", "keep")

        flagname = config.get("flagnames", "spatialduplicate")
        records[flagname] = regi0.geographic.find_grid_duplicates(
            records,
            config.get("colnames", "species"),
            config.getfloat("duplicates", "pixelsize"),
            bounds,
            keep,
        )
        if remove:
            records = records[~records[flagname]]

    if not quiet:
        logger.info(f"Saving results to {pathlib.Path(output).resolve()}.")
    records = records.drop(columns="geometry")
    regi0.write_table(records, output, index=False)
