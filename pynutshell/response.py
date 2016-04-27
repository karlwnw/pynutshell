# -*- coding: utf-8 -*-
import json


class NutshellResponse(object):
    """
    https://www.nutshell.com/api/jsonrpc.html
    https://en.wikipedia.org/wiki/JSON-RPC
    """
    def __init__(self, body):
        self.json = json.loads(body)
        self.id = self.json.get('id')
        self.result = self.json.get('result')
        self.error = self.json.get('error')

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, str(self.json))
