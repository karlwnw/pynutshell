# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import logging

# Documentation: https://github.com/agilecrm/rest-api
from .http import request_method, JSONRPCRequest

NUTSHELL_API_HOST = "app01.nutshell.com/api/v1/json"


# These two lines enable debugging at httplib level (requests->urllib3->http.client)
# You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
# The only thing missing will be the response.body which is not logged.
try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client
http_client.HTTPConnection.debuglevel = 1

# You must initialize logging, otherwise you'll not see debug output.
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True


class BaseNutshellCRMClient(object):

    def __init__(self, api_email, api_key, backend=None, timeout=5):
        if backend is None:
            from .requests import RequestsBackend
            backend = RequestsBackend

        self._api_email = api_email
        self._api_key = api_key
        self._timeout = timeout
        self._host = NUTSHELL_API_HOST

        self.http = backend(self, auth=(self.api_email, self.api_key))

    @property
    def scheme(self):
        return 'https'

    @property
    def host(self):
        return self._host

    @property
    def api_email(self):
        return self._api_email

    @property
    def api_key(self):
        return self._api_key

    @property
    def timeout(self):
        return self._timeout


class NutshellCRMClient(BaseNutshellCRMClient):
    """
    Note on Contacts/People and Accounts/Companies: you might notice that Nutshell refers to People and Companies,
    but the API uses the terminology Contacts and Accounts.

    https://blog.nutshell.com/nutshell-is-getting-more-personal
    https://www.nutshell.com/api/entities-relationships.html
    """

    # CONTACTS (PEOPLE)

    @request_method
    def get_contact(self, contact_id):
        params = {"contactId": contact_id}
        return JSONRPCRequest(self, "getContact", params)

    @request_method
    def new_contact(self, params):
        return JSONRPCRequest(self, "newContact", params)

    @request_method
    def edit_contact(self, contact_id, rev="REV_IGNORE", name=None, phone=None, tags=None):
        contact = {}
        if name:
            contact["name"] = name
        if phone:
            contact["phone"] = phone
        if tags:
            contact["tags"] = tags
        params = {"contact": contact, "contactId": contact_id, "rev": rev}

        return JSONRPCRequest(self, "editContact", params)

    @request_method
    def find_contacts(self, query, order_by='name', order_direction='ASC', limit=50, page=1, stub_responses=True):
        params = {}
        return JSONRPCRequest(self, "findContacts", params)

    @request_method
    def search_contacts(self, string, limit=10):
        params = {'string': string, 'limit': limit}
        return JSONRPCRequest(self, "searchContacts", params)

    # ACCOUNTS (COMPANIES)

    @request_method
    def get_account(self, account_id):
        params = {"accountId": account_id}
        return JSONRPCRequest(self, "getAccount", params)

    @request_method
    def new_account(self, params):
        return JSONRPCRequest(self, "newAccount", params)

    @request_method
    def edit_account(self, account_id, rev="REV_IGNORE", name=None, url=None, tags=None):
        contact = {}
        if name:
            contact["name"] = name
        if url:
            contact["url"] = url
        if tags:
            contact["tags"] = tags
        params = {"account": contact, "accountId": account_id, "rev": rev}
        return JSONRPCRequest(self, "editAccount", params)

    @request_method
    def find_accounts(self, query, order_by='name', order_direction='ASC', limit=50, page=1, stub_responses=True):
        params = {}
        return JSONRPCRequest(self, "findAccounts", params)

    @request_method
    def search_accounts(self, string, limit=10):
        params = {'string': string, 'limit': limit}
        return JSONRPCRequest(self, "searchAccounts", params)

    # CUSTOM FIELDS

    @request_method
    def find_custom_fields(self):
        return JSONRPCRequest(self, "findCustomFields")
