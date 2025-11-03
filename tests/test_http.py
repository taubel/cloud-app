import requests

from .settings import get_host, get_user, get_private_key_path

HOST = get_host()
USER = get_user()
PRIVATE_KEY_PATH = get_private_key_path()


def test_http_get():
    response = requests.get(f"http://{HOST}:80/")
    assert response.status_code == 200, (f"GET request failed. "
                                         f"Status code: {response.status_code}, "
                                         f"reason: {response.reason}, payload: {response.text}")
