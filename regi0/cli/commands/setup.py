"""
$ regi0 setup
"""
import pathlib
import shutil

import appdirs
import click

from regi0.cli.utils.logger import logger


@click.command()
@click.option(
    "-o",
    "--overwrite",
    is_flag=True,
    default=False,
    show_default=True,
    help="Overwrites any existing configuration file.",
)
def setup(overwrite):
    """
    Sets up the configuration file required to run other CLI commands.
    """
    root = pathlib.Path(__file__).parents[1]
    config_file = root.joinpath("config/settings.ini")

    config_folder = pathlib.Path(appdirs.user_config_dir("regi0"))
    config_folder.mkdir(parents=True, exist_ok=True)

    if config_folder.joinpath("settings.ini").exists():
        if not overwrite:
            logger.warning(
                f"Configuration file already exists in {config_folder}. Run this command"
                f" with the -o/--overwrite flag to overwrite it."
            )
            return

    shutil.copy(config_file, config_folder)
    logger.info(f"Copied configuration file to {config_folder}")
