import configparser
import os

import appdirs

CONFIG = configparser.ConfigParser()

CONFIG_PATH = os.path.join(appdirs.user_config_dir("recovery"), "settings.ini")
if os.path.exists(CONFIG_PATH):
    CONFIG.read(CONFIG_PATH)
