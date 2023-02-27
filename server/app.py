import sys
import traceback
import logging.config

from flask import Flask

from config import config
from loggers import logger
from server.funcs.path_module import path_to_file, create_dir

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello BagHou!"


def log_handler(exctype, value, tb):
    """
    Custom exception handler.
    All critical errors will be logged with tag [ERROR]
    """
    logger.exception(''.join(traceback.format_exception(exctype, value, tb)))


# Create folder for log and load log configuration
create_dir("logs")

logging.config.fileConfig(fname=path_to_file("logging.conf"), disable_existing_loggers=False)
if not config["debug"]:
    logging.disable(level=logging.WARNING)
sys.excepthook = log_handler

if __name__ == "__main__":
    app.run(debug=config["debug"])
