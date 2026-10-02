import pytest
from jsonschema import validate

from schemas.club_schema import club_schema
from schemas.error_schema import detail_error_schema, validation_error_schema
from utils.data import make_club_payload
from utils.http_client import REQUEST_TIMEOUT, auth_header

CLUBS_PATH = "/clubs/"
NONEXISTENT_ID = 99999999


def club_url(base_url, club_id):
    return f"{base_url}{CLUBS_PATH}{club_id}/"


# ---------------------------------------------------------------- POST


def test_create_club(http, base_url, user, auth_headers):
    payload = make_club_payload()

    response = http.post(f"{base_url}{CLUBS_PATH}", json=payload, headers=auth_headers, timeout=REQUEST_TIMEOUT)

    assert response.status_code == 201, response.text

    body = response.json()
    validate(body, schema=club_schema)

    for field, value in payload.items():
        assert body[field] == value, f"Поле {field} сохранено неверно"

    assert body["owner"] == user["id"], "Владельцем должен стать автор запроса"
    assert body["members"] == [user["id"]], "Создатель автоматически становится участником"
    assert body["reviews"] == []
    assert body["modified"] is None, "У только что созданного клуба нет даты изменения"


def test_create_club_without_auth(http, base_url):
    response = http.post(f"{base_url}{CLUBS_PATH}", json=make_club_payload(), timeout=REQUEST_TIMEOUT)

    assert response.status_code == 401, response.text
    validate(response.json(), schema=detail_error_schema)


def test_create_club_ignores_readonly_fields(http, base_url, user, auth_headers):
    payload = make_club_payload()
    request_body = {**payload, "id": 1, "owner": 1, "members": [1], "reviews": [{"id": 1}]}

    response = http.post(f"{base_url}{CLUBS_PATH}", json=request_body, headers=auth_headers, timeout=REQUEST_TIMEOUT)

    assert response.status_code == 201, response.text

    body = response.json()
    assert body["id"] != 1, "id назначает сервер"
    assert body["owner"] == user["id"], "owner берётся из токена, а не из тела запроса"
    assert body["members"] == [user["id"]]
    assert body["reviews"] == []


def test_create_club_with_existing_title(http, base_url, auth_headers, club):
    payload = make_club_payload(bookTitle=club["bookTitle"])

    response = http.post(f"{base_url}{CLUBS_PATH}", json=payload, headers=auth_headers, timeout=REQUEST_TIMEOUT)

    assert response.status_code == 400, response.text

    body = response.json()
    validate(body, schema=validation_error_schema)

    assert body["bookTitle"] == ["Book Club with this Book Title already exists."]


@pytest.mark.parametrize(
    "overrides, expected_errors",
    [
        (
            {"telegramChatLink": "not-a-url"},
            {"telegramChatLink": ["Enter a valid URL."]},
        ),
        (
            {"publicationYear": "не число"},
            {"publicationYear": ["A valid integer is required."]},
        ),
    ],
    ids=[
        "invalid_url",
        "year_not_a_number",
    ],
)
def test_create_club_validation_errors(http, base_url, auth_headers, overrides, expected_errors):
    payload = make_club_payload(**overrides)

    response = http.post(f"{base_url}{CLUBS_PATH}", json=payload, headers=auth_headers, timeout=REQUEST_TIMEOUT)

    assert response.status_code == 400, response.text

    body = response.json()
    validate(body, schema=validation_error_schema)

    assert body == expected_errors


def test_create_club_with_empty_body(http, base_url, auth_headers):
    response = http.post(f"{base_url}{CLUBS_PATH}", json={}, headers=auth_headers, timeout=REQUEST_TIMEOUT)

    assert response.status_code == 400, response.text

    body = response.json()
    validate(body, schema=validation_error_schema)

    assert set(body) == {"bookTitle", "bookAuthors", "publicationYear", "description", "telegramChatLink"}
    for messages in body.values():
        assert messages == ["This field is required."]


# ---------------------------------------------------------------- GET


def test_get_club_anonymously(http, base_url, club):
    response = http.get(club_url(base_url, club["id"]), timeout=REQUEST_TIMEOUT)

    assert response.status_code == 200, response.text

    body = response.json()
    validate(body, schema=club_schema)

    assert body == club, "Чтение без авторизации должно возвращать те же данные"


def test_get_nonexistent_club(http, base_url):
    response = http.get(club_url(base_url, NONEXISTENT_ID), timeout=REQUEST_TIMEOUT)

    assert response.status_code == 404, response.text
    validate(response.json(), schema=detail_error_schema)


# ---------------------------------------------------------------- PUT / PATCH


def test_patch_club(http, base_url, auth_headers, club):
    new_title = make_club_payload()["bookTitle"]

    response = http.patch(club_url(base_url, club["id"]), json={"bookTitle": new_title},
                          headers=auth_headers, timeout=REQUEST_TIMEOUT)

    assert response.status_code == 200, response.text

    body = response.json()
    validate(body, schema=club_schema)

    assert body["bookTitle"] == new_title
    assert body["bookAuthors"] == club["bookAuthors"], "PATCH не должен менять непереданные поля"
    assert body["created"] == club["created"]
    assert body["modified"] is not None, "После изменения должна появиться дата modified"


def test_put_club(http, base_url, auth_headers, club):
    payload = make_club_payload(publicationYear=1999)

    response = http.put(club_url(base_url, club["id"]), json=payload,
                        headers=auth_headers, timeout=REQUEST_TIMEOUT)

    assert response.status_code == 200, response.text

    body = response.json()
    validate(body, schema=club_schema)

    for field, value in payload.items():
        assert body[field] == value

    assert body["id"] == club["id"]
    assert body["modified"] is not None


def test_put_club_with_partial_body(http, base_url, auth_headers, club):
    response = http.put(club_url(base_url, club["id"]), json={"bookTitle": make_club_payload()["bookTitle"]},
                        headers=auth_headers, timeout=REQUEST_TIMEOUT)

    assert response.status_code == 400, response.text

    body = response.json()
    validate(body, schema=validation_error_schema)

    assert set(body) == {"bookAuthors", "publicationYear", "description", "telegramChatLink"}


@pytest.mark.parametrize("method", ["put", "patch", "delete"])
def test_modify_foreign_club_forbidden(http, base_url, club, create_user, method):
    stranger_headers = auth_header(create_user())
    kwargs = {"json": make_club_payload()} if method in ("put", "patch") else {}

    response = http.request(method, club_url(base_url, club["id"]),
                            headers=stranger_headers, timeout=REQUEST_TIMEOUT, **kwargs)

    assert response.status_code == 403, response.text

    body = response.json()
    validate(body, schema=detail_error_schema)

    assert body["detail"] == "You do not have permission to perform this action."


# ---------------------------------------------------------------- DELETE


def test_delete_club(http, base_url, auth_headers, club):
    response = http.delete(club_url(base_url, club["id"]), headers=auth_headers, timeout=REQUEST_TIMEOUT)

    assert response.status_code == 204, response.text
    assert response.text == "", "204 отдаётся без тела"

    response = http.get(club_url(base_url, club["id"]), timeout=REQUEST_TIMEOUT)
    assert response.status_code == 404, "Удалённый клуб не должен читаться"


# ---------------------------------------------------------------- lifecycle


def test_club_lifecycle(http, base_url, user, auth_headers):
    payload = make_club_payload()
    url = f"{base_url}{CLUBS_PATH}"

    response = http.post(url, json=payload, headers=auth_headers, timeout=REQUEST_TIMEOUT)
    assert response.status_code == 201, response.text
    created = response.json()
    assert created["owner"] == user["id"]

    response = http.get(club_url(base_url, created["id"]), timeout=REQUEST_TIMEOUT)
    assert response.status_code == 200, response.text
    assert response.json() == created

    new_description = "Описание, обновлённое автотестом"
    response = http.patch(club_url(base_url, created["id"]), json={"description": new_description},
                          headers=auth_headers, timeout=REQUEST_TIMEOUT)
    assert response.status_code == 200, response.text

    response = http.get(club_url(base_url, created["id"]), timeout=REQUEST_TIMEOUT)
    assert response.status_code == 200, response.text
    updated = response.json()
    assert updated["description"] == new_description, "Изменение должно сохраниться в базе"
    assert updated["bookTitle"] == created["bookTitle"]
    assert updated["modified"] is not None

    response = http.delete(club_url(base_url, created["id"]), headers=auth_headers, timeout=REQUEST_TIMEOUT)
    assert response.status_code == 204, response.text

    response = http.get(club_url(base_url, created["id"]), timeout=REQUEST_TIMEOUT)
    assert response.status_code == 404, "После удаления клуб недоступен"
