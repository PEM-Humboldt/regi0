import datetime
import logging
import logging.config
import os

log_folder = "logs"
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

start_date = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
log_fn = os.path.join(log_folder, start_date + ".log")
logging.config.fileConfig("config/logging.ini", defaults={"logfilename": log_fn})
logger = logging.getLogger("root")
