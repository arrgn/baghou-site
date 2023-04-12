import datetime
import sys
import traceback
import logging.config
import re
import jwt

from flask import Flask, request
from bcrypt import hashpw, checkpw

from server import salt
from config import config
from loggers import logger
from server.funcs.path_module import path_to_file, create_dir
from data.db_session import create_session, global_init
from data.__all_models import User, Token
from os import environ

app = Flask(__name__)

global_init()


@app.post("/reg")
def reg():
    try:
        username = request.json["username"]
        email = request.json["email"]
        password = request.json["password"]
        hashed_password = hashpw(password.encode("utf-8"), salt).decode("utf-8")

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return {"status": 400, "msg": "Некорректный адрес электронной почты"}

        dao = create_session()

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
    try:
        email = request.json["email"]
        password = request.json["password"]

        dao = create_session()

        user = dao.query(User).filter(User.email == email).first()
        if not user:
            return {"status": 400, "msg": "Пользователь не найден!"}

        if not checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
            return {"status": 400, "msg": "Неверный логин или пароль!"}

        payload = {"id": user.id}
        refresh_time = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=30)
        access_time = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=30)
        refresh_token = jwt.encode({"exp": refresh_time, "data": payload}, environ["SECRET_REFRESH_KEY"],
                                   algorithm="HS256")
        access_token = jwt.encode({"exp": access_time, "data": payload}, environ["SECRET_ACCESS_KEY"],
                                  algorithm="HS256")

        token = dao.query(Token).filter(Token.user_id == user.id).first()
        if token:
            token.refresh_token = refresh_token
        else:
            token = Token(user_id=user.id, refresh_token=refresh_token)
        dao.add(token)
        dao.commit()

        return {"status": 200, "msg": "Вы успешно вошли в аккаунт!", "refresh_token": refresh_token,
                "access_token": access_token}

    except Exception as e:
        print(e)
        return {"status": 400, "msg": "Что-то пошло не так."}


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
