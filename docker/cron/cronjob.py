#!/usr/bin/python3
from xmlrpc.client import ServerProxy
from elasticsearch import Elasticsearch
from type import TYPE
from api import API
from datetime import date
import json

# setup #

es = Elasticsearch('http://elasticsearch:9200')
ser = ServerProxy('http://app:2900', allow_none=True)  # ToDo: 'http://localhost:2900'

def store(doc, ident):
    print(ident, '\n', json.dumps(doc, indent=4))
    return  # ToDo: remove later
    res = es.index(
        index="lazy-investor",
        id = ident,
        document=doc
    )

def rpc(typ: TYPE, symbol: str, country: str, api: API):
    ident = f'{str(date.today())}_{typ.name}_{(symbol+"_") if symbol else ""}{(country+"_") if country else ""}{api.name}'
    doc = json.loads(ser.metrics(typ.value, symbol, country, api.value))
    store(doc, ident)

# example calls/storing #

# rpc(TYPE.INDEX, 'NDX', None, API.LEEWAY)
# rpc(TYPE.MARKET, None, 'DE', API.LEEWAY)
rpc(TYPE.STOCK, 'IBM', 'US', API.LEEWAY)