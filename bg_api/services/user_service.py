import re
from datetime import datetime, timezone, timedelta
from os import environ
from typing import Any

import jwt
from bcrypt import hashpw, checkpw
from flask import request, make_response, abort, Response

from bg_api import salt
from bg_api.data.__all_models import User, Token, Follower
from bg_api.data.db_session import create_session


class UserService:
    @staticmethod
    def reg() -> Response:
        """
        Registrate user.

        :return: None.
        """

        # get user data
        username = request.json["username"]
        email = request.json["email"]
        password = request.json["password"]
        hashed_password = hashpw(password.encode("utf-8"), salt).decode("utf-8")

        # check email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            abort(400, {"msg": "Некорректный адрес электронной почты"})

        # get data access object
        with create_session() as dao:
            # check for user with the same email
            if dao.query(User).filter(User.email == email).first():
                abort(400, {"msg": "Пользователь с такой почтой уже существует!"})

            # create user
            user = User(
                name=username,
                email=email,
                password=hashed_password
            )

            dao.add(user)
            dao.commit()

        res = make_response({"msg": "Пользователь успешно создан!"})

        return res

    @staticmethod
    def login() -> Response:
        """
        Login user.

        :return: Access token.
        """

        # get user data
        email = request.json["email"]
        password = request.json["password"]

        # get data access object
        with create_session() as dao:
            # check user exists
            user = dao.query(User).filter(User.email == email).first()
            if not user:
                abort(400, {"msg": "Пользователь не найден!"})

            # check password
            if not checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
                abort(400, {"msg": "Неверный логин или пароль!"})

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

        res = make_response({"msg": "Вы успешно вошли в аккаунт!", "access_token": tokens["access_token"]})
        # set cookie for 30 days
        res.set_cookie("refresh_token", tokens["refresh_token"], max_age=30 * 24 * 60 * 60, httponly=True)

        return res

    @staticmethod
    def refresh_access_token() -> Response:
        """
        Generate new access token and return to the client.

        :return: Access token.
        """

        # get refresh token
        refresh_token = None
        if "refresh_token" in request.cookies:
            refresh_token = request.cookies["refresh_token"]
        if not refresh_token:
            abort(401, {"msg": "Пользователь не авторизован!"})

        # get user data from token from request
        old_user_data = jwt.decode(refresh_token, environ["SECRET_REFRESH_KEY"], algorithms=["HS256"])["data"]

        with create_session() as dao:
            # get token from db
            token_from_db = dao.query(Token).filter(Token.refresh_token == refresh_token).first()

            # check for existing token in db
            if not token_from_db:
                abort(401, {"msg": "Пользователь не авторизован!"})

            # update tokens & save to db
            payload = {"id": old_user_data["id"]}
            tokens = UserService.generate_tokens(payload)
            token_from_db.refresh_token = tokens["refresh_token"]

            dao.add(token_from_db)
            dao.commit()

        res = make_response({"msg": "Доступ успешно получен!", "access_token": tokens["access_token"]})
        # set refresh token expiration to 30 days
        res.set_cookie("refresh_token", tokens["refresh_token"], max_age=30 * 24 * 60 * 60, httponly=True)

        return res

    @staticmethod
    def get_profile_data(gtag: str) -> Response:
        """
        Return user data.

        :param gtag: Gtag.
        :return: User data.
        """

        # get user
        user = UserService.get_user(gtag)

        res = make_response({
            "gtag": f"{user.name}#{user.id}",
            "bio": user.bio,
            "rating": user.rating,
            "avatar": user.avatar
        })

        return res

    @staticmethod
    def get_users_by_name() -> Response:
        """
        Search for users with the name and return them.

        :return: List of users.
        """

        # get username
        username = request.args["q"]

        with create_session() as dao:
            # get all users
            users = dao.query(User).filter(User.name == username).all()

        res = make_response(list(map(lambda user: {
            "gtag": f"{user.name}#{user.id}",
            "avatar": user.avatar
        }, users)))

        return res

    @staticmethod
    def follow(user: User) -> Response:
        """
        Follow user.

        :param user: Follower.
        :return: None.
        """

        # get target (followed)
        gtag = request.json["gtag"]
        target = UserService.get_user(gtag)

        with create_session() as dao:
            # follow
            following_row = Follower(follower_id=user.id, followed_id=target.id)

            dao.add(following_row)
            dao.commit()

        res = make_response({"msg": f"Вы успешно подписались на пользователя {gtag}!"})

        return res

    @staticmethod
    def unfollow(user: User) -> Response:
        """
        Unfollow user.

        :param user: Follower.
        :return: None.
        """

        # get target (followed)
        gtag = request.json["gtag"]
        target = UserService.get_user(gtag)

        with create_session() as dao:
            # get data about following that must be deleted
            following_row = dao.query(Follower).filter(Follower.follower_id == user.id,
                                                       Follower.followed_id == target.id).first()

            dao.delete(following_row)
            dao.commit()

        res = make_response({"msg": f"Вы успешно отписались от пользователя {gtag}!"})

        return res

    @staticmethod
    def get_followers(gtag: str):
        """
        Get a follower list of user.

        :param gtag: Gtag.
        :return: List of followers.
        """

        # get followed user
        user = UserService.get_user(gtag)

        with create_session() as dao:
            # get followers
            followers = dao.query(User).join(Follower, Follower.follower_id == User.id).filter(
                Follower.followed_id == user.id).all()

        res = make_response(list(map(lambda follower: {
            "gtag": f"{follower.name}#{follower.id}",
            "avatar": follower.avatar
        }, followers)))

        return res

    @staticmethod
    def generate_tokens(payload: Any) -> dict[str, str]:
        """
        Generate access and refresh token from payload.

        :param payload: Some data.
        :return: Access and refresh token.
        """

        # generate expiration time
        # refresh exists for 30 days; access - for 30 minutes
        refresh_time = datetime.now(tz=timezone.utc) + timedelta(days=30)
        access_time = datetime.now(tz=timezone.utc) + timedelta(minutes=30)
        # generate tokens
        refresh_token = jwt.encode({"exp": refresh_time, "data": payload}, environ["SECRET_REFRESH_KEY"],
                                   algorithm="HS256")
        access_token = jwt.encode({"exp": access_time, "data": payload}, environ["SECRET_ACCESS_KEY"],
                                  algorithm="HS256")

        return {"refresh_token": refresh_token, "access_token": access_token}

    @staticmethod
    def parse_gtag(gtag: str) -> tuple[str, int]:
        """
        Parse gtag in name and id.

        :param gtag: Gtag.
        :return: Username and user's id.
        """

        # end of tag's name
        eot = gtag.rfind("-")
        username = gtag[:eot]
        user_id = int(gtag[eot + 1:])

        return username, user_id

    @staticmethod
    def get_user(gtag) -> User:
        """
        Get user from database.

        :param gtag: Gtag.
        :return: User.
        """

        # parse gtag
        username, user_id = UserService.parse_gtag(gtag)

        with create_session() as dao:
            user = dao.query(User).filter(User.id == user_id, User.name == username).first()
            if not user:
                abort(400, {"msg": f"пользователь {gtag} не найден"})

        # noinspection PyTypeChecker
        return user
