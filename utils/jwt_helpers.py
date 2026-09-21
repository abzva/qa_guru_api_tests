import base64
import json


def decode_jwt_payload(token):
    parts = token.split(".")
    assert len(parts) == 3, f"Токен не похож на JWT: {token!r}"

    payload = parts[1]
    payload += "=" * (-len(payload) % 4)
    return json.loads(base64.urlsafe_b64decode(payload))
