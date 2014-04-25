# -*- coding: utf-8 -*-

import json

from jsmapper import (
    JSONSchema,
    Mapping,
    Reference,
    object_property,
)
from jsmapper.defines import JSONSchemaDraftV3
from jsmapper.exceptions import ValidationError
from jsmapper.types import (
    Array,
    Object,
    String,
)


class Card(Mapping):
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

    fn = JSONSchema(type=String(), description="Formatted Name")

    @object_property(name='familyName')
    def family_name(self):
        return JSONSchema(
            String(max_length=10),  # FIXME
        )

    @object_property(name='givenName')
    def given_name(self):
        return JSONSchema(String())

    @object_property(name='additionalName')
    def additional_name(self):
        return JSONSchema(String())

    @object_property(name='honorific_prefix')
    def honorific_prefix(self):
        return JSONSchema(Array(items=JSONSchema(String())))

    @object_property(name='honorificSuffix')
    def honorific_suffix(self):
        return JSONSchema(Array(items=JSONSchema(String())))

    nickname = JSONSchema(String())
    url = JSONSchema(String(), format="uri")
    addr = JSONSchema(Reference("http://json-schema.org/address"))
    geo = JSONSchema(Reference("http://json-schema.org/geo"))
    tz = JSONSchema(String())
    photo = JSONSchema(String())
    logo = JSONSchema(String())
    sound = JSONSchema(String())
    bday = JSONSchema(String(), format="date")
    title = JSONSchema(String())
    role = JSONSchema(String())

    class Email(Mapping):
        type = JSONSchema(String())
        value = JSONSchema(String(), format="email")

    email = JSONSchema(Object(properties=Email))

    class Tel(Mapping):
        type = JSONSchema(String())
        value = JSONSchema(String(), format="phone")

    tel = JSONSchema(Object(properties=Tel))

    class Org(Mapping):
        organizationName = JSONSchema(String())
        organizationUnit = JSONSchema(String())

    org = JSONSchema(Object(properties=Org))


CardSchema = JSONSchema(
    Object(
        properties=Card,
        required=[Card.family_name, Card.given_name],
    ),
    schema=JSONSchemaDraftV3,
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
