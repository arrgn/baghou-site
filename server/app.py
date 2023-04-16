import logging.config
import sys
import traceback

from flask import make_response
from jwt import ExpiredSignatureError
from werkzeug.exceptions import HTTPException

from server import app
from server import config
from server.funcs.path_module import path_to_file, create_dir
from server.loggers import logger
from server.services.user_service import UserService


@app.post("/auth/reg")
def reg():
    return UserService.reg()


@app.post("/auth/login")
def login():
    return UserService.login()


@app.get("/auth/refresh")
def refresh():
    return UserService.refresh_access_token()


@app.errorhandler(HTTPException)
def a(e):
    res = make_response(e.description)
    res.status = e.code
    return res


@app.errorhandler(ExpiredSignatureError)
def expired_signature_error(e):
    res = make_response({"msg": "Пользователь не авторизован!"})
    res.status = 401
    return res


@app.errorhandler(Exception)
def something_went_wrong_error(e):
    logger.exception(e)
    res = make_response({"msg": "Что-то пошло не так."})
    res.status = 500
    return res


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
