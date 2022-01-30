"""
$ regi0 tax
"""
import pathlib

import click
import pandas as pd
import regi0

from ..utils.config import config
from ..utils.logger import logger


@click.command()
@click.argument("input", type=click.Path(exists=True))
@click.argument("output", type=click.Path(exists=False))
@click.option(
    "--data-source-ids",
    default="1",
    show_default=True,
    help="Data source IDs for GNR. See http://resolver.globalnames.org/data_sources.json"
    " for a list of available IDs. Multiple IDs must be separated by commas.",
)
@click.option(
    "--add-taxonomy",
    default=False,
    is_flag=True,
    show_default=True,
    help="Add superior taxonomy classification.",
)
@click.option(
    "--duplicates",
    default=False,
    is_flag=True,
    show_default=True,
    help="Identify duplicate records.",
)
@click.option(
    "--category",
    type=click.Choice(["alien", "endemic", "cites", "mads", "iucn"]),
    multiple=True,
    help="Administrative divisions to skip during verification.",
)
@click.option(
    "-r",
    "--remove",
    default=False,
    is_flag=True,
    show_default=True,
    help="Remove records with positive flags.",
)
@click.option(
    "-q",
    "--quiet",
    default=False,
    is_flag=True,
    help="Silence information logging.",
    show_default=True,
)
def tax(
    input, output, data_source_ids, add_taxonomy, duplicates, category, remove, quiet
):
    """
    Executes a flexible taxonomic verification workflow on a set of
    biological records.
    """
    if not config.sections():
        logger.error("No configuration file found. Please run regi0 setup first.")
        return

    if not quiet:
        logger.info(f"Reading records from {pathlib.Path(input).resolve()}.")
    records = regi0.read_table(input)

    if not quiet:
        logger.info(f"Getting canonical names.")
    canonical_label = config.get("suggestednames", "canonical")
    records[canonical_label] = regi0.taxonomic.get_canonical_name(
        records[config.get("colnames", "species")]
    )

    if not quiet:
        logger.info(f"Verifying scientific names using GNR.")
    data_source_ids = data_source_ids.split(",")
    classification = regi0.taxonomic.gnr.get_classification(
        records[canonical_label],
        add_supplied_names=False,
        add_source=True,
        expand=True,
        best_match_only=True,
        data_source_ids=data_source_ids,
    )
    records = regi0.verify(
        records,
        config.get("colnames", "species"),
        classification["species"],
        config.get("flagnames", "species"),
        add_suggested=True,
        suggested_name=config.get("suggestednames", "species"),
        add_source=True,
        source=classification["source"],
        source_name=config.get("sourcenames", "species"),
        drop=remove,
    )

    if add_taxonomy:
        if not quiet:
            logger.info(f"Adding superior taxonomy retrieved from GNR.")
        records = pd.concat(
            [records, classification.drop(columns=["species", "source"])], axis=1
        )

    if duplicates:
        try:
            keep = config.getboolean("duplicates", "keep")
        except ValueError:
            keep = config.get("duplicates", "keep")
        records[config.get("flagnames", "duplicate")] = records.duplicated(
            subset=[
                config.get("colnames", "species"),
                config.get("colnames", "date"),
                config.get("colnames", "collection"),
                config.get("colnames", "collector"),
            ],
            keep=keep,
        )

    if category:
        if not quiet:
            logger.info("Retrieving categories from checklist.")
        values = regi0.taxonomic.get_checklist_fields(
            records[config.get("colnames", "species")],
            config.get("paths", "checklist"),
            name_field=config.get("checklist", "species"),
            fields=[config.get("checklist", cat) for cat in category],
            add_supplied_names=False,
            expand=True,
        )
        records = pd.concat([records, values], axis=1)

    if not quiet:
        logger.info(f"Saving results to {pathlib.Path(output).resolve()}.")
    regi0.write_table(records, output, index=False)
