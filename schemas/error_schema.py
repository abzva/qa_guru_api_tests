detail_error_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Error with detail",
    "type": "object",
    "properties": {
        "detail": {
            "type": "string"
        }
    },
    "required": [
        "detail"
    ]
}

validation_error_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Validation errors",
    "type": "object",
    "minProperties": 1,
    "additionalProperties": {
        "type": "array",
        "minItems": 1,
        "items": {
            "type": "string"
        }
    }
}
