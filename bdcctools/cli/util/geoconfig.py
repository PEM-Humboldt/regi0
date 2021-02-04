"""
Creates a ConfigParser object with parameters to run bdcctools geo.
"""

import configparser
import os
import pathlib

import appdirs

CONFIG = configparser.ConfigParser()

CONFIG_PATH = os.path.join(appdirs.user_config_dir("bdcctools"), "geographic.ini")
if os.path.exists(CONFIG_PATH):
    CONFIG.read(CONFIG_PATH)
else:
    root = pathlib.Path(__file__).parent.parent
    template_config_file = root.joinpath("config").joinpath("geographic.ini")
    CONFIG.read(template_config_file)
