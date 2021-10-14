"""
Options for $ regi0 taxonomic
"""
import click

from ..util.config import CONFIG

species_col = click.option(
    "--species-col",
    type=str,
    default=CONFIG.get("colnames", "species"),
    help="Species name column.",
    show_default=True
)

data_sources = click.option(
    "--data-sources",
    type=str,
    default=None,
    help="Data source IDs to pass to Global Names Resolver API.",
    show_default=True
)

checklists_path = click.option(
    "--checklists-path",
    type=click.Path(exists=True),
    default=CONFIG.get("paths", "checklists"),
    help="Path to a folder with the checklists.",
    show_default=True
)

fields = click.option(
    "--fields",
    type=str,
    default=None,
    help="Checklist field(s) to retrieve. Pass it multiple times for multiple fields.",
    multiple=True,
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
