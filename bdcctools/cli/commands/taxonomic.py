"""
$ bdcctools taxonomic
"""
import glob
import os

import click
import pandas as pd
from bdcctools.io import read_table, write_table
from bdcctools.taxonomic.local import get_checklist_fields_multiple
from bdcctools.taxonomic.web.gnr import get_classification
from bdcctools.utils import verify

from ..options import taxonomic as opts
from ..util.config import CONFIG
from ..util.logger import LOGGER


@click.command(
    short_help="Performs a complete taxonomic verification on a set of records."
)
@click.argument("src", type=click.Path(exists=True))
@click.argument("dst", type=click.Path(exists=False))
@opts.species_col
@opts.data_sources
@opts.checklists_path
@opts.fields
@opts.drop
@opts.quiet
def taxonomic(
    src,
    dst,
    species_col,
    data_sources,
    checklists_path,
    fields,
    drop,
    quiet
):
    if not quiet:
        LOGGER.info(f"Reading records from {src}.")
    records = read_table(src)

    if not quiet:
        LOGGER.info("Validating scientific names using GNR.")
    if data_sources:
        data_sources = data_sources.split(",")
    classification = get_classification(
        records[species_col],
        add_supplied_names=False,
        add_source=True,
        expand=True,
        best_match_only=True,
        data_source_ids=data_sources
    )
    species = classification["species"]
    flag_name = CONFIG.get("flagnames", "species")
    suggested_name = CONFIG.get("suggestednames", "species")
    records = verify(
        records,
        species_col,
        species,
        flag_name,
        add_suggested=True,
        suggested_name=suggested_name,
        drop=drop
    )
    records[CONFIG.get("sourcenames", "species")] = classification["source"]

    # For extracting new information based on the scientific names, it is
    # necessary to pass accepted scientific names. Hence, if the user a
    # new series is created with the combination of originally correct
    # names and the new suggested ones for those cases where the resolver
    # found a suggestion.
    accepted_names = records.loc[records[flag_name], species_col]
    suggested_names = records.loc[~records[flag_name], suggested_name]
    names = pd.concat([accepted_names, suggested_names]).sort_index()

    if checklists_path:
        filenames = glob.glob(os.path.join(checklists_path, "*"))
    if fields:
        fields = list(fields)
        if not quiet:
            LOGGER.info("Retrieving fields from local checklists.")
        result = get_checklist_fields_multiple(
            names,
            filenames,
            species_col,
            fields,
            add_supplied_names=False,
            expand=True,
            keep_first=True,
            add_source=True,
            source_name="source"
        )
        records = pd.concat([records, result], axis=1)

    if not quiet:
        LOGGER.info(f"Saving results to {dst}.")
    write_table(records, dst, index=False)
