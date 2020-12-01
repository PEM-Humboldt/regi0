"""$ recovery download"""

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

    if not quiet:
        LOGGER.info(f"Downloading data from {url}.")
    file_name = gdown.download(url, dst, quiet=True)

    if not quiet:
        LOGGER.info(f"Extracting data in {os.path.basename(file_name)}")
    paths = gdown.extractall(file_name)
    file_paths = filter(os.path.isfile, paths)

    if not quiet:
        LOGGER.info(f"Updating config at {CONFIG_PATH}.")
    for path in file_paths:
        name = os.path.splitext(os.path.basename(path))[0]
        if CONFIG.has_option("paths", name):
            CONFIG.set("paths", name, path)
    with open(CONFIG_PATH, "w") as config_file:
        CONFIG.write(config_file)
