import os
import unittest
from datetime import datetime

from main import *

test_iiko_login = os.environ.get('IIKO_LOGIN')
test_iiko_password = os.environ.get('IIKO_PASSWORD')
test_iiko_org_id = os.environ.get('IIKO_ORG_ID')


class TestStringMethods(unittest.TestCase):

    def test_get_token(self):
        token = get_iikobiz_token(test_iiko_login, test_iiko_password)
        self.assertIsNotNone(token)
        return token

    def test_get_nomenclature(self):
        token = self.test_get_token()
        nomenclature = get_nomenclature(token, test_iiko_org_id)
        self.assertIsNotNone(nomenclature['revision'])
        return nomenclature

    def test_check_order(self):
        token = self.test_get_token()
        nomenclature = self.test_get_nomenclature()

        result = check_order(nomenclature, token, test_iiko_org_id, {})

        self.assertEqual('success', result['status'])
        self.assertEqual(200, result['status_code'])

    def test_check_order_on_address(self):
        token = self.test_get_token()
        nomenclature = self.test_get_nomenclature()

        result = check_order(nomenclature, token, test_iiko_org_id, {'street': 'Ленина', 'home': 1,'city': 'Орёл'})

        self.assertEqual('success', result['status'])
        self.assertEqual(200, result['status_code'])


if __name__ == '__main__':
    print(test_iiko_login)
    print(test_iiko_password)
    print(test_iiko_org_id)
    unittest.main()
