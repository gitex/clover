# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Settings
merchant_id = 'GY4KX03XFVVYG'  # Your merchant ID
client_id = r'4ZTHEZAYFDKD8'  # App ID
client_secret = r'466fccba-0ff0-9929-6584-b14aac626ce4'  # App Secret
redirect_uri = 'http://127.0.0.1:5000/callback'  # Local or global URL

# List of REST API Endpoints
base_urls = {
    'us': 'https://api.clover.com',
    'eu': 'https://api.eu.clover.com',
    'sandbox': 'https://sandbox.dev.clover.com'
}