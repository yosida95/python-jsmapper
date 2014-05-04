# -*- coding: utf-8 -*-

import json
import os
import unittest
from nose.tools import (
    eq_,
    raises,
)

from . import product_request
from ..examples import product
from ..types import Object

here = os.path.dirname(os.path.abspath(__file__))


class TestPrimitiveType(unittest.TestCase):

    def test_object(self):
        obj = Object(properties=product.Product)
        inst = obj.bind(product_request)

        self.assertIsInstance(inst, product.Product)
        self.assertEqual(inst.id, 2)
        self.assertEqual(inst.name, "An ice sculpture")
        self.assertEqual(inst.price, 12.50)
        self.assertEqual(inst.tags, ["cold", "ice"])
        self.assertEqual(inst.dimensions.length, 7.0)
        self.assertEqual(inst.dimensions.width, 12.0)
        self.assertEqual(inst.dimensions.height, 9.5)
        self.assertEqual(inst.warehouseLocation, {
            "latitude": -78.75,
            "longitude": 20.4,
        })

    def test_object_bind(self):
        obj = Object(properties=product.Product._to_dict(),
                     required=[
                         product.Product.id,
                         product.Product.name,
                         product.Product.price])
        inst = obj.bind(product_request)
        self.assertEqual(inst, product_request)

        with open(os.path.join(here, '../examples/product.json'), 'r') as fp:
            expected = json.load(fp)["items"]
            del expected["title"]

            self.assertEqual(expected, obj.to_dict())


def test_dependencies_to_dict():
    dep = {
        product.Product.tags: [product.Product.name],
    }
    eq_(Object.dependencies_to_dict(dep), {'tags': ['name']})


@raises(ValueError)
def test_dependencies_to_dict_with_integer_key():
    Object.dependencies_to_dict({123: [product.Product.name]})


@raises(ValueError)
def test_dependencies_to_dict_with_integer_value():
    Object.dependencies_to_dict({product.Product.tags: [123]})
