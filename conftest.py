import os

import pytest
import requests

from utils.data import make_club_payload, make_credentials
from utils.http_client import REQUEST_TIMEOUT, auth_header, build_session

DEFAULT_BASE_URL = "https://book-club.qa.guru/api/v1"


@pytest.fixture(scope="session")
def http():
    session = build_session()
    yield session
    session.close()


@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BOOK_CLUB_BASE_URL", DEFAULT_BASE_URL).rstrip("/")


def delete_user(http, base_url, credentials):
    try:
        response = http.post(f"{base_url}/auth/token/", json=credentials, timeout=REQUEST_TIMEOUT)
        if response.status_code != 200:
            return
        headers = {"Authorization": f"Bearer {response.json()['access']}"}
        http.delete(f"{base_url}/users/me/", headers=headers, timeout=REQUEST_TIMEOUT)
    except requests.RequestException:
        pass


@pytest.fixture
def new_credentials():
    return make_credentials()


@pytest.fixture
def register_user(http, base_url):
    """Фабрика регистрации: возвращает ответ API, созданные пользователи удаляются после теста."""
    registered = []

    def _register_user(credentials=None):
        credentials = credentials or make_credentials()
        response = http.post(f"{base_url}/users/register/", json=credentials, timeout=REQUEST_TIMEOUT)
        if response.status_code == 201:
            registered.append(credentials)
        return response

    yield _register_user

    for credentials in registered:
        delete_user(http, base_url, credentials)


@pytest.fixture
def create_user(http, base_url, register_user):
    """Фабрика готовых пользователей: регистрация плюс авторизация."""

    def _create_user(credentials=None):
        credentials = credentials or make_credentials()

        response = register_user(credentials)
        assert response.status_code == 201, f"Не удалось зарегистрировать пользователя: {response.text}"
        registered = response.json()

        response = http.post(f"{base_url}/auth/token/", json=credentials, timeout=REQUEST_TIMEOUT)
        assert response.status_code == 200, f"Не удалось авторизоваться: {response.text}"

        return {**credentials, "id": registered["id"], **response.json()}

    return _create_user


@pytest.fixture
def user(create_user):
    return create_user()


@pytest.fixture
def auth_headers(user):
    return auth_header(user)


@pytest.fixture
def club(http, base_url, auth_headers):
    """Клуб текущего пользователя. Уборка не нужна: удаление владельца каскадом удаляет его клубы."""
    response = http.post(f"{base_url}/clubs/", json=make_club_payload(), headers=auth_headers, timeout=REQUEST_TIMEOUT)
    assert response.status_code == 201, f"Не удалось создать клуб: {response.text}"
    return response.json()
