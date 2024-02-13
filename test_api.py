import pytest
import requests


HOST_NAME = 'https://reqres.in'
USER_NAME = 'test name'
USER_JOB = 'test job'
VALID_PAYLOAD_REGISTRATION_AUTHORIZATION = {
    "email": "eve.holt@reqres.in",
    "password": "test"
}
PAYLOAD_WITHOUT_PASSWORD = {
    "email": "eve.holt@reqres.in"
}


@pytest.fixture(scope="function")
def user():
    payload = {
        "name": USER_NAME,
        "job": USER_JOB
    }
    response = requests.post(f'{HOST_NAME}/api/users', json=payload)
    yield response
    requests.delete(f'{HOST_NAME}/api/users/{response.json()["id"]}')


def test_get_information_single_user():
    user_id = 2
    response = requests.get(f'{HOST_NAME}/api/users/{user_id}')
    assert response.json()['data']['id'] == 2
    assert response.status_code == 200


def test_get_information_single_user_not_found():
    user_id = 0
    response = requests.get(f'{HOST_NAME}/api/users/{user_id}')
    assert response.json() == {}
    assert response.status_code == 404


def test_post_create_user(user):
    response_data = user.json()
    assert response_data['name'] == USER_NAME
    assert response_data['job'] == USER_JOB
    assert user.status_code == 201


def test_put_information_single_user(user):
    new_user_name = 'new test name'
    new_user_job = 'new test job'
    payload = {
        "name": new_user_name,
        "job": new_user_job
    }
    response = requests.put(f'{HOST_NAME}/api/users/{user.json()["id"]}', json=payload)
    response_data = response.json()
    assert response_data['name'] == new_user_name
    assert response_data['job'] == new_user_job
    assert response.status_code == 200


def test_delete_single_user(user):
    response = requests.delete(f'{HOST_NAME}/api/users/{user.json()["id"]}')
    assert response.text == ''
    assert response.status_code == 204


def test_get_list_users():
    page_number = 2
    response = requests.get(f'{HOST_NAME}/api/users?page={page_number}')
    response_data = response.json()
    assert response_data['page'] == page_number
    assert len(response_data['data']) == response_data['per_page']
    assert response.status_code == 200


def test_post_register_successful():
    response = requests.post(
        f'{HOST_NAME}/api/register',
        json=VALID_PAYLOAD_REGISTRATION_AUTHORIZATION
    )
    response_data = response.json()
    assert 'id' in response_data
    assert 'token' in response_data
    assert response.status_code == 200


def test_post_register_unsuccessful_password():
    response = requests.post(f'{HOST_NAME}/api/register', json=PAYLOAD_WITHOUT_PASSWORD)
    assert response.json()['error'] == 'Missing password'
    assert response.status_code == 400


def test_post_login_successful():
    response = requests.post(
        f'{HOST_NAME}/api/login',
        json=VALID_PAYLOAD_REGISTRATION_AUTHORIZATION
    )
    assert 'token' in response.json()
    assert response.status_code == 200


def test_post_login_unsuccessful_password():
    response = requests.post(f'{HOST_NAME}/api/login', json=PAYLOAD_WITHOUT_PASSWORD)
    assert response.json()['error'] == 'Missing password'
    assert response.status_code == 400
