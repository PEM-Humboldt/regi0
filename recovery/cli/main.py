import argparse
import configparser
import datetime
import logging
import logging.config
import os

from rasterstats import point_query

from geovalidation import (
    read_records,
    check_historical,
    find_outliers,
    find_spatial_duplicates,
)


def main(
    src: str,
    dst: str,
    logger: logging.Logger,
    config: configparser.ConfigParser,
    crs: str = "epsg:4326",
    drop: bool = False,
) -> None:
    """
    Performs a complete geographical validation on a dataset of biological
    records and saves a copy or a subset of the original file with the
    corresponding new columns.

    Parameters
    ----------
    src:    Absolute or relative path of the input table. Only csv and
            xlsx files are supported.
    dst:    Absolute or relative path of the output table. Only csv files
            are supported.
    logger: Logger object to output information and errors.
    config: Configuration object with the parameters to run the tool.
    crs:    Coordinate Reference System of the records. Must be in the
            form epsg:code.
    drop:   Whether to drop records with positive flags.

    Returns
    -------
    None
    """

    try:
        logger.info("Reading records...")
        records = read_records(
            src,
            config.get("colnames", "longitude"),
            config.get("colnames", "latitude"),
            crs=crs,
            drop_empty_coords=True
        )

        logger.info("Validating administrative boundaries...")
        for key in ["admin0", "admin1", "admin2"]:
            records = check_historical(
                records,
                config.get("paths", key),
                config.get("colnames", "date"),
                config.get("flagnames", key),
                direction="backward",
                default_year="last",
                op="match",
                left_col=config.get("colnames", key),
                right_col=config.get("matchnames", key),
                suggested_name=config.get("suggestednames", key),
                add_source=True,
                source_name=config.get("sourcenames", key),
                drop=drop
            )

        logger.info("Identifying records in urban areas")
        records = check_historical(
            records,
            config.get("paths", "urban"),
            config.get("colnames", "date"),
            config.get("flagnames", "urban"),
            direction="nearest",
            default_year="last",
            op="intersection",
            add_source=True,
            source_name=config.get("sourcenames", "urban"),
            drop=drop
        )

        logger.info("Extracting elevation values...")
        records[config.get("valuenames", "elevation")] = point_query(
            records.geometry, config.get("paths", "dem"), interpolate="nearest"
        )

        logger.info("Validating consistency in elevation values...")
        records = find_outliers(
            records,
            config.get("colnames", "species"),
            config.get("valuenames", "elevation"),
            config.get("flagnames", "elevation"),
            method="zscore",
            drop=drop
        )

        logger.info("Identifying spatial duplicates...")
        records = find_spatial_duplicates(
            records,
            config.get("colnames", "species"),
            config.get("flagnames", "spatialduplicate"),
            resolution=config.getfloat("misc", "resolution"),
            drop=drop,
            keep="first"
        )

        logger.info("Saving result...")
        records.drop(columns="geometry").to_csv(dst, index=False)

    except:
        logger.exception("Something went wrong.")
        raise


if __name__ == "__main__":

    log_folder = "logs"
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)
    start_date = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    log_fn = os.path.join(log_folder, start_date + ".log")
    logging.config.fileConfig("../../config/logger.ini", defaults={"logfilename": log_fn})
    logger = logging.getLogger("root")

    config = configparser.ConfigParser()
    config.read("config/settings.ini")

    parser = argparse.ArgumentParser(description=config.get("texts", "tool"))
    parser.add_argument("recovery", type=str, help=config.get("texts", "recovery"))
    parser.add_argument("dst", type=str, help=config.get("texts", "dst"))
    parser.add_argument(
        "-crs", type=str, default="epsg:4326", help=config.get("texts", "crs")
    )
    parser.add_argument("--drop", help=config.get("texts", "drop"), action="store_true")
    args = parser.parse_args()

    main(args.src, args.dst, logger, config, crs=args.crs, drop=args.drop)
