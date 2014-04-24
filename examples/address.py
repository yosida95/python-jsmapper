# -*- coding: utf-8 -*-


from jsmapper.primitive import (
    Array,
    Object,
    String,
)
from jsmapper.schema import (
    Definition,
    JsonSchema,
    Property,
    Reference,
)
from jsmapper.defines import JsonSchemaDraftV3


class Card(JsonSchema):
    """
    {
        "$schema": "http://json-schema.org/draft-03/schema#",
        "description": "A representation of a person, company, organization, or place",
        "type": "object",
        "properties": {
            "fn": {
                "description": "Formatted Name",
                "type": "string"
            },
            "familyName": {
                "type": "string",
                "required": true
            },
            "givenName": {
                "type": "string",
                "required": true
            },
            "additionalName": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            },
            "honorificPrefix": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            },
            "honorificSuffix": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            },
            "nickname": {
                "type": "string"
            },
            "url": {
                "type": "string",
                "format": "uri"
            },
            "email": {
                "type": "object",
                "properties": {
                    "type": {
                        "type": "string"
                    },
                    "value": {
                        "type": "string",
                        "format": "email"
                    }
                }
            },
            "tel": {
                "type": "object",
                "properties": {
                    "type": {
                        "type": "string"
                    },
                    "value": {
                        "type": "string",
                        "format": "phone"
                    }
                }
            },
            "adr": {
                "$ref": "http://json-schema.org/address"
            },
            "geo": {
                "$ref": "http://json-schema.org/geo"
            },
            "tz": {
                "type": "string"
            },
            "photo": {
                "type": "string"
            },
            "logo": {
                "type": "string"
            },
            "sound": {
                "type": "string"
            },
            "bday": {
                "type": "string",
                "format": "date"
            },
            "title": {
                "type": "string"
            },
            "role": {
                "type": "string"
            },
            "org": {
                "type": "object",
                "properties": {
                    "organizationName": {
                        "type": "string"
                    },
                    "organizationUnit": {
                        "type": "string"
                    }
                }
            }
        }
    }
    """

    __jsmeta__ = {
        "$schema": JsonSchemaDraftV3,
        "description": "A representation of a person, company, organization,"
                       "or place",
        "type": Object,
    }

    fn = Property(String(description="Formatted Name"))
    familyName = Property(String(required=True))
    givenName = Property(String(required=True))
    additionalName = Property(String(required=True))
    honorificPrefix = Property(Array(items=String))
    honorificSuffix = Property(Array(items=String))
    nickname = String()
    url = String(format="uri")

    @Definition(name="email")
    class Email(JsonSchema):
        __jsmeta__ = {
            "type": Object,
        }

        type = String()
        value = String(format="email")

    @Definition(name="tel")
    class Tel(JsonSchema):
        __jsmeta__ = {
            "type": Object,
        }

        type = String()
        value = String(format="phone")

    addr = Property(Reference("http://json-schema.org/address"))
    geo = Property(Reference("http://json-schema.org/geo"))
    tz = Property(String())
    photo = Property(String())
    logo = Property(String())
    sound = Property(String())
    bday = Property(String(format="date"))
    title = Property(String())
    role = Property(String())

    @Definition(name="org")
    class Org(JsonSchema):
        __jsmeta__ = {
            "type": Object,
        }

        organizationName = Property(String())
        organizationUnit = Property(String())
