# !/usr/bin/env python
# -*- coding: utf-8 -*-

from clover.api import Clover
from config import *

# Authorization with OAuth2
api = Clover(
    api_uri=base_urls['sandbox'],
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    merchant_id=merchant_id,
    debug=True
)


# Call API
items = api.get_items()['elements']
print items