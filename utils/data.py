import uuid


def unique_suffix():
    return uuid.uuid4().hex[:10]


def make_credentials():
    suffix = unique_suffix()
    return {"username": f"qa_guru_{suffix}", "password": f"P@ssw0rd-{suffix}"}


def username_of_length(length):
    base = f"qa_{unique_suffix()}"
    assert length >= len(base), f"Минимальная длина уникального username — {len(base)}"
    return base + "a" * (length - len(base))


def password_of_length(length):
    return "a" * length


def make_club_payload(**overrides):
    payload = {
        "bookTitle": f"QA Guru Club {unique_suffix()}",
        "bookAuthors": "John Steinbeck",
        "publicationYear": 1937,
        "description": "Клуб, созданный автотестом",
        "telegramChatLink": "https://t.me/qa_guru_club",
    }
    payload.update(overrides)
    return payload
