# !/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import httplib2
import simplejson as json
from urlparse import urlparse

from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client import tools

from clover.exceptions import *


class Clover:
    """ Class for authorization with OAuth2 in the Clover.com and working with it """

    def __init__(self, api_uri, client_id, client_secret, redirect_uri, merchant_id, debug=False):
        # Api uri
        self.api_uri = api_uri
        self.auth_uri = self.api_uri + '/oauth/authorize'
        self.token_uri = self.api_uri + '/oauth/token'

        # Variables
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.merchant_id = merchant_id
        self.debug = debug
        self.http = httplib2.Http()
        self.auth()

    # OAUTH2
    def auth(self):
        flow = OAuth2WebServerFlow(
            client_id=self.client_id,
            client_secret=self.client_secret,
            scope='',
            redirect_uri=self.redirect_uri,
            auth_uri=self.auth_uri,
            token_uri=self.token_uri
        )

        storage = Storage('credentials_clover.dat')
        credentials = storage.get()
        parser = argparse.ArgumentParser(parents=[tools.argparser])
        flags = parser.parse_args()

        # Set port
        url = urlparse(self.redirect_uri)
        flags.auth_host_port = [url.port] if url.port else [5000]
        flags.auth_host_name = url.hostname if url.hostname else 'localhost'

        if credentials is None or credentials.invalid:
            credentials = tools.run_flow(flow, storage, flags)
        self.http = credentials.authorize(self.http)
        self.api_token = credentials.__dict__['access_token']

    # HTTP
    def request(self, uri, method, headers=None, body=None):
        """Send the authentificated request to the  API and
           deal with error code and JSON conversion of response.
           headers and body are already urlencoded!
           method are standards HTTP methods
        """

        authorization_bearer = {"Authorization": "Bearer " + self.api_token}

        if not headers:
            headers = authorization_bearer
        elif headers and isinstance(headers, dict):
            headers.update(authorization_bearer)

        response, content = self.http.request(self.api_uri + uri, method, headers=headers, body=body)

        if self.debug:
            print "Request:", uri, headers, body
            print "Response:", response, content

        status_code = int(response['status'])
        try:
            content = json.loads(content)
        except json.JSONDecodeError:
            pass

        # Success
        if status_code in [200, 201]:
            return content
        elif 204 == status_code:
            # Your request was processed but doesn't return any information/object (e.g when you delete an object)
            return None

        # Redirection
        if 302 == status_code:
            try:
                return self.GET(response['location'].split('?')[0])
            except KeyError:
                status_code = 404
                content = response

        # Error
        if self.debug:
            print 'ERROR: request failled at URI', uri

        status_exceptions = {
            400: CloverBadRequest,
            401: CloverUnauthorized,
            403: CloverAccessDenied,
            404: CloverNotFound,
            409: CloverConflict,
            500: CloverInternalServerError
        }

        if status_code in status_exceptions:
            raise status_exceptions[status_code], content
        else:
            raise CloverUnknown, content

    def _HTTP(self, uri, method, json_obj=None):
        """Helper function for HTTP method taking care to encode JSON obj into
           string if it was not already done.
           If json_obj is not a str, unicode or a valid json object will
           propagate the JSON exception ValueError.
        """

        if json_obj:
            if not type(json_obj) in (unicode, str):
                json_obj = json.dumps(json_obj)
            return self.request(uri, method, {'Content-type': 'application/json', 'Accept': 'text/plain'}, json_obj)
        else:
            return self.request(uri, method)

    def GET(self, uri, json_obj=None):
        return self._HTTP(uri, 'GET', json_obj)

    def DELETE(self, uri, json_obj=None):
        return self._HTTP(uri, 'DELETE', json_obj)

    def POST(self, uri, json_obj=None):
        return self._HTTP(uri, 'POST', json_obj)

    def PUT(self, uri, json_obj=None):
        return self._HTTP(uri, 'PUT', json_obj)

    # Clover API (https://www.clover.com/api_docs/)

    # MERCHANTS ()
    def get_merchant(self, merchant_id):
        print locals()
        return self.GET('/v3/merchants/{mId}'.format(mId=merchant_id))

    # ITEMS ()
    def get_items(self):
        return self.GET('/v3/merchants/{mId}/items'.format(mId=self.merchant_id))

    # CATEGORIES ()
    def get_categories(self):
        return self.GET('/v3/merchants/{mId}/categories'.format(mId=self.merchant_id))

    def get_category(self, category_id):
        return self.GET('/v3/merchants/{mId}/categories/{catId}'.format(
            mId=self.merchant_id, catId=category_id))

    # ORDERS (https://www.clover.com/api_docs/#!/orders/)
    def get_orders(self):
        return self.GET('/v3/merchants/{mId}/orders'.format(mId=self.merchant_id))

    def create_order(self):  ## Don't work!!!
        return self.POST('/v3/merchants/{mId}/orders/'.format(mId=self.merchant_id), {"state": "open"})

    def get_order(self, order_id):
        values = {'mId': self.merchant_id, 'orderId': order_id}
        return self.GET('/v3/merchants/{mId}/orders/{orderId}'.format(**values))

    # EXPORT ()
    def create_export(self, export_type, start_time, end_time):
        return self.POST('/v3/merchants/{mId}/exports/'.format(mId=self.merchant_id), {
            'type': export_type,
            'startTime': start_time,
            'endTime': end_time,
        })

    def get_export(self, export_id):
        return self.GET('/v3/merchants/{mId}/exports/{exportId}'.format(
            mId=self.merchant_id, exportId=export_id))