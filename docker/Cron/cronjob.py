#!/usr/bin/python3
from xmlrpc.client import ServerProxy
from elasticsearch import Elasticsearch
from type import TYPE
from api import API
from datetime import date

# setup
es = Elasticsearch("http://elasticsearch:9200")
ser = ServerProxy('http://localhost:2900', allow_none=True)  # ToDo: "http://app:2900"

def store(doc, ident):
    print('doc:', doc)
    return  # ToDo: remove later
    res = es.index(
        index="lazy-investor",
        id = ident,
        document=doc
    )

def rpc(typ: TYPE, symbol: str, country: str, api: API):
    ident = f'{str(date.today())}_{typ.name}_{(symbol+"_") if symbol else ""}{(country+"_") if country else ""}{api.name}'
    print(ident)
    doc = ser.metrics(typ.value, symbol, country, api.value)
    store(doc, ident)

# example calls and storing
rpc(TYPE.INDEX, 'NDX', None, API.LEEWAY)
rpc(TYPE.MARKET, None, 'DE', API.LEEWAY)
rpc(TYPE.STOCK, 'AAPL', 'US', API.LEEWAY)