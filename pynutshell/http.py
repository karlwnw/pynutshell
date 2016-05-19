# -*- coding: utf-8 -*-

from __future__ import (print_function, unicode_literals, absolute_import,
                        division)

import copy
import json

from .errors import *
from .response import NutshellResponse

GET, POST, PUT, DELETE = "GET", "POST", "PUT", "DELETE"


class RequestMethod(object):
    def __init__(self, client, f):
        self.client = client
        self.f = f
        self.__name__ = f.__name__

    def __call__(self, *args, **kwargs):
        return self.client.http.send_request(self.make_request(*args, **kwargs))

    def make_request(self, *args, **kwargs):
        return self.f(self.client, *args, **kwargs)


def doc_string(doc):
    def decorator(f):
        f.__doc__ = doc
        return f
    return decorator


def request_method(f):
    @property
    @doc_string(f.__doc__)
    def wrapped(self):
        return RequestMethod(self, f)
    return wrapped


def make_query_string(params):
    return '&'.join(map('='.join, sorted(params.items(), key=lambda x: x[0])))


def process_response(status, body):
    """
    Todo: handle 204, sometimes Agile API returns 204 as success
    """
    if status == 200:
        return NutshellResponse(body)
    elif status == 400:
        raise NutshellCRMBadRequest(body)
    elif status == 401:
        raise NutshellCRMBadAuth(body)
    elif status == 404:
        raise NutshellCRMNotFound(body)
    elif status == 403:
        raise NutshellCRMForbidden(body)
    elif status == 406:
        raise NutshellCRMLimitExceeded(body)
    elif status == 500:
        raise NutshellCRMServerError(body)
    else:
        raise NutshellCRMBadStatus("%s: %s" % (status, body))


class Request(object):
    """Represents the request to be made to the API Client.

    An instance of that object is passed to the backend's send_request method
    for each request.

    :param config: an instance of Client
    :param method: HTTP method as a string
    :param params: Query params or body depending on the method
    :param headers: custom HTTP headers
    """
    def __init__(self, config, method, params=None, headers=None):
        if params is None:
            params = {}
        self.config = config
        self.method = method
        self.params = copy.copy(params)
        if method == POST:
            self.body = json.dumps(params)
            self.query_params = {}
            self._headers = {
                "Accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded"
            }
        elif method == GET:
            self.body = bytes()
            self.query_params = params
            self._headers = {
                "Accept": "application/json",
            }
        else:
            raise NotImplementedError("Only GET and POST supported")

        if headers is not None:
            self._headers.update(headers)

    @property
    def query_string(self):
        return make_query_string(self.query_params)

    @property
    def url(self):
        return "%s://%s" % (self.config.scheme, self.config.host)

    @property
    def headers(self):
        return self._headers


class JSONRPCRequest(Request):

    def __init__(self, config, method, params=None):
        params = self.make_params(method, params)
        super(JSONRPCRequest, self).__init__(config, POST, params)

    def make_params(self, method, params=None):
        """
        Construct the JSON-RPC params
        """
        jsonrpc_params = {"id": "apeye", "method": method}
        if params is not None:
            jsonrpc_params.update({'params': params})
        return jsonrpc_params
