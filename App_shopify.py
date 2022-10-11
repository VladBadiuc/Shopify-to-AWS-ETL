#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 13:28:29 2022

@author: vladbad
"""

import requests
import credentials
import pandas as pd
import numpy as np
import schedule
import time

shop_url = "https://%s:%s@AppStoreXX.myshopify.com/admin/api/2022-07/" % (credentials.API_KEY, credentials.PASSWORD)
customers_table = []
orders_table = []

def get_draft_orders():
    #endpoint = 'products.json'
    endpoint = 'draft_orders.json'
    r = requests.get(shop_url + endpoint)
    print(r)
    return r.json()

def get_customers():
    #endpoint = 'products.json'
    endpoint = 'customers.json'
    r = requests.get(shop_url + endpoint)
    print(r)
    return r.json()

