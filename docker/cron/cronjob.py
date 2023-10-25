#!/usr/bin/python3
from xmlrpc.client import ServerProxy
from elasticsearch import Elasticsearch
from sort import Sort
from api import Api
import json

# setup #

es = Elasticsearch('http://elasticsearch:9200')
ser = ServerProxy('http://app:2900', allow_none=True)

def store(data, request):
    print(request, '\n', json.dumps(data, indent=4))
    for doc in data:
        doc['request'] = request
        res = es.index(
            index="lazy-investor",
            document=doc
        )
        print(res)

def rpc(sort: Sort, symbols: str, country_codes: str, api: Api):
    data = json.loads(ser.metrics(sort.value, symbols, country_codes, api.value))
    symbols_format = (('-'.join(symbols) if type(symbols) == list else symbols) + '_') if symbols else ""
    country_codes_format = (('-'.join(country_codes) if type(country_codes) == list else country_codes) + '_') if country_codes else ""
    request = f'{sort.name}_{symbols_format}{country_codes_format}{api.name}'
    store(data, request)

# example calls/storing #

rpc(Sort.INDEX, 'NDX', None, Api.ALPHA_VANTAGE)
rpc(Sort.MARKET, None, 'DE', Api.FINANCIAL_MODELING_PREP)
rpc(Sort.STOCK, 'IBM', 'US', Api.LEEWAY)