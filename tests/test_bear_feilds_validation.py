from json import JSONDecodeError

import pytest
import allure

from helpers import DataGenerator


@allure.feature('Bear fields validation')
@allure.story('Validation empty fields')
@pytest.mark.parametrize("body", [
    {'bear_name': 'TEST', 'bear_age': 11.5},
    {'bear_type': 'POLAR', 'bear_age': 11.5},
    {'bear_type': 'POLAR', 'bear_name': 'TEST'},
    {'bear_type': 'POLAR'},
    {'bear_name': 'TEST'},
    {'bear_age': 11.5}
])
def test_validation_empty_field(alaska_api, body):
    with allure.step("Try create bear item"):
        response = alaska_api.post("bear", json=body)
        # assert response.status_code != 200, f"Invalid status code {response.status_code}" #TODO: clarify what the code should be
        #assert response.text == 'Error. Pls fill all parameters', f"Invalid response: {response.text}"
        try:
            res = response.json()
            assert not isinstance(res, int), f"Item is created with id {response.text}"
        except JSONDecodeError:
            assert response.text == 'Error. Pls fill all parameters', f"Invalid response: {response.text}"


@allure.feature('Bear fields validation')
@allure.story('Validation wrong bear_name field')
@pytest.mark.parametrize("bear_name", [
    "",
    " ",
    "         ",
    "@#$%^&*"
    # "Hubert Blaine Wolfeschlegelsteinhausenbergerdorff Sr Hubert Blaine Wolfeschlegelsteinhausenbergerdorff Sr Hubert Blaine Wolfeschlegelsteinhausenbergerdorff Sr. Hubert Blaine Wolfeschlegelsteinhausenbergerdorff Sr."
    #TODO: Need more information
])
def test_validation_wrong_bear_name(alaska_api, bear_name):
    with allure.step("Try create bear_item"):
        body = {'bear_type': 'POLAR', 'bear_name': bear_name, 'bear_age': 12.5}
        response = alaska_api.post("bear", json=body)
        # assert response.status_code != 200, f"Invalid status code {response.status_code}"
        try:
            res = response.json()
            assert not isinstance(res, int), f"Item is created with id {response.text}"
        except JSONDecodeError:
            assert not isinstance(response.text, int), f"Item is created with id {response.text}"

@allure.feature('Bear fields validation')
@allure.story('Validation right bear_name field')
@pytest.mark.parametrize("bear_name", [
    "Mike",
    "mike",
    "michael jackson",
    "MICHAEL",
    "MICHAEL_1",
    "Hubert Blaine Wolfeschlegelsteinhausenbergerdorff Sr."
    # TODO: max len?
])
def test_validation_right_bear_name(alaska_api, bear_name):
    with allure.step("Create bear item"):
        body = {'bear_type': 'BLACK', 'bear_name': bear_name, 'bear_age': 12.5}
        response = alaska_api.post("bear", json=body)
        # assert response.status_code != 200, f"Invalid status code {response.status_code}"
        try:
            res = response.json()
            assert isinstance(res, int), f"Bear item is not created {response.text}"
            body['bear_id'] = res
            body['bear_name'] = body['bear_name'].upper()
        except JSONDecodeError:
            assert not isinstance(response.text, int), f"Bear item is not created {response.text}"

    with allure.step("Check bear item"):
        response = alaska_api.get(f"bear/{body['bear_id']}")
        res = response.json()
        assert res == body, f"Invalid bear data"

@allure.feature('Bear fields validation')
@allure.story('Validation wrong bear_type field')
@pytest.mark.parametrize("bear_type", [
    "*",
    "",
    " ",
    ".*",
    "%",
    "POLAR%",
    "BROW%",
    "BLAC*",
    "GUM.*",
    "POLAR%",
    "%LAC%",
    "LAC",
    "LACK",
])
def test_validation_wrong_bear_type(alaska_api, bear_type):
    with allure.step("Try create bear item"):
        body = {'bear_type': bear_type, 'bear_name': 'TEST', 'bear_age': 9.5}
        response = alaska_api.post("bear", json=body)
        # assert response.status_code != 200, f"Invalid status code {response.status_code}"
        try:
            res = response.json()
            assert not isinstance(res, int), f"Item is created with id {response.text}"
        except JSONDecodeError:
            assert not isinstance(response.text, int), f"Item is created with id {response.text}"

@allure.feature('Bear fields validation')
@allure.story('Validation wrong bear_age field')
@pytest.mark.parametrize("bear_age", [
    "*",
    "",
    " ",
    ".*",
    "%",
    "AA",
    "bb",
    "?",
    "-1",
    "0",
    "0.0",
    "-1.0",
    "1,0"
    #TODO: max age?
])
def test_validation_wrong_bear_age(alaska_api, bear_age):
    with allure.step("Try create bear item"):
        body = {'bear_type': 'BLACK', 'bear_name': 'TEST', 'bear_age': bear_age}
        response = alaska_api.post("bear", json=body)
        # assert response.status_code != 200, f"Invalid status code {response.status_code}"
        try:
            res = response.json()
            assert not isinstance(res, int), f"Item is created with id {response.text}"
        except JSONDecodeError:
            assert not isinstance(response.text, int), f"Item is created with id {response.text}"

@allure.feature('Bear fields validation')
@allure.story('Validation right bear_age field')
@pytest.mark.parametrize("bear_age", [
    0.1,
    2.1,
    30.0,
    69.9,
    9999999999.9, #TODO: max value?
    0.1111,
    1,
    99
])
def test_validation_right_bear_age(alaska_api, bear_age):
    with allure.step("Create bear item"):
        body = {'bear_type': 'BLACK', 'bear_name': 'TEST', 'bear_age': bear_age}
        response = alaska_api.post("bear", json=body)
        # assert response.status_code != 200, f"Invalid status code {response.status_code}"
        try:
            res = response.json()
            assert isinstance(res, int), f"Bear item is not created {response.text}"
            body['bear_id'] = res
            body['bear_name'] = body['bear_name'].upper()
        except JSONDecodeError:
            assert not isinstance(response.text, int), f"Bear item is not created {response.text}"

    with allure.step("Check bear item"):
        response = alaska_api.get(f"bear/{body['bear_id']}")
        res = response.json()
        assert res == body, f"Invalid bear data"