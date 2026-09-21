import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

REQUEST_TIMEOUT = 30


def build_session():
    """Сессия для тестов: повторяет запрос, только если он не дошёл до сервера."""
    session = requests.Session()
    adapter = HTTPAdapter(max_retries=Retry(total=None, connect=3, read=0, status=0, backoff_factor=1.0))
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def auth_header(user):
    return {"Authorization": f"Bearer {user['access']}"}
