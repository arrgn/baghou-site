import re
from datetime import datetime, timezone, timedelta
from os import environ

import jwt
from bcrypt import hashpw, checkpw
from flask import request

from server import app, salt
from server.data.__all_models import User, Token
from server.data.db_session import create_session


class UserService:
    @staticmethod
    @app.post("/auth/reg")
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

    @staticmethod
    @app.post("/auth/login")
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
            tokens = UserService.generate_tokens(payload)

            # save refresh token to database or update it if it already exists
            token = dao.query(Token).filter(Token.user_id == user.id).first()
            if token:
                token.refresh_token = tokens["refresh_token"]
            else:
                token = Token(user_id=user.id, refresh_token=tokens["refresh_token"])
            dao.add(token)
            dao.commit()

            return {"status": 200, "msg": "Вы успешно вошли в аккаунт!", **tokens}

        except Exception as e:
            print(e)
            return {"status": 500, "msg": "Что-то пошло не так."}

    @staticmethod
    @app.get("/auth/refresh")
    def refresh_access_token():
        try:
            refresh_token = None
            if "refresh_token" in request.cookies:
                refresh_token = request.cookies["refresh_token"]
            if not refresh_token:
                return {"status": 401, "msg": "Пользователь не авторизован!"}

            old_user_data = jwt.decode(refresh_token, environ["SECRET_REFRESH_KEY"], algorithms=["HS256"])["data"]

            dao = create_session()

            token_from_db = dao.query(Token).filter(Token.refresh_token == refresh_token).first()

            if not token_from_db:
                return {"status": 401, "msg": "Пользователь не авторизован!"}

            payload = {"id": old_user_data["id"]}
            tokens = UserService.generate_tokens(payload)
            token_from_db.refresh_token = tokens["refresh_token"]
            dao.add(token_from_db)
            dao.commit()

            return {"status": 200, "msg": "Доступ успешно получен", **tokens}

        except jwt.ExpiredSignatureError:
            return {"status": 401, "msg": "Пользователь не авторизован!"}
        except Exception as e:
            print(e)
            return {"status": 500, "msg": "Что-то пошло не так!"}

    @staticmethod
    def generate_tokens(payload):
        # generate tokens:
        # refresh exists fot 30 days; access - for 30 minutes
        refresh_time = datetime.now(tz=timezone.utc) + timedelta(days=30)
        access_time = datetime.now(tz=timezone.utc) + timedelta(minutes=30)
        refresh_token = jwt.encode({"exp": refresh_time, "data": payload}, environ["SECRET_REFRESH_KEY"],
                                   algorithm="HS256")
        access_token = jwt.encode({"exp": access_time, "data": payload}, environ["SECRET_ACCESS_KEY"],
                                  algorithm="HS256")

        return {"refresh_token": refresh_token, "access_token": access_token}
