"""
Logger object accessible by CLI commands.
"""
import logging
import logging.config
import pathlib

root = pathlib.Path(__file__).parents[1]
config_path = root.joinpath("config").joinpath("logger.ini")
logging.config.fileConfig(config_path)
logger = logging.getLogger(__name__)
