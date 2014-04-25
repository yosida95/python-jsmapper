# -*- coding: utf-8 -*-

from jsmapper import (
    JSONSchema,
    Mapping,
    object_property,
)
from jsmapper.exceptions import ValidationError
from jsmapper.types import (
    String,
    Object,
)


class Address(Mapping):

    @object_property(name='post-office-box')
    def post_office_box(self):
        return JSONSchema(String())

    @object_property(name='extended-address')
    def extended_address(self):
        return JSONSchema(String())

    @object_property(name='street-address')
    def street_address(self):
        return JSONSchema(String())

    locality = JSONSchema(String())
    region = JSONSchema(String())

    @object_property(name='postal-code')
    def postal_code(self):
        return JSONSchema(String())

    @object_property(name='country-name')
    def country_name(self):
        return JSONSchema(String())


AddressSchema = JSONSchema(
    type=Object,
    description="An Address following the convention of "
                "http://microformats.org/wiki/hcard",
    properties=Address,
    dependencies=[
        (Address.post_office_box, Address.street_address),
        (Address.extended_address, Address.street_address),
    ],
    required=[Address.locality, Address.region],
)


def handler(request):
    try:
        address = AddressSchema.bind(request.json_body)
    except ValidationError:
        return 400
    else:
        assert isinstance(address, Address)
