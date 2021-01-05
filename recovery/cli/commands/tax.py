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
@opts.add_authority
@opts.authority_col
@opts.add_cites_listing
@opts.cites_listing_col
@opts.add_risk_category
@opts.risk_category_col
@opts.drop
@opts.quiet
def tax(
    src,
    dst,
    species_col,
    add_suggested,
    add_source,
    add_authority,
    authority_col,
    add_cites_listing,
    cites_listing_col,
    add_risk_category,
    risk_category_col,
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

    if add_authority:
        if not quiet:
            LOGGER.info("Retrieving scientific name authorship.")
        df[authority_col] = recovery.taxonomic.get_authority(
            df[species_col], CONFIG.get("tokens", "iucn")
        )

    if add_cites_listing:
        if not quiet:
            LOGGER.info("Retrieving cites listing.")
        df[cites_listing_col] = recovery.taxonomic.get_cites_listing(
            df[species_col], CONFIG.get("tokens", "speciesplus")
        )

    if add_risk_category:
        if not quiet:
            LOGGER.info("Retrieving global risk categories from IUCN.")
        df[risk_category_col] = recovery.taxonomic.get_risk_category(
            df[species_col], CONFIG.get("tokens", "iucn")
        )

    if not quiet:
        LOGGER.info(f"Saving results to {dst}.")
    df.to_csv(dst, index=False)
