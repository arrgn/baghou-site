from flask import make_response, redirect, request

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
        user = res["user"]
        u_name, u_id = self.parse_gtag(user["gtag"])
        user["name"] = u_name
        user["id"] = u_id
        self.set_user(user)
        print(self.user)
        return response

    def registration(self, username: str, email: str, password: str):
        res = AuthService.registration(email, username, password)
        response = make_response(redirect("/auth/login"))
        return response

    def logout(self):
        self.set_user({})
        # res = AuthService.logout()
        response = make_response(redirect("/"))
        response.set_cookie("access_token", "", expires=0)
        return response

    def check_auth(self):
        if "access_token" in request.cookies:
            self.set_auth(True)
        else:
            self.set_auth(False)

    def get_user_by_gtag(self, gtag):
        pass

    def parse_gtag(self, gtag: str):
        eot = gtag.rfind("#")
        username = gtag[:eot]
        user_id = gtag[eot + 1:]

        return username, user_id
