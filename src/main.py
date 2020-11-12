import argparse
import configparser
import os

import geopandas
import pandas as pd

from argvalidation import validate_config_file
from geovalidation import drop_empty_coords
from log import logger


def main(input: str, config: configparser.ConfigParser, crs: str = "epsg:4326") -> None:
    """

    Parameters
    ----------
    input
    config
    crs

    Returns
    -------

    """
    longitude_col = config.get("colnames", "longitude")
    latitude_col = config.get("colnames", "latitude")




if __name__ == "__main__":

    desc = configparser.ConfigParser()
    desc.read("config/descriptions.ini")

    msg = configparser.ConfigParser()
    msg.read("config/messages.ini")

    parser = argparse.ArgumentParser(description=desc.get("tool", "general"))
    parser.add_argument("input", type=str, help=desc.get("args", "input"))
    parser.add_argument("-crs", type=str, help=desc.get("args", "crs"))
    parser.add_argument(
        "-c", type=str, default="config/settings.ini", help=desc.get("args", "c")
    )
    args = parser.parse_args()

    logger.info(msg.get("info", "argval"))
    config = validate_config_file(args.c)

    # main(args.input, config, crs=args.crs)
