"""
$ recovery tax
"""

import click
import pandas as pd
import recovery.taxonomic

from ..options import tax as opts
from ..util.taxconfig import CONFIG
from ..util.logger import LOGGER


@click.command(
    short_help="Performs a complete taxonomic verification on a set of records."
)
@click.argument("src", type=click.Path(exists=True))
@click.argument("dst", type=click.Path(exists=False))
@opts.species_col
@opts.add_suggested
@opts.add_source
@opts.drop
@opts.quiet
def tax(
    src,
    dst,
    species_col,
    add_suggested,
    add_source,
    drop,
    quiet
):
    if not quiet:
        LOGGER.info(f"Reading records from {src}.")
    df = pd.read_csv(src)

    if not quiet:
        LOGGER.info("Validating scientific species.")
    df = recovery.taxonomic.check_species(
        df,
        species_col,
        CONFIG.get("flagnames", "species"),
        add_suggested=add_suggested,
        suggested_name=CONFIG.get("suggestednames", "species"),
        add_source=add_source,
        source_name=CONFIG.get("sourcenames", "species"),
        drop=drop
    )

    if not quiet:
        LOGGER.info(f"Saving results to {dst}.")
    df.to_csv(dst, index=False)
