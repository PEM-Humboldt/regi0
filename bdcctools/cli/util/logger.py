"""
Create logger object so CLI commands can access it.
"""

import logging
import logging.config
import os

import appdirs

LOGGER = None

config_path = os.path.join(appdirs.user_config_dir("bdcctools"), "logger.ini")
if os.path.exists(config_path):
    logging.config.fileConfig(config_path)
    LOGGER = logging.getLogger(__name__)
