get_clubs_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Generated schema for Root",
    "type": "object",
    "properties": {
        "count": {
            "type": "number"
        },
        "next": {
            "type": ["string", "null"]
        },
        "previous": {
            "type": ["string", "null"]
        },
        "results": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "number"
                    },
                    "bookTitle": {
                        "type": "string"
                    },
                    "bookAuthors": {
                        "type": "string"
                    },
                    "publicationYear": {
                        "type": "number"
                    },
                    "description": {
                        "type": "string"
                    },
                    "telegramChatLink": {
                        "type": "string"
                    },
                    "owner": {
                        "type": "number"
                    },
                    "members": {
                        "type": "array",
                        "items": {
                            "type": "number"
                        }
                    },
                    "reviews": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {
                                    "type": "number"
                                },
                                "club": {
                                    "type": "number"
                                },
                                "user": {
                                    "type": "object",
                                    "properties": {
                                        "id": {
                                            "type": "number"
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
                                    "type": "number"
                                },
                                "readPages": {
                                    "type": "number"
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
                    "created"
                ]
            }
        }
    },
    "required": [
        "count",
        "next",
        "previous",
        "results"
    ]
}
