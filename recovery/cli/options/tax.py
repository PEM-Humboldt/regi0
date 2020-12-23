"""
Options for $ recovery tax.
"""

import click

from ..util.geoconfig import CONFIG

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


