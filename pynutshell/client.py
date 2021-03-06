# -*- coding: utf-8 -*-

from __future__ import unicode_literals

# import logging

# Documentation: https://github.com/agilecrm/rest-api
from .http import request_method, JSONRPCRequest
from .requests import RequestsBackend

NUTSHELL_API_HOST = "app01.nutshell.com"
REV_IGNORE = "REV_IGNORE"


# These two lines enable debugging at httplib level (requests->urllib3->http.client)
# You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
# The only thing missing will be the response.body which is not logged.
# try:
#     import http.client as http_client
# except ImportError:
#     # Python 2
#     import httplib as http_client
# http_client.HTTPConnection.debuglevel = 1
#
# # You must initialize logging, otherwise you'll not see debug output.
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True


class BaseNutshellCRMClient(object):

    def __init__(self, api_email, api_key, backend=None, timeout=5,
                 host=NUTSHELL_API_HOST, scheme='https'):
        if backend is None:
            backend = RequestsBackend

        self._api_email = api_email
        self._api_key = api_key
        self._timeout = timeout
        self._host = "{}{}".format(host, "/api/v1/json")
        self._scheme = scheme

        self.http = backend(self, auth=(self.api_email, self.api_key))

    @property
    def scheme(self):
        return self._scheme

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

    @classmethod
    def get_endpoint(cls, username):
        """
        https://www.nutshell.com/api/endpoint-discovery.html
        """
        params = {'username': username}

        class AnonymousClient(object):
            host = "api.nutshell.com/v1/json"
            scheme = "http"
            timeout = 5

            def __init__(self):
                self.http = RequestsBackend(self)
        client = AnonymousClient()
        return client.http.send_request(JSONRPCRequest(client, "getApiForUsername", params))


class NutshellCRMClient(BaseNutshellCRMClient):
    """
    Note on Contacts/People and Accounts/Companies: you might notice that Nutshell refers to People and Companies,
    but the API uses the terminology Contacts and Accounts.

    https://blog.nutshell.com/nutshell-is-getting-more-personal
    https://www.nutshell.com/api/entities-relationships.html
    """

    # CONTACTS (PEOPLE)

    @request_method
    def get_contact(self, contact_id, rev=REV_IGNORE):
        params = {"contactId": contact_id, "rev": rev}
        return JSONRPCRequest(self, "getContact", params)

    @request_method
    def new_contact(self, params):
        return JSONRPCRequest(self, "newContact", {"contact": params})

    @request_method
    def edit_contact(self, contact_id, contact, rev=REV_IGNORE):
        params = {'contactId': contact_id, "contact": contact, "rev": rev}
        return JSONRPCRequest(self, "editContact", params)

    @request_method
    def delete_contact(self, contact_id):
        params = {"contactId": contact_id, "rev": REV_IGNORE}
        return JSONRPCRequest(self, "deleteContact", params)

    @request_method
    def find_contacts(self, query, order_by='name', order_direction='ASC', limit=50, page=1, stub_responses=True):
        params = {
            'query': query,
            'orderBy': order_by,
            'orderDirection': order_direction,
            'limit': limit,
            'page': page,
            'stubResponses': stub_responses
        }
        return JSONRPCRequest(self, "findContacts", params)

    @request_method
    def search_contacts(self, string, limit=10):
        params = {'string': string, 'limit': limit}
        return JSONRPCRequest(self, "searchContacts", params)

    # ACCOUNTS (COMPANIES)

    @request_method
    def get_account(self, account_id, rev=REV_IGNORE):
        params = {"accountId": account_id, "rev": rev}
        return JSONRPCRequest(self, "getAccount", params)

    @request_method
    def new_account(self, params):
        return JSONRPCRequest(self, "newAccount", {"account": params})

    @request_method
    def edit_account(self, account_id, account, rev=REV_IGNORE):
        params = {'accountId': account_id, "account": account, "rev": rev}
        return JSONRPCRequest(self, "editAccount", params)

    @request_method
    def delete_account(self, account_id, rev=REV_IGNORE):
        params = {"contactId": account_id, "rev": rev}
        return JSONRPCRequest(self, "deleteAccount", params)

    @request_method
    def find_accounts(self, query, order_by='name', order_direction='ASC', limit=50, page=1, stub_responses=True):
        params = {
            'query': query,
            'orderBy': order_by,
            'orderDirection': order_direction,
            'limit': limit,
            'page': page,
            'stubResponses': stub_responses
        }
        return JSONRPCRequest(self, "findAccounts", params)

    @request_method
    def search_accounts(self, string, limit=10):
        params = {'string': string, 'limit': limit}
        return JSONRPCRequest(self, "searchAccounts", params)

    # LEADS

    @request_method
    def get_lead(self, lead_id, rev=REV_IGNORE):
        params = {"leadId": lead_id, "rev": rev}
        return JSONRPCRequest(self, "getLead", params)

    @request_method
    def new_lead(self, params):
        return JSONRPCRequest(self, "newLead", {"lead": params})

    @request_method
    def edit_lead(self, lead_id, lead, rev=REV_IGNORE):
        params = {'leadId': lead_id, "lead": lead, "rev": rev}
        return JSONRPCRequest(self, "editLead", params)

    @request_method
    def delete_lead(self, lead_id, rev=REV_IGNORE):
        params = {"leadId": lead_id, "rev": rev}
        return JSONRPCRequest(self, "deleteLead", params)

    @request_method
    def find_lead_outcomes(self, order_by='description', order_direction='ASC', limit=50, page=1):
        params = {
            'orderBy': order_by,
            'orderDirection': order_direction,
            'limit': limit,
            'page': page,
        }
        return JSONRPCRequest(self, "findLead_Outcomes", params)

    @request_method
    def find_leads(self, query, order_by='id', order_direction='ASC', limit=50, page=1, stub_responses=True):
        params = {
            'query': query,
            'orderBy': order_by,
            'orderDirection': order_direction,
            'limit': limit,
            'page': page,
            'stubResponses': stub_responses
        }
        return JSONRPCRequest(self, "findLeads", params)

    # TASKS

    @request_method
    def get_task(self, task_id, rev=REV_IGNORE):
        params = {"taskId": task_id, "rev": rev}
        return JSONRPCRequest(self, "getTask", params)

    @request_method
    def new_task(self, params):
        return JSONRPCRequest(self, "newTask", {"task": params})

    @request_method
    def edit_task(self, task_id, task, rev=REV_IGNORE):
        params = {'taskId': task_id, "task": task, "rev": rev}
        return JSONRPCRequest(self, "editTask", params)

    @request_method
    def delete_task(self, task_id, rev=REV_IGNORE):
        params = {"taskId": task_id, "rev": rev}
        return JSONRPCRequest(self, "deleteTask", params)

    @request_method
    def find_tasks(self, query, order_by='due_time', order_direction='ASC', limit=50, page=1, stub_responses=True):
        params = {
            'query': query,
            'orderBy': order_by,
            'orderDirection': order_direction,
            'limit': limit,
            'page': page,
            'stubResponses': stub_responses
        }
        return JSONRPCRequest(self, "findTasks", params)

    # ACTIVITIES

    @request_method
    def get_activity(self, activity_id, rev=REV_IGNORE):
        params = {"activityId": activity_id, "rev": rev}
        return JSONRPCRequest(self, "getActivity", params)

    @request_method
    def new_activity(self, params):
        return JSONRPCRequest(self, "newActivity", {"activity": params})

    @request_method
    def edit_activity(self, activity_id, activity, rev=REV_IGNORE):
        params = {'activityId': activity_id, "activity": activity, "rev": rev}
        return JSONRPCRequest(self, "editActivity", params)

    @request_method
    def delete_activity(self, activity_id, rev=REV_IGNORE):
        params = {"activityId": activity_id, "rev": rev}
        return JSONRPCRequest(self, "deleteActivity", params)

    @request_method
    def find_activities(self, query, order_by='name', order_direction='ASC', limit=50, page=1, stub_responses=True):
        params = {
            'query': query,
            'orderBy': order_by,
            'orderDirection': order_direction,
            'limit': limit,
            'page': page,
            'stubResponses': stub_responses
        }
        return JSONRPCRequest(self, "findActivities", params)

    # PRODUCTS

    @request_method
    def get_product(self, product_id, rev=REV_IGNORE):
        params = {"productId": product_id, "rev": rev}
        return JSONRPCRequest(self, "getProduct", params)

    @request_method
    def new_product(self, params):
        return JSONRPCRequest(self, "newProduct", {"product": params})

    @request_method
    def edit_product(self, product_id, product, rev=REV_IGNORE):
        params = {'productId': product_id, "product": product, "rev": rev}
        return JSONRPCRequest(self, "editProduct", params)

    @request_method
    def delete_product(self, product_id, rev=REV_IGNORE):
        params = {"productId": product_id, "rev": rev}
        return JSONRPCRequest(self, "deleteProduct", params)

    @request_method
    def find_products(self, query, order_by='name', order_direction='ASC', limit=50, page=1, stub_responses=True):
        params = {
            'query': query,
            'orderBy': order_by,
            'orderDirection': order_direction,
            'limit': limit,
            'page': page,
            'stubResponses': stub_responses
        }
        return JSONRPCRequest(self, "findProducts", params)

    # NOTES

    @request_method
    def get_note(self, note_id, rev=REV_IGNORE):
        params = {"noteId": note_id, "rev": rev}
        return JSONRPCRequest(self, "getNote", params)

    @request_method
    def new_note(self, params):
        return JSONRPCRequest(self, "newNote", {"note": params})

    @request_method
    def edit_note(self, note_id, note, rev=REV_IGNORE):
        params = {'noteId': note_id, "note": note, "rev": rev}
        return JSONRPCRequest(self, "editNote", params)

    @request_method
    def delete_note(self, note_id, rev=REV_IGNORE):
        params = {"noteId": note_id, "rev": rev}
        return JSONRPCRequest(self, "deleteNote", params)

    # sources

    @request_method
    def new_source(self, name):
        """
        Given a source name, fetches an existing source or creates a new one if it does not exist.
        """
        params = {"name": name}
        return JSONRPCRequest(self, "newSource", params)

    @request_method
    def find_sources(self, order_by='name', order_direction='ASC', limit=50, page=1):
        params = {
            'orderBy': order_by,
            'orderDirection': order_direction,
            'limit': limit,
            'page': page,
        }
        return JSONRPCRequest(self, "findSources", params)

    @request_method
    def search_contacts(self, string, limit=10):
        params = {'string': string, 'limit': limit}
        return JSONRPCRequest(self, "searchSources", params)

    # Field, Tags, Territories, Backups

    @request_method
    def find_custom_fields(self):
        return JSONRPCRequest(self, "findCustomFields")

    @request_method
    def find_tags(self):
        return JSONRPCRequest(self, "findTags")

    @request_method
    def find_backups(self):
        return JSONRPCRequest(self, "findBackups")

    @request_method
    def new_backup(self):
        return JSONRPCRequest(self, "newBackup")

    @request_method
    def instance_data(self):
        return JSONRPCRequest(self, "instanceData")

    @request_method
    def find_territories(self, order_by='name', order_direction='ASC', limit=50, page=1):
        params = {
            'orderBy': order_by,
            'orderDirection': order_direction,
            'limit': limit,
            'page': page
        }
        return JSONRPCRequest(self, "findTerritories", params)

    @request_method
    def find_account_types(self, order_by='name', order_direction='ASC', limit=50, page=1):
        params = {
            'orderBy': order_by,
            'orderDirection': order_direction,
            'limit': limit,
            'page': page
        }
        return JSONRPCRequest(self, "findAccountTypes", params)

    @request_method
    def get_analytics_report(self, report_type, period, filter=None, options=None):
        params = {'reportType': report_type, 'period': period}
        if filter is not None:
            params.update({'filter': filter})
        if options is not None:
            params.update({'options': options})
        return JSONRPCRequest(self, "getAnalyticsReport", params)

    # TESTING

    @request_method
    def add(self, num1, num2):
        params = {"num1": num1, "num2": num2}
        return JSONRPCRequest(self, "add", params)
