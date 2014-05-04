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

    class Dimensions(Mapping):
        length = JSONSchema(type=Number())
        width = JSONSchema(type=Number())
        height = JSONSchema(type=Number())

    id = JSONSchema(type=Number(),
                    description="The unique identifier for a product")
    name = JSONSchema(type=String())
    price = JSONSchema(type=Number(minimum=0, exclusive_minimum=True))
    tags = JSONSchema(type=Array(items=JSONSchema(type=String()),
                                 min_items=1, unique_items=True))
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
