from client.http.api import Api


class UserService:
    @staticmethod
    def get_user_by_gtag(gtag: str):
        name, id = UserService.parse_gtag_client(gtag)
        res = Api.get(f"/players/profile/{name}-{id}")

        return res

    @staticmethod
    def parse_gtag_api(gtag: str):
        eot = gtag.rfind("#")
        username = gtag[:eot]
        user_id = gtag[eot + 1:]

        return username, user_id

    @staticmethod
    def parse_gtag_client(gtag: str):
        eot = gtag.rfind("-")
        username = gtag[:eot]
        user_id = gtag[eot + 1:]

        return username, user_id
