import argparse
import configparser
import datetime
import logging
import logging.config
import os

from geovalidation import read_input


def main(fn: str, logger, config, crs: str = "epsg:4326") -> None:
    """

    Parameters
    ----------
    fn
    logger
    config
    crs

    Returns
    -------

    """
    lon_col = config.get("colnames", "longitude")
    lat_col = config.get("colnames", "latitude")
    elev_col = config.get("colnames", "elevation")

    records = read_input(fn, lon_col, lat_col, elev_col, crs=crs, drop_empty_coords=True)


if __name__ == "__main__":

    log_folder = "logs"
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)
    start_date = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    log_fn = os.path.join(log_folder, start_date + ".log")
    logging.config.fileConfig("config/loggers.ini", defaults={"logfilename": log_fn})
    logger = logging.getLogger("root")

    config = configparser.ConfigParser()
    config.read("config/settings.ini")

    parser = argparse.ArgumentParser(description=config.get("texts", "tool"))
    parser.add_argument("table", type=str, help=config.get("texts", "table"))
    parser.add_argument("-crs", type=str, help=config.get("texts", "crs"))
    args = parser.parse_args()

    main(args.input, logger, config, crs=args.crs)
