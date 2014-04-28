# -*- coding: utf-8 -*-

import unittest

from . import address_request
from ..examples import address
from ..types import (
    Numeric,
    Object,
)


class TestPrimitiveType(unittest.TestCase):

    def test_object(self):
        obj = Object(properties=address.Address)
        inst = obj.bind(address_request)

        self.assertIsInstance(inst, address.Address)
        self.assertEqual(inst.country_name, 'Japan')
        self.assertEqual(inst.region, 'Tokyo')
        self.assertEqual(inst.locality, 'Chiyoda-ku')
        self.assertEqual(inst.street_address, '1-3-6 Kudan-kita')
        self.assertEqual(inst.extended_address, '7F')

        self.assertIsNone(inst.postal_code)
        self.assertIsNone(inst.post_office_box)

    def test_object_without_properties(self):
        obj = Object()
        inst = obj.bind(address_request)

        self.assertIs(inst, address_request)
