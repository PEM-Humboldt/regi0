import configparser
import os

from log import logger


def validate_config_file(path: str) -> configparser.ConfigParser:
    """

    Parameters
    ----------
    path

    Returns
    -------

    """
    if not os.path.exists(path):
        logger.error("The specified config file does not exist.")
        raise SystemExit(1)

    config = configparser.ConfigParser()
    try:
        config.read(path)
    except configparser.Error as e:
        logger.error("The specified config file is not a valid config file.")
        raise SystemExit(1)

    return config
