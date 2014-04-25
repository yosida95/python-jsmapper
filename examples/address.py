# -*- coding: utf-8 -*-

from jsmapper import JsonSchema
from jsmapper.exceptions import ValidationError
from jsmapper.mapping import Mapping
from jsmapper.schema import Property
from jsmapper.types import (
    String,
    Object,
)


class Address(ObjectProperties):
    foo = JsonSchema(
        String(maxLength=10)
    )

    @object_property(name='personName')
    def person_name(self):
        return JsonSchema(
            type=Object,
            properties=PersonName,
            description="",
        )



AddressSchema = JsonSchema(
    type=Address,
    description="An Address following the convention of "
                "http://microformats.org/wiki/hcard",
    dependencies=[
        (Address.post_office_box, Address.street_address),
        (Address.extended_address, Address.street_address),
    ]
    # properties=Address,
)

FooSchema = new Integer(maximum=10)
foo = FooSchema.bind(request.json_body)
assert isinstance(foo, int)


def main(request):
    try:
        address = AddressSchema.bind(request.json_body)

        assert isinstance(address, Address)
    except ValidationError:
        return 400
