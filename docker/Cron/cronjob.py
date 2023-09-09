#!/usr/bin/python3
from xmlrpc.client import ServerProxy
from elasticsearch import Elasticsearch
from datetime import datetime

# setup
es = Elasticsearch("http://elasticsearch:9200")
ser = ServerProxy("http://app:2900")

# example call
doc = ser.metrics()
# example storing
res = es.index(
    index="lazy-investor",
    id ="my_id",
    document=doc
)