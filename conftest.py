import pytest
import requests
import allure
import random
from helpers import DataGenerator


class ApiClient:
    # TODO:  Res|Req logger
    def __init__(self, base_address):
        self.base_address = base_address

    def post(self, path="/", params=None, data=None, json=None, headers=None):
        url = f"{self.base_address}{path}"
        with allure.step(f'POST request to: {url}'):
            response = requests.post(url=url, params=params, data=data, json=json, headers=headers)
            with allure.step(response.text):
                pass
            return response


    def get(self, path="/", params=None, headers=None):
        url = f"{self.base_address}{path}"
        with allure.step(f'GET request to: {url}'):
            response = requests.get(url=url, params=params, headers=headers)
            with allure.step(response.text):
                pass
            return response

    def put(self, path="/", params=None, data=None, json=None, headers=None):
        url = f"{self.base_address}{path}"
        with allure.step(f'PUT request to: {url}'):
            response = requests.put(url=url, params=params, data=data, json=json, headers=headers)
            with allure.step(response.text):
                pass
            return response

    def delete(self, path="/", params=None, headers=None):
        url = f"{self.base_address}{path}"
        with allure.step(f'DELETE request to: {url}'):
            response = requests.delete(url=url, params=params, headers=headers)
            with allure.step(response.text):
                pass
            return response

@pytest.fixture
def alaska_api():
    return ApiClient(base_address="http://0.0.0.0:8091/")

@pytest.fixture
def bear_item():
    alaska_api = ApiClient(base_address="http://0.0.0.0:8091/")

    # bear_type = ['POLAR', 'BROWN', 'BLACK', 'GUMMY']
    bear_types = ['POLAR', 'BROWN', 'BLACK'] # bug on create GUMMY bear
    bear_type = random.choice(bear_types)

    data = {'bear_type': bear_type, 'bear_name': DataGenerator.bear_name(), 'bear_age': DataGenerator.bear_age()}
    response = alaska_api.post("bear", json=data)
    with allure.step(f"Check created bear [{bear_type}]"):
        assert response.status_code == 200, f"Invalid status code: {response.status_code}"
        bear_id = response.json()
        assert isinstance(bear_id, int), f"Invalid response id: {bear_id}"
    data['bear_id'] = bear_id
    return data
