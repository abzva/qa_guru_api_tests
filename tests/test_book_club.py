import requests
from jsonschema import validate

from schemas.get_clubs_schema import get_clubs_schema
from utils.http_client import REQUEST_TIMEOUT


def test_get_clubs_schema():
    response = requests.get("https://book-club.qa.guru/api/v1/clubs/", timeout=REQUEST_TIMEOUT)
    body = response.json()

    assert response.status_code == 200
    validate(instance=body, schema=get_clubs_schema)


def test_get_clubs_search(club):
    url = "https://book-club.qa.guru/api/v1/clubs/"
    search = club["bookTitle"].split()[-1]
    response = requests.get(url, params={"search": search}, timeout=REQUEST_TIMEOUT)
    body = response.json()

    assert response.status_code == 200
    validate(instance=body, schema=get_clubs_schema)

    assert club["id"] in [found["id"] for found in body["results"]]

    for found in body["results"]:
        assert search.lower() in found["bookTitle"].lower(), \
            f"Club id={found['id']} title={found['bookTitle']!r} doesn't match"


def test_get_clubs_page():
    url = "https://book-club.qa.guru/api/v1/clubs/"
    page = 2
    response = requests.get(url, params={"page": page}, timeout=REQUEST_TIMEOUT)
    body = response.json()

    assert response.status_code == 200
    validate(instance=body, schema=get_clubs_schema)

    assert body["previous"] is not None
    assert body["next"] is not None
