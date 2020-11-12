import argparse
import configparser
import logging
import logging.config
import os

import geopandas
import pandas as pd

# from .functions import drop_empty_coords


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
    longitude_col = config.get("fieldnames", "longitude")
    latitude_col = config.get("fieldnames", "latitude")

    dtypes = {
        longitude_col: float,
        latitude_col: float
    }

    input_ext = os.path.splitext(input)[1]
    if input_ext == ".csv":
        records = pd.read_csv(input, dtype=dtypes)
    elif input_ext == ".xlsx":
        records = pd.read_excel(input, dtype=dtypes)
    else:
        pass

    # records = drop_empty_coords(records, longitude_col, latitude_col)

    geometry = geopandas.points_from_xy(records[longitude_col], records[latitude_col])
    records = geopandas.GeoDataFrame(records, geometry=geometry)


if __name__ == "__main__":

    desc = configparser.ConfigParser()
    desc.read("descriptions.ini")

    parser = argparse.ArgumentParser(description=desc.get("tool", "general"))
    parser.add_argument("input", type=str, help=desc.get("args", "input"))
    parser.add_argument("-crs", type=str, help=desc.get("args", "crs"))
    parser.add_argument("-c", type=str, default="config.ini", help=desc.get("args", "c"))
    parser.add_argument("-l", type=str, default="info.log")
    args = parser.parse_args()

    if not os.path.exists(args.c):
        print("Shit")
    config = configparser.ConfigParser()
    try:
        config.read(args.c)
    except configparser.Error:
        print("fuck")

    # main(args.input, config, crs=args.crs)
