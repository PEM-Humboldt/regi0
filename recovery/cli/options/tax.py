"""
Options for $ recovery tax.
"""

import click

from ..util.taxconfig import CONFIG

species_col = click.option(
    "--species-col",
    type=str,
    default=CONFIG.get("colnames", "species"),
    help="Species name column.",
    show_default=True
)

add_suggested = click.option(
    "--add-suggested",
    default=CONFIG.getboolean("behaviour", "add_suggested"),
    is_flag=True,
    help="Add suggested species names.",
    show_default=True
)

add_source = click.option(
    "--add-source",
    default=CONFIG.getboolean("behaviour", "add_source"),
    is_flag=True,
    help="Add source for suggested species names.",
    show_default=True
)

add_authority = click.option(
    "--add-authority",
    default=CONFIG.getboolean("behaviour", "add_authority"),
    is_flag=True,
    help="Add scientific name authority.",
    show_default=True
)

authority_col = click.option(
    "--authority-col",
    default=CONFIG.get("colnames", "authority"),
    type=str,
    help="Name for the authority column.",
    show_default=True
)

add_cites_listing = click.option(
    "--add-cites-listing",
    default=CONFIG.getboolean("behaviour", "add_cites_listing"),
    is_flag=True,
    help="Add cites listing.",
    show_default=True
)

cites_listing_col = click.option(
    "--cites-listing-col",
    default=CONFIG.get("colnames", "cites_listing"),
    type=str,
    help="Name for the cites listing column.",
    show_default=True
)

add_risk_category = click.option(
    "--add-risk-category",
    default=CONFIG.getboolean("behaviour", "add_risk_category"),
    is_flag=True,
    help="Add IUCN risk category.",
    show_default=True
)

risk_category_col = click.option(
    "--risk-category-col",
    default=CONFIG.get("colnames", "risk_category"),
    type=str,
    help="Name for the risk category column.",
    show_default=True
)

drop = click.option(
    "--drop",
    default=CONFIG.getboolean("behaviour", "drop"),
    is_flag=True,
    help="Drop records with a positive flag.",
    show_default=True
)

quiet = click.option(
    "--quiet",
    default=CONFIG.getboolean("behaviour", "quiet"),
    is_flag=True,
    help="Silence information logging.",
    show_default=True
)


