import requests
from os import environ


class Api:
    @staticmethod
    def post(address: str, data):
        print(data)
        res = requests.post(f"http://{environ['API_URL']}{address}", json=data)
        return res.json()

    @staticmethod
    def get(address: str, data):
        res = requests.get(f"http://{environ['API_URL']}{address}", json=data)
        return res.json()