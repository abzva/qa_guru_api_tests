import pytest
import requests
from jsonschema import validate

from schemas.error_schema import validation_error_schema
from schemas.user_schema import user_schema
from utils.data import password_of_length, username_of_length
from utils.http_client import REQUEST_TIMEOUT

REGISTER_PATH = "/users/register/"
AUTH_PATH = "/auth/token/"
ME_PATH = "/users/me/"

VALID_PASSWORD = "P@ssw0rd123"


def test_successful_registration(register_user, new_credentials):
    response = register_user(new_credentials)

    assert response.status_code == 201, response.text

    body = response.json()
    validate(body, schema=user_schema)

    assert body["username"] == new_credentials["username"]
    assert body["id"] > 0
    assert body["firstName"] == ""
    assert body["lastName"] == ""
    assert body["email"] == ""
    assert "password" not in body, "Пароль не должен возвращаться в ответе"


def test_registered_user_can_authenticate(base_url, register_user, new_credentials):
    response = register_user(new_credentials)
    assert response.status_code == 201, response.text
    registered = response.json()

    response = requests.post(f"{base_url}{AUTH_PATH}", json=new_credentials, timeout=REQUEST_TIMEOUT)
    assert response.status_code == 200, response.text
    access_token = response.json()["access"]

    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{base_url}{ME_PATH}", headers=headers, timeout=REQUEST_TIMEOUT)
    assert response.status_code == 200, response.text

    body = response.json()
    assert body["id"] == registered["id"]
    assert body["username"] == new_credentials["username"]


def test_registration_with_existing_username(base_url, user):
    request_body = {"username": user["username"], "password": "AnotherP@ssw0rd"}

    response = requests.post(f"{base_url}{REGISTER_PATH}", json=request_body, timeout=REQUEST_TIMEOUT)

    assert response.status_code == 400, response.text

    body = response.json()
    validate(body, schema=validation_error_schema)

    assert body["username"] == ["A user with that username already exists."]


@pytest.mark.parametrize(
    "request_body, expected_errors",
    [
        (
            {"username": "qa_missing_password"},
            {"password": ["This field is required."]},
        ),
        (
            {"password": VALID_PASSWORD},
            {"username": ["This field is required."]},
        ),
        (
            {"username": "", "password": VALID_PASSWORD},
            {"username": ["This field may not be blank."]},
        ),
        (
            {"username": "qa invalid name", "password": VALID_PASSWORD},
            {"username": [
                "Enter a valid username. "
                "This value may contain only letters, numbers, and @/./+/-/_ characters."
            ]},
        ),
    ],
    ids=[
        "no_password",
        "no_username",
        "blank_username",
        "username_with_space",
    ],
)
def test_registration_validation_errors(base_url, request_body, expected_errors):
    response = requests.post(f"{base_url}{REGISTER_PATH}", json=request_body, timeout=REQUEST_TIMEOUT)

    assert response.status_code == 400, response.text

    body = response.json()
    validate(body, schema=validation_error_schema)

    assert body == expected_errors


def test_registration_accepts_boundary_lengths(register_user):
    credentials = {
        "username": username_of_length(150),
        "password": password_of_length(16),
    }

    response = register_user(credentials)

    assert response.status_code == 201, response.text

    body = response.json()
    validate(body, schema=user_schema)

    assert body["username"] == credentials["username"]


def test_registration_rejects_too_long_values(base_url):
    request_body = {
        "username": username_of_length(151),
        "password": password_of_length(16),
    }

    response = requests.post(f"{base_url}{REGISTER_PATH}", json=request_body, timeout=REQUEST_TIMEOUT)

    assert response.status_code == 400, response.text

    body = response.json()
    validate(body, schema=validation_error_schema)

    assert body == {"username": ["Ensure this field has no more than 150 characters."]}
