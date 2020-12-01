"""
Options for $ recovery geo.
"""

import click

from ..util.config import CONFIG

lon_col = click.option(
    "--lon_col",
    type=str,
    default=CONFIG.get("colnames", "longitude"),
    help="Longitude column.",
    show_default=True
)

lat_col = click.option(
    "--lat_col",
    type=str,
    default=CONFIG.get("colnames", "latitude"),
    help="Latitude column.",
    show_default=True
)

crs = click.option(
    "--crs",
    type=str,
    default="epsg:4326",
    help="Coordinate Reference System in the form epsg:code.",
    show_default=True
)

admin0_col = click.option(
    "--admin0_col",
    type=str,
    default=CONFIG.get("colnames", "admin0"),
    help="Level 0 administrative division column (i.e. country).",
    show_default=True
)

admin1_col = click.option(
    "--admin1_col",
    type=str,
    default=CONFIG.get("colnames", "admin1"),
    help="Level 1 administrative division column (e.g. department or state).",
    show_default=True
)

admin2_col = click.option(
    "--admin2_col",
    type=str,
    default=CONFIG.get("colnames", "admin2"),
    help="Level 2 administrative division column (e.g. municipality or county).",
    show_default=True
)

date_col = click.option(
    "--date_col",
    type=str,
    default=CONFIG.get("colnames", "date"),
    help="Collection date column.",
    show_default=True
)

species_col = click.option(
    "--species-col",
    type=str,
    default=CONFIG.get("colnames", "species"),
    help="Species name column.",
    show_default=True
)

default_year = click.option(
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

gridres = click.option(
    "--gridres",
    type=float,
    default=CONFIG.getfloat("misc", "resolution"),
    help="Resolution of the grid to identify spatial duplicated. Units must be the same "
         "as crs.",
    show_default=True
)

ignore = click.option(
    "--ignore",
    type=str,
    default=False,
    help="What records that are spatial duplicates to ignore. Can be 'first' or 'last'. "
         "Do not pass this parameter to not ignore any record.",
    show_default=True
)

drop = click.option(
    "--drop",
    default=False,
    is_flag=True,
    help="Drop records with a positive flag.",
    show_default=True
)
