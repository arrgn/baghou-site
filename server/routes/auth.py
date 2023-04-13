import re
from datetime import datetime, timezone, timedelta
from os import environ

import jwt
from bcrypt import hashpw, checkpw
from flask import request

from server import app, salt
from server.data.__all_models import User, Token
from server.data.db_session import create_session


@app.post("/reg")
def reg():
    try:
        username = request.json["username"]
        email = request.json["email"]
        password = request.json["password"]
        hashed_password = hashpw(password.encode("utf-8"), salt).decode("utf-8")

        # check email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return {"status": 400, "msg": "Некорректный адрес электронной почты"}

        # get data access object
        dao = create_session()

        # check for user with the same email
        if dao.query(User).filter(User.email == email).first():
            return {"status": 400, "msg": "Пользователь с такой почтой уже существует!"}

        # create user
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
        return {"status": 500, "msg": "Что-то пошло не так."}


@app.post("/login")
def login():
    try:
        email = request.json["email"]
        password = request.json["password"]

        # get data access object
        dao = create_session()

        # check user exists
        user = dao.query(User).filter(User.email == email).first()
        if not user:
            return {"status": 400, "msg": "Пользователь не найден!"}

        # check password
        if not checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
            return {"status": 400, "msg": "Неверный логин или пароль!"}

        # generate tokens:
        # refresh exists fot 30 days; access - for 30 minutes
        payload = {"id": user.id}
        refresh_time = datetime.now(tz=timezone.utc) + timedelta(days=30)
        access_time = datetime.now(tz=timezone.utc) + timedelta(minutes=30)
        refresh_token = jwt.encode({"exp": refresh_time, "data": payload}, environ["SECRET_REFRESH_KEY"],
                                   algorithm="HS256")
        access_token = jwt.encode({"exp": access_time, "data": payload}, environ["SECRET_ACCESS_KEY"],
                                  algorithm="HS256")

        # save refresh token to database or update it if it already exists
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
        return {"status": 500, "msg": "Что-то пошло не так."}
