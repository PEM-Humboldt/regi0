"""
$ regi0 setup
"""
import pathlib
import shutil

import appdirs
import click

from .utils.logger import logger


@click.command()
def setup():
    """
    Sets up the configuration file required to run other CLI commands.
    """
    root = pathlib.Path(__file__).parents[0]
    config_file = root.joinpath("config/settings.ini")

    config_folder = pathlib.Path(appdirs.user_config_dir("regi0"))
    config_folder.mkdir(parents=True, exist_ok=True)
    shutil.copy(config_file, config_folder)

    logger.info(f"Copied configuration files to {config_folder}")
