# -*- coding: utf-8 -*-

import unittest

from ..examples import address


class TestMapping(unittest.TestCase):
    address_request = {
        'country-name': 'Japan',
        'region': 'Tokyo',
        'locality': 'Chiyoda-ku',
        'street-address': '1-3-6 Kudan-kita',
        'extended-address': '7F',
    }

    def test_bind_address(self):
        inst = address.Address._bind(self.address_request)
        self.assertIsInstance(inst, address.Address)
        self.assertEqual(inst.country_name, 'Japan')
        self.assertEqual(inst.region, 'Tokyo')
        self.assertEqual(inst.locality, 'Chiyoda-ku')
        self.assertEqual(inst.street_address, '1-3-6 Kudan-kita')
        self.assertEqual(inst.extended_address, '7F')

        self.assertIsNone(inst.postal_code)
        self.assertIsNone(inst.post_office_box)
