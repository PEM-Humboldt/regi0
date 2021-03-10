"""
$ bdcctools download
"""
import os

import click
import gdown

from ..util.config import CONFIG, CONFIG_PATH
from ..util.logger import LOGGER


@click.command(
    short_help="Download necessary data to run the bdcctools geographic and taxonomic "
               "command line utilities."
)
@click.argument("url", type=str)
@click.argument("dst", type=str, default=None, required=False)
@click.option(
    "--quiet",
    default=False,
    is_flag=True,
    help="Silence information logging.",
    show_default=True
)
def download(url, dst, quiet):
    if not os.path.exists(CONFIG_PATH):
        raise Exception("Config file not found. Run `bdcctools setup` first.")

    output_path = gdown.download(url, dst, quiet=quiet)

    if not quiet:
        LOGGER.info(f"Extracting data in {os.path.basename(output_path)}")
    extracted_paths = gdown.extractall(output_path)
    print(extracted_paths)

    if not quiet:
        LOGGER.info(f"Updating config at {CONFIG_PATH}.")
    for path in extracted_paths:
        if os.path.isfile(path):
            path = os.path.abspath(path)
            name = os.path.splitext(os.path.basename(path))[0]
            if CONFIG.has_option("paths", name):
                CONFIG.set("paths", name, path)
        else:
            if path.endswith("txt/"):
                CONFIG.set("paths", "checklists", path)
    with open(CONFIG_PATH, "w") as config_file:
        CONFIG.write(config_file)
