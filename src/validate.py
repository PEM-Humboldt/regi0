import argparse
import configparser
import logging

import geopandas
import pandas as pd


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
    records = geopandas.read_file(input)
    records.geometry = geopandas.points_from_xy(
        records[config.get("fieldnames", "longitude")],
        records[config.get("fieldnames", "latitude")]
    )


if __name__ == "__main__":

    config = configparser.ConfigParser()
    config.read("config.ini")

    parser = argparse.ArgumentParser(description=config.get("descriptions", "tool"))
    parser.add_argument("input", type=str, help=config.get("descriptions", "input"))
    parser.add_argument("-crs", type=str, help=config.get("descriptions", "crs"))
    args = parser.parse_args()

    main(args.input, config, crs=args.crs)
