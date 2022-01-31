"""
ConfigParser object with parameters to run $ regi0 _geographic
"""
import configparser
import pathlib

import appdirs

config = configparser.ConfigParser()

config_path = pathlib.Path(appdirs.user_config_dir("regi0")).joinpath("settings.ini")
if config_path.exists():
    config.read(config_path)
