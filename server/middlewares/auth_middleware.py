from functools import wraps
from os import environ

import jwt
from flask import make_response
from flask import request

from server.data.__all_models import User
from server.data.db_session import create_session
from server.loggers import logger


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # get token from request
        access_token = None
        if "Authorization" in request.headers:
            access_token = request.headers["Authorization"].split(" ")[1]

        # return error if token wasn't found
        if not access_token:
            res = make_response({"msg": "Пользователь не авторизован!"})
            res.status = 401
            return res
        try:
            # get data from token
            data = jwt.decode(access_token, environ["SECRET_ACCESS_KEY"], algorithms=["HS256"])["data"]

            # data access object
            dao = create_session()

            # get user by id; if not found - return an error
            user = dao.query(User).filter(User.id == data["id"]).first()
            if not user:
                res = make_response({"msg": "Пользователь не найден!"})
                res.status = 400
                return res

        # check if access token is alive
        except jwt.ExpiredSignatureError:
            res = make_response({"msg": "Пользователь не авторизован!"})
            res.status = 401
            return res
        except Exception as e:
            logger.exception(e)
            res = make_response({"msg": "Что-то пошло не так."})
            res.status = 500
            return res

        return f(user, *args, **kwargs)

    return decorated
