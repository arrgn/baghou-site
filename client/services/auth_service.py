from client.http.api import Api


class AuthService:
    @staticmethod
    def login(email: str, password: str):
        return Api.post("/auth/login", {"email": email, "password": password})

    @staticmethod
    def registration(email: str, username: str, password: str):
        return Api.post("/auth/reg", {"email": email, "username": username, "password": password})

    @staticmethod
    def logout():
        return Api.post("/auth/logout")