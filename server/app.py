import sys
import traceback
import logging.config
import re

from flask import Flask, request
from bcrypt import hashpw, checkpw, gensalt

from config import config
from loggers import logger
from server.funcs.path_module import path_to_file, create_dir
from data.db_session import create_session, global_init
from data.__all_models import User

app = Flask(__name__)

global_init()


@app.post("/reg")
def reg():
    try:
        username = request.json["username"]
        email = request.json["email"]
        password = request.json["password"]
        hashed_password = hashpw(password.encode("utf-8"), gensalt())

        if not re.match("[^@]+@[^@]+\.[^@]+", email):
            return {"status": 400, "msg": "Некорректный адрес электронной почты"}

        dao = create_session()

        # here crashes
        if dao.query(User).filter(User.email == email).first():
            return {"status": 400, "msg": "Пользователь с такой почтой уже существует!"}

        user = User(
            name=username,
            email=email,
            password=hashed_password
        )

        dao.add(user)
        dao.commit()
        return {"status": 200, "msg": "Пользователь успешно создан!"}

    except Exception as e:
        print(e)
        return {"status": 400, "msg": "Что-то пошло не так."}


@app.post("/login")
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    hashed_password = hashpw(password.encode("utf-8"), gensalt())
    return {"status": "ok"}


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
