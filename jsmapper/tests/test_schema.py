# -*- coding: utf-8 -*-

import unittest
from nose.tools import ok_
from ..schema import (
    JSONSchema,
    JSONSchemaBase,
    JSONSchemaMeta,
    Property,
)


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
