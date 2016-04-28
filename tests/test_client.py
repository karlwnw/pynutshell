# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import

import json
import unittest

from pynutshell.client import NutshellCRMClient
from pynutshell.http import JSONRPCRequest
from tests.stubs import get_contact

try:
    import unittest.mock as mock
except ImportError:
    import mock


class TestClient(unittest.TestCase):

    def setUp(self):
        self.client = NutshellCRMClient(u'test@domain.com', 'TEST-API-KEY')

    def test_get_contact_request(self):
        expected_params = {
            'id': 'apeye',
            'method': 'getContact',
            'params': {
                'contactId': 12,
                'rev': 'REV_IGNORE'
            }
        }

        with mock.patch('json.dumps', return_value=expected_params) as json_dumps_mock:
            request = self.client.get_contact.make_request(12)

            self.assertEqual(request.url, u'https://app01.nutshell.com/api/v1/json')
            self.assertEqual(request.method, u'POST')
            self.assertEqual(request.params, expected_params)

        json_dumps_mock.assert_called_once_with(expected_params)

    def test_new_contact_request(self):
            params = {
                'contact': {
                    "name": "Andy Fowler",
                    "owner": {
                        "entityType": "Users",
                        "id": 1
                    },
                    "description": "Beagle owner",
                    "phone": ["717-555-0480", "+216 707-555-2903", "877-555-5555"],
                    "email": ["andy@gmail.com", "fowler@charter.net"]
                }
            }

            expected_params = {
                'id': 'apeye',
                'method': 'newContact',
                'params': params
            }

            json_dumped = json.dumps(expected_params)
            with mock.patch('json.dumps', return_value=json_dumped) as json_dumps_mock:
                request = self.client.new_contact.make_request(params)

                self.assertEqual(request.url, u'https://app01.nutshell.com/api/v1/json')
                self.assertEqual(request.method, u'POST')
                self.assertEqual(request.params, expected_params)
                self.assertEqual(request.body, json_dumped)

            json_dumps_mock.assert_called_once_with(expected_params)

    def test_get_contact_response(self):
        stub_response = mock.Mock()
        stub_response.text = json.dumps(get_contact.RESPONSE)
        stub_response.status_code = 200

        with mock.patch('requests.Session.request', return_value=stub_response) as request_mock:
            request = JSONRPCRequest(self.client, "getContact", {"accountId": 1})
            response = self.client.http.send_request(request)

            self.assertEqual(response.json, get_contact.RESPONSE)
            self.assertEqual(response.id, get_contact.RESPONSE['id'])
            self.assertEqual(response.error, get_contact.RESPONSE['error'])
            self.assertEqual(response.result, get_contact.RESPONSE['result'])

        request_mock.assert_called_once_with('POST', request.url,
                                             headers=request.headers,
                                             data=request.body,
                                             timeout=self.client.timeout,
                                             auth=(self.client.api_email, self.client.api_key))


if __name__ == '__main__':
    unittest.main()
