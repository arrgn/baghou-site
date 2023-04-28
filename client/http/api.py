from os import environ

import requests
from flask import request


class Api:
    @staticmethod
    def post(address: str, data={}):
        if "access_token" in request.cookies:
            access_token = "BEARER " + request.cookies["access_token"]
            res = requests.post(f"http://{environ['API_URL']}{address}", json=data,
                                headers={"Authorization": access_token})
        else:
            res = requests.post(f"http://{environ['API_URL']}{address}", json=data)
        status_code = res.status_code
        response = res.json()
        response["status_code"] = status_code
        return response

    @staticmethod
    def get(address: str, data={}):
        if "access_token" in request.cookies:
            access_token = "BEARER " + request.cookies["access_token"]
            res = requests.get(f"http://{environ['API_URL']}{address}", json=data,
                               headers={"Authorization": access_token})
        else:
            res = requests.get(f"http://{environ['API_URL']}{address}", json=data)
        status_code = res.status_code
        response = res.json()
        response["status_code"] = status_code
        return response
