# -*- coding: utf-8 -*-

from jsmapper import (
    JSONSchema,
    Array,
    Mapping,
    Number,
    Object,
    String,
)
from jsmapper.defines import JSONSchemaDraftV4


class Product(Mapping):

    id = JSONSchema(type=Number(),
                    description="The unique identifier for a product")
    name = JSONSchema(type=String())
    price = JSONSchema(type=Number(minimum=0, exclusiveMinimum=True))
    tags = JSONSchema(type=Array(items=JSONSchema(type=String()),
                                 minItems=1, uniqueItems=True))
    dimensions = JSONSchema(type=Object(
        properties=Dimensions,
        required=[Dimensions.length, Dimensions.width, Dimensions.height]
    ))
    warehouseLocation = JSONSchema(
        ref="http://json-schema.org/geo",
        description="Coordinates of the warehouse with the product"
    )


ProductSchema = JSONSchema(
    schema=JSONSchemaDraftV4,
    title="Product set",
    type=Array(
        items=JSONSchema(
            title="Product",
            type=Object(
                properties=Product,
                required=[Product.id, Product.name, Product.price]
            )
        )
    ),
)
