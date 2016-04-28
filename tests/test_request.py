# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import

import unittest

from pynutshell.client import NutshellCRMClient
from pynutshell.http import JSONRPCRequest


class TestClient(unittest.TestCase):

    def setUp(self):
        self.client = NutshellCRMClient(u'test@domain.com', 'TEST-API-KEY')

    def test_jsonrpc_request(self):
        request = JSONRPCRequest(self.client, "getAccount", {'accountId': 4, 'rev': 'REV_IGNORE'})

        expected_params = {
            'id': 'apeye',
            'method': 'getAccount',
            'params': {
                'accountId': 4,
                'rev': 'REV_IGNORE'
            }
        }

        self.assertEqual(request.params, expected_params)

