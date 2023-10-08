#!/usr/bin/python3
from xmlrpc.client import ServerProxy
from elasticsearch import Elasticsearch
from sort import Sort
from api import Api
from datetime import date
import json

# setup #

es = Elasticsearch('http://elasticsearch:9200')
ser = ServerProxy('http://app:2900', allow_none=True)

def store(doc, ident):
    print(ident, '\n', json.dumps(doc, indent=4))
    return  # ToDo: remove later
    res = es.index(
        index="lazy-investor",
        id = ident,
        document=doc
    )

def rpc(typ: Sort, symbol: str, country: str, api: Api):
    ident = f'{str(date.today())}_{typ.name}_{(symbol+"_") if symbol else ""}{(country+"_") if country else ""}{api.name}'
    doc = json.loads(ser.metrics(typ.value, symbol, country, api.value))
    store(doc, ident)

# example calls/storing #

# rpc(Sort.INDEX, 'NDX', None, Api.LEEWAY)
# rpc(Sort.MARKET, None, 'DE', Api.LEEWAY)
# rpc(Sort.STOCK, 'IBM', 'US', Api.LEEWAY)

rpc(Sort.STOCK, 'AAPL', 'US', Api.FINANCIAL_MODELING_PREP)