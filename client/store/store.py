from flask import make_response, redirect, request

from client.services.auth_service import AuthService
from client.services.user_service import UserService


class Store:
    def __init__(self):
        self.user = {"gtag": None}
        self.is_auth = False

    def set_auth(self, value: bool):
        self.is_auth = value

    def set_user(self, value):
        self.user = value

    def login(self, email: str, password: str):
        res = AuthService.login(email, password)
        response = make_response(redirect("/"))
        response.set_cookie("access_token", res["access_token"], max_age=30 * 60 * 60 * 24)
        user = res["user"]
        u_name, u_id = UserService.parse_gtag_api(user["gtag"])
        user["name"] = u_name
        user["id"] = u_id
        print(user)
        self.set_user(user)
        return response

    def registration(self, username: str, email: str, password: str):
        res = AuthService.registration(email, username, password)
        response = make_response(redirect("/auth/login"))
        return response

    def logout(self):
        self.set_user({"gtag": "none#0"})
        response = make_response(redirect("/"))
        response.set_cookie("access_token", "", expires=0)
        return response

    def check_auth(self):
        if "access_token" in request.cookies:
            self.set_auth(True)
        else:
            self.set_auth(False)

    def get_user_by_gtag(self, gtag):
        res = UserService.get_user_by_gtag(gtag)
        return res