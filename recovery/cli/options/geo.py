"""
Options for $ recovery geo.
"""

import click

from ..util.geoconfig import CONFIG

crs = click.option(
    "--crs",
    type=str,
    default=CONFIG.get("misc", "crs"),
    help="Coordinate Reference System in the form epsg:code.",
    show_default=True
)

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

date_col = click.option(
    "--date_col",
    type=str,
    default=CONFIG.get("colnames", "date"),
    help="Collection date column.",
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

species_col = click.option(
    "--species-col",
    type=str,
    default=CONFIG.get("colnames", "species"),
    help="Species name column.",
    show_default=True
)

admin0_path = click.option(
    "--admin0_path",
    type=click.Path(exists=True),
    default=CONFIG.get("paths", "admin0"),
    help="""
        Path to a .gpkg file or a folder with .shp files with the level 0
        administrative boundaries.
    """,
    show_default=True
)

admin1_path = click.option(
    "--admin1_path",
    type=click.Path(exists=True),
    default=CONFIG.get("paths", "admin1"),
    help="""
        Path to a .gpkg file or a folder with .shp files with the level 1
        administrative boundaries.
    """,
    show_default=True
)

admin2_path = click.option(
    "--admin2_path",
    type=click.Path(exists=True),
    default=CONFIG.get("paths", "admin2"),
    help="""
        Path to a .gpkg file or a folder with .shp files with the level 2
        administrative boundaries.
    """,
    show_default=True
)

urban_path = click.option(
    "--urban_path",
    type=click.Path(exists=True),
    default=CONFIG.get("paths", "urban"),
    help="""
        Path to a .gpkg file or a folder with .shp files with the urban/population
        centers polygons.
    """,
    show_default=True,
)

dem_path = click.option(
    "--dem_path",
    type=click.Path(exists=True),
    default=CONFIG.get("paths", "dem"),
    help="Path to a raster file with a Digital Elevation Model (DEM).",
    show_default=True,
)

admin0_match = click.option(
    "--admin0_match",
    type=str,
    default=CONFIG.get("matchfields", "admin0"),
    help="Field name to match records using admin0_col.",
    show_default=True
)

admin1_match = click.option(
    "--admin1_match",
    type=str,
    default=CONFIG.get("matchfields", "admin1"),
    help="Field name to match records using admin1_col.",
    show_default=True
)

admin2_match = click.option(
    "--admin2_match",
    type=str,
    default=CONFIG.get("matchfields", "admin2"),
    help="Field name to match records using admin2_col.",
    show_default=True
)

default_year = click.option(
    "--default-year",
    type=str,
    default=CONFIG.get("misc", "defaultyear"),
    help="""
        Default year to take for records that do not have a collection date or whose 
        collection data did not match with any year. Can be 'last' for the most recent 
        year in the historical data, 'first' for the oldest year in the historical data 
        or 'none' to ignore the verification on records without a date.
    """,
    show_default=True
)

gridres = click.option(
    "--gridres",
    type=float,
    default=CONFIG.getfloat("duplicates", "gridres"),
    help="""
        Resolution of the grid to identify spatial duplicated records. Units must be the 
        same as crs.
    """,
    show_default=True
)

mark = click.option(
    "--mark",
    type=str,
    default=CONFIG.get("duplicates", "mark"),
    help="What duplicates to mark. Can be 'head', 'tail' or 'all'.",
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
