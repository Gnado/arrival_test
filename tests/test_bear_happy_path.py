import pytest
import allure
from helpers import DataGenerator

@allure.feature('Happy path')
@allure.story('Get bear items')
def test_get_bear(alaska_api, bear_item):
    response = alaska_api.get("bear")
    assert response.status_code == 200, f"Invalid status code: {response.status_code}"
    res = response.json()
    assert isinstance(res, list), "Invalid format"
    assert len(res) > 0, "Data base is empty"
    at_bear = None
    for item in res:
        if item['bear_id'] == bear_item['bear_id']:
            at_bear = item
    assert at_bear is not None, f"Bear id {bear_item['bear_id']} is not found"
    #TODO: check any field

@allure.feature('Happy path')
@allure.story('Create bear item')
@pytest.mark.parametrize("bear_type", [
    "POLAR",
    "BROWN",
    "BLACK",
    "GUMMY"
])
def test_create_bear(alaska_api, bear_type):
    with allure.step("Create bear item"):
        bear = {'bear_type': bear_type, 'bear_name': DataGenerator.bear_name(), 'bear_age': DataGenerator.bear_age()}
        response = alaska_api.post("bear", json=bear)

        assert response.status_code == 200, f"Invalid status code: {response.status_code}"
        bear_id = response.json()
        assert isinstance(bear_id, int), f"Invalid response id: {bear_id}"
    bear['bear_id'] = bear_id

    response = alaska_api.get(f"bear/{bear_id}")
    with allure.step("Check creation bear item"):
        assert response.status_code == 200, f"Invalid status code: {response.status_code}"
        assert response.text != 'EMPTY', f"Bear id {bear_id} is EMPTY"
        response = response.json()
        assert isinstance(response, dict), "Invalid format"
        assert response == bear, f"Invalid bear data"

@allure.feature('Happy path')
@allure.story('Update bear item')
@pytest.mark.parametrize("bear_type", [
    "POLAR",
    "BROWN",
    "BLACK",
    "GUMMY"
])
def test_update_bear(alaska_api, bear_type, bear_item):
    # TODO: to exclude duplicates bear_type
    update_bear = {'bear_type': bear_type, 'bear_name': DataGenerator.bear_name(), 'bear_age': DataGenerator.bear_age()}
    response = alaska_api.put(f"bear/{bear_item['bear_id']}", json=update_bear)
    assert response.status_code == 200, f"Invalid status code: {response.status_code}"
    assert response.text == 'OK', "The update was not successful"

    update_bear['bear_id'] = bear_item['bear_id']

    with allure.step("Check update data"):
        response = alaska_api.get(f"bear/{bear_item['bear_id']}")
        assert response.status_code == 200, f"Invalid status code: {response.status_code}"
        res = response.json()
        assert isinstance(res, dict), "Invalid format"
        assert res == update_bear, f"Invalid bear data"

@allure.feature('Happy path')
@allure.story('Delete bear item')
def test_delete_bear(alaska_api, bear_item):
    response = alaska_api.delete(f"bear/{bear_item['bear_id']}")
    assert response.status_code == 200, f"Invalid status code: {response.status_code}"
    with allure.step("Check delete data"):
        response = alaska_api.get(f"bear/{bear_item['bear_id']}")
        assert response.status_code == 200, f"Invalid status code: {response.status_code}"
        assert response.text == 'EMPTY', "The delete was not successful"

@allure.feature('Happy path')
@allure.story('Delete all bear items')
def test_delete_all_bear(alaska_api, bear_item):
    with allure.step("Delete bear item"):
        response = alaska_api.delete("bear")
        assert response.status_code == 200, f"Invalid status code: {response.status_code}"
    with allure.step("Check delete data"):
        response = alaska_api.get("bear")
        res = response.json()
        assert isinstance(res, list), "Invalid format"
        assert len(res) == 0, "Data base is not empty"
