# -*- coding: utf-8 -*-

import json
import os
import unittest
from nose.tools import ok_

from ..examples import product
from ..mapping import MappingProperty
from ..schema import (
    JSONSchema,
    JSONSchemaBase,
    JSONSchemaMeta,
    Property,
)
from ..types import (
    Object,
    String,
)
from . import product_request

here = os.path.dirname(os.path.abspath(__file__))


class DummyType(JSONSchemaBase):

    def is_primitive(self):
        return True


def test_is_valid_type():
    ok_(JSONSchema.is_valid_type(JSONSchemaBase()) is False)
    ok_(JSONSchema.is_valid_type(DummyType()))
    ok_(JSONSchema.is_valid_type(None))


class TestProperty(unittest.TestCase):

    def test_it(self):
        prop = Property('prop')
        DummySchema = JSONSchemaMeta('DummySchema',
                                     (JSONSchemaBase, ),
                                     {'prop': prop})

        self.assertIs(DummySchema.prop, prop)

        inst = DummySchema()
        self.assertIsNone(inst.prop)

        inst.prop = 'value'
        self.assertEqual(inst.prop, 'value')


class TestJSONSchema(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_it(self):
        obj = product.ProductSchema.bind([product_request])
        self.assertIsInstance(obj, list)
        self.assertEqual(len(obj), 1)

        inst = obj[0]
        self.assertIsInstance(inst, product.Product)

    def test_to_dict(self):
        with open(os.path.join(here, '../examples/product.json'), 'r') as fp:
            expected = json.load(fp)
            self.assertEqual(expected, product.ProductSchema.to_dict())

    def test_dict_properties_01(self):
        schema = JSONSchema(
            type=Object(
                properties={
                    "foo": JSONSchema(type=String())
                }
            )
        )
        self.assertEqual(
            schema.to_dict(),
            {
                "type": "object",
                "properties": {
                    "foo": {
                        "type": "string"
                    }
                }
            }
        )

    def test_dict_properties_02(self):
        schema = JSONSchema(
            type=Object(
                properties={
                    "foo": MappingProperty("foo", JSONSchema(type=String()))
                }
            )
        )

        self.assertEqual(
            schema.to_dict(),
            {
                "type": "object",
                "properties": {
                    "foo": {
                        "type": "string"
                    }
                }
            }
        )
