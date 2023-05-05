import json

context: str

with open('assets/context.json') as j:
    context = json.load(j)

def get_indicator_context(function, type):
    return context[type][function]
