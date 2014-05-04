# -*- coding: utf-8 -*-

import unittest

from . import product_request
from ..examples import product
from ..types import Object


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
