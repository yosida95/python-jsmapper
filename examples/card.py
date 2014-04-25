# -*- coding: utf-8 -*-

import json

from jsmapper import JsonSchema
from jsmapper.exceptions import ValidationError
from jsmapper.schema import (
    Reference,
)
from jsmapper.defines import JsonSchemaDraftV3
from jsmapper.types import (
    Array,
    Object,
    String,
    object_property,
)


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

    fn = JsonSchema(type=String(), description="Formatted Name")

    @object_property(name='familyName', required=True)
    def family_name(self):
        return JsonSchema(
            String(max_length=10),  # FIXME
        )

    @object_property(name='givenName', required=True)
    def given_name(self):
        return JsonSchema(String())

    @object_property(name='additionalName', required=True)
    def additional_name(self):
        return JsonSchema(String())

    @object_property(name='honorific_prefix')
    def honorific_prefix(self):
        return JsonSchema(Array(String))

    @object_property(name='honorificSuffix')
    def honorific_suffix(self):
        return JsonSchema(Array(String))

    nickname = JsonSchema(String())
    url = JsonSchema(String(), format="uri")
    addr = JsonSchema(Reference("http://json-schema.org/address"))
    geo = JsonSchema(Reference("http://json-schema.org/geo"))
    tz = JsonSchema(String())
    photo = JsonSchema(String())
    logo = JsonSchema(String())
    sound = JsonSchema(String())
    bday = JsonSchema(String(), format="date")
    title = JsonSchema(String())
    role = JsonSchema(String())

    class Email(JsonSchema):
        type = JsonSchema(String())
        value = JsonSchema(String(), format="email")

    email = JsonSchema(Object(properties=Email))

    class Tel(JsonSchema):
        type = JsonSchema(String())
        value = JsonSchema(String(), format="phone")

    tel = JsonSchema(Object(), properties=Tel)

    class Org(JsonSchema):
        organizationName = JsonSchema(String())
        organizationUnit = JsonSchema(String())

    org = JsonSchema(Object(), properties=Org)


CardSchema = JsonSchema(
    Object(properties=Card),
    schema=JsonSchemaDraftV3
)


def handler(request):
    try:
        card = CardSchema.bind(json.loads(request))
    except ValidationError:
        return 400
    else:
        assert isinstance(card, Card)
        assert isinstance(card.email, Card.Email)
        assert isinstance(card.tel, Card.Tel)
        assert isinstance(card.org, Card.Org)
