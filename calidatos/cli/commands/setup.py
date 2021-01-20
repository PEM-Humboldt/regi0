"""
$ calidatos setup
"""

import pathlib
import os
import shutil

import appdirs
import click


@click.command(
    short_help="Setups the configuration files required to run the other CLI commands."
)
def setup():

    root = pathlib.Path(__file__).parent.parent
    template_config_folder = root.joinpath("config")
    target_conf_folder = appdirs.user_config_dir("calidatos")
    if not os.path.exists(target_conf_folder):
        os.makedirs(target_conf_folder)

    for config_file in template_config_folder.glob("*.ini"):
        shutil.copy(config_file, target_conf_folder)
