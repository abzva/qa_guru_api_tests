import requests

from jsonschema import validate
from schemas.get_clubs_schema import get_clubs_schema


def test_get_clubs_schema():
    response = requests.get("https://book-club.qa.guru/api/v1/clubs/")
    body = response.json()

    assert response.status_code == 200
    validate(instance=body, schema=get_clubs_schema)


def test_get_clubs_search():
    url = "https://book-club.qa.guru/api/v1/clubs/"
    response = requests.get(url, params={"search": "mice"})
    body = response.json()

    assert response.status_code == 200
    validate(instance=body, schema=get_clubs_schema)
    assert len(body["results"]) != 0

    for club in body["results"]:
        assert "mice" in club["bookTitle"].lower(), f"Club id={club['id']} title={club['bookTitle']!r} doesn't match"


def test_get_clubs_page_size():
    url = "https://book-club.qa.guru/api/v1/clubs/"
    page_size = 355
    response = requests.get(url, params={"page_size": page_size})
    body = response.json()

    assert response.status_code == 200
    validate(instance=body, schema=get_clubs_schema)

    assert len(body["results"]) == page_size


def test_get_clubs_page():
    url = "https://book-club.qa.guru/api/v1/clubs/"
    page = 2
    response = requests.get(url, params={"page": page})
    body = response.json()

    assert response.status_code == 200
    validate(instance=body, schema=get_clubs_schema)

    assert body["previous"] is not None
    assert body["next"] is not None
