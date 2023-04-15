from functools import wraps
from os import environ

import jwt
from flask import request

from server.data.__all_models import User
from server.data.db_session import create_session


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # get token from request
        access_token = None
        if "Authorization" in request.headers:
            access_token = request.headers["Authorization"].split(" ")[1]

        # return error if token wasn't found
        if not access_token:
            return {"status": 401, "msg": "Пользователь не авторизован!"}
        try:
            # get data from token
            data = jwt.decode(access_token, environ["SECRET_ACCESS_KEY"], algorithms=["HS256"])["data"]

            # data access object
            dao = create_session()

            # get user by id; if not found - return an error
            user = dao.query(User).filter(User.id == data["id"]).first()
            if not user:
                return {"status": 400, "msg": "Пользователь не найден!"}

        # check if access token is alive
        except jwt.ExpiredSignatureError:
            return {"status": 401, "msg": "Пользователь не авторизован!"}
        except Exception as e:
            print(e)
            return {"status": 500, "msg": "Что-то пошло не так."}

        return f(user, *args, **kwargs)

    return decorated
