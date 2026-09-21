user_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "User",
    "type": "object",
    "properties": {
        "id": {
            "type": "integer"
        },
        "username": {
            "type": "string"
        },
        "firstName": {
            "type": "string"
        },
        "lastName": {
            "type": "string"
        },
        "email": {
            "type": "string"
        },
        "remoteAddr": {
            "type": "string"
        }
    },
    "required": [
        "id",
        "username",
        "firstName",
        "lastName",
        "email",
        "remoteAddr"
    ]
}
