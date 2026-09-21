import requests
from jsonschema import validate

from schemas.auth_schema import (
    invalid_credentials_schema,
    success_auth,
    unsupported_media_type,
    wrong_credentials_auth,
)
from utils.http_client import REQUEST_TIMEOUT
from utils.jwt_helpers import decode_jwt_payload

AUTH_PATH = "/auth/token/"


def test_successful_auth(base_url, user):
    request_body = {"username": user["username"], "password": user["password"]}

    response = requests.post(f"{base_url}{AUTH_PATH}", json=request_body, timeout=REQUEST_TIMEOUT)

    assert response.status_code == 200, response.text

    body = response.json()
    validate(body, schema=success_auth)

    access_token = body["access"]
    refresh_token = body["refresh"]
    assert access_token != refresh_token

    access_payload = decode_jwt_payload(access_token)
    refresh_payload = decode_jwt_payload(refresh_token)
    assert access_payload["token_type"] == "access"
    assert refresh_payload["token_type"] == "refresh"
    assert access_payload["user_id"] == user["id"]
    assert refresh_payload["user_id"] == user["id"]


def test_wrong_credentials_auth(base_url, user):
    request_body = {"username": user["username"], "password": "wrong"}

    response = requests.post(f"{base_url}{AUTH_PATH}", json=request_body, timeout=REQUEST_TIMEOUT)

    assert response.status_code == 401, response.text

    body = response.json()
    validate(body, schema=wrong_credentials_auth)

    assert body["detail"] == "Invalid username or password."


def test_nonexistent_user_auth(base_url, new_credentials):
    response = requests.post(f"{base_url}{AUTH_PATH}", json=new_credentials, timeout=REQUEST_TIMEOUT)

    assert response.status_code == 401, response.text

    body = response.json()
    validate(body, schema=wrong_credentials_auth)

    assert body["detail"] == "Invalid username or password."


def test_missing_username_auth(base_url, new_credentials):
    request_body = {"password": new_credentials["password"]}

    response = requests.post(f"{base_url}{AUTH_PATH}", json=request_body, timeout=REQUEST_TIMEOUT)

    assert response.status_code == 400, response.text

    body = response.json()
    validate(body, schema=invalid_credentials_schema)

    assert body["username"] == ["This field is required."]


def test_missing_password_auth(base_url, new_credentials):
    request_body = {"username": new_credentials["username"]}

    response = requests.post(f"{base_url}{AUTH_PATH}", json=request_body, timeout=REQUEST_TIMEOUT)

    assert response.status_code == 400, response.text

    body = response.json()
    validate(body, schema=invalid_credentials_schema)

    assert body["password"] == ["This field is required."]


def test_wrong_body_type_boolean(base_url):
    request_body = {"username": True, "password": False}

    response = requests.post(f"{base_url}{AUTH_PATH}", json=request_body, timeout=REQUEST_TIMEOUT)

    assert response.status_code == 400, response.text

    body = response.json()
    validate(body, schema=invalid_credentials_schema)

    assert body["username"] == ["Not a valid string."]
    assert body["password"] == ["Not a valid string."]


def test_wrong_content_type_auth(base_url, new_credentials):
    headers = {"content-type": "image/png"}

    response = requests.post(f"{base_url}{AUTH_PATH}", headers=headers, json=new_credentials, timeout=REQUEST_TIMEOUT)

    assert response.status_code == 415, response.text

    body = response.json()
    validate(body, schema=unsupported_media_type)

    assert body["detail"] == 'Unsupported media type "image/png" in request.'
