from schemas.error_schema import detail_error_schema, validation_error_schema

success_auth = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Generated schema for Root",
    "type": "object",
    "properties": {
        "refresh": {
            "type": "string"
        },
        "access": {
            "type": "string"
        }
    },
    "required": [
        "refresh",
        "access"
    ]
}

wrong_credentials_auth = detail_error_schema
unsupported_media_type = detail_error_schema
invalid_credentials_schema = validation_error_schema
