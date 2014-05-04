# -*- coding: utf-8 -*-

import json
import os
import unittest
from pprint import pprint

from ..schema import JSONSchema
from ..types import Number, Numeric

from ..examples import product

here = os.path.dirname(os.path.abspath(__file__))

product_request = {
    "id": 2,
    "name": "An ice sculpture",
    "price": 12.50,
    "tags": ["cold", "ice"],
    "dimensions": {
        "length": 7.0,
        "width": 12.0,
        "height": 9.5
    },
    "warehouseLocation": {
        "latitude": -78.75,
        "longitude": 20.4
    }
}


class TestJSONSchema(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_to_dict(self):
        with open(os.path.join(here, '../examples/product.json'), 'r') as fp:
            expected = json.load(fp)
            self.assertEqual(expected, product.ProductSchema.to_dict())
