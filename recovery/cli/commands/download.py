"""
$ recovery download
"""

import os

import click
import gdown

from ..options import common as common_opts
from ..util.config import CONFIG, CONFIG_PATH
from ..util.logger import LOGGER


@click.command(
    short_help="Download necessary data to run the recovery geo command line utility."
)
@click.argument("dst", type=str, default=None, required=False)
@click.argument("url", type=str, default=CONFIG.get("misc", "url"))
@common_opts.quiet
def download(dst, url, quiet):

    if not os.path.exists(CONFIG_PATH):
        raise Exception("Config file not found. Run `recovery setup` first.")

    output_path = gdown.download(url, dst, quiet=quiet)

    if not quiet:
        LOGGER.info(f"Extracting data in {os.path.basename(output_path)}")
    extracted_paths = gdown.extractall(output_path)

    if not quiet:
        LOGGER.info(f"Updating config at {CONFIG_PATH}.")
    for path in extracted_paths:
        if os.path.isfile(path):
            path = os.path.abspath(path)
            name = os.path.splitext(os.path.basename(path))[0]
            if CONFIG.has_option("paths", name):
                CONFIG.set("paths", name, path)
    with open(CONFIG_PATH, "w") as config_file:
        CONFIG.write(config_file)
