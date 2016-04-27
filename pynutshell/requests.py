# -*- coding: utf-8 -*-

from __future__ import (print_function, unicode_literals, absolute_import,
                        division)

import requests

from .http import process_response


class RequestsBackend(object):
    """Adapter for the requests module.

    :param config:  client object
    :param options: key-value passed into the requests.request constructor
    """
    def __init__(self, config, **options):
        self.config = config
        self.options = options
        self.session = requests.Session()

    def send_request(self, request):
        resp = self.session.request(
            request.method,
            request.url,
            headers=request.headers,
            data=request.body,
            timeout=self.config.timeout,
            **self.options
        )
        return process_response(resp.status_code, resp.text)
