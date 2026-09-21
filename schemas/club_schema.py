review_schema = {
    "type": "object",
    "properties": {
        "id": {
            "type": "integer"
        },
        "club": {
            "type": "integer"
        },
        "user": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer"
                },
                "username": {
                    "type": "string"
                }
            },
            "required": [
                "id",
                "username"
            ]
        },
        "review": {
            "type": "string"
        },
        "assessment": {
            "type": "integer",
            "minimum": 1,
            "maximum": 5
        },
        "readPages": {
            "type": "integer"
        },
        "created": {
            "type": "string"
        },
        "modified": {
            "type": ["string", "null"]
        }
    },
    "required": [
        "id",
        "club",
        "user",
        "review",
        "assessment",
        "readPages",
        "created"
    ]
}

club_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Book Club",
    "type": "object",
    "properties": {
        "id": {
            "type": "integer"
        },
        "bookTitle": {
            "type": "string",
            "maxLength": 255
        },
        "bookAuthors": {
            "type": "string",
            "maxLength": 255
        },
        "publicationYear": {
            "type": "integer"
        },
        "description": {
            "type": "string"
        },
        "telegramChatLink": {
            "type": "string",
            "maxLength": 200
        },
        "owner": {
            "type": "integer"
        },
        "members": {
            "type": "array",
            "items": {
                "type": "integer"
            }
        },
        "reviews": {
            "type": "array",
            "items": review_schema
        },
        "created": {
            "type": "string"
        },
        "modified": {
            "type": ["string", "null"]
        }
    },
    "required": [
        "id",
        "bookTitle",
        "bookAuthors",
        "publicationYear",
        "description",
        "telegramChatLink",
        "owner",
        "members",
        "reviews",
        "created",
        "modified"
    ]
}
