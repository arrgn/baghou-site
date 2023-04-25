from flask import make_response, redirect

from client.forms.login_form import LoginForm
from client.services.auth_service import AuthService


class Store:
    def __init__(self):
        self.user = {}
        self.is_auth = False

    def set_auth(self, value: bool):
        self.is_auth = value

    def set_user(self, value):
        self.user = value

    def login(self, email: str, password: str):
        res = AuthService.login(email, password)
        response = make_response(redirect("/"))
        response.set_cookie("access_token", res["access_token"])
        self.set_auth(True)
        return response

    def registration(self, username: str, email: str, password: str):
        res = AuthService.registration(email, username, password)
        response = make_response(redirect("/auth/login"))
        return response

    def logout(self):
        pass
