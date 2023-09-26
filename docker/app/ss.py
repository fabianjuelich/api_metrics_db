from stocksymbol import StockSymbol
import tokens as tokens
import json
import os

# API setup #

api_key = tokens.stocksymbol
ss = StockSymbol(api_key)

# custom functions #

# joins index list with symbol list by matching index symbol
def index_symbols(indices=None):
    index_list = ss.index_list
    if indices:
        if type(indices) != list:
            indices = [indices]
        index_list = [index_list[i] for i, index in enumerate(index_list) if index['indexId'] in indices]
    indices_json = {}
    for index in index_list:
        symbol = index['indexId']
        indices_json[symbol] = {}
        indices_json[symbol]['information'] = index
        try:
            indices_json[symbol]['components'] = dict(map(lambda s: (s['symbol'], s), ss.get_symbol_list(index=symbol)))
            indices_json[symbol]['information']['totalCount'] = len(indices_json[symbol]['components'])
        except:
            indices_json[symbol]['components'] = None
            print('WARNING:', symbol, 'not found.')
    return indices_json

# joins market list with symbol list by matching market country
def market_symbols(markets=None):
    market_list = ss.market_list
    if markets:
        if type(markets) != list:
            markets = [markets]
        market_list = [market_list[m] for m, market in enumerate(market_list) if market['abbreviation'] in markets]
    markets_json = {}
    for market in market_list:
        country = market['abbreviation']
        markets_json[country] = {}
        markets_json[country]['information'] = market
        try:
            markets_json[country]['components'] = dict(map(lambda s: (s['symbol'], s), ss.get_symbol_list(market=country)))
        except Exception as e:
            markets_json[country]['components'] = None
            print('WARNING:', country, 'not found.')
    return markets_json

# lists stock symbols of a market with the indices in which it is listed
def stock_indices(market):
    stock_json = dict(map(lambda component: (component, []), market_symbols_json[market]['components']))
    for symbol in stock_json:
        for index in index_symbols_json:
            if index_symbols_json[index]['information']['abbreviation'] == market\
            and symbol in index_symbols_json[index]['components']:
                stock_json[symbol].append(index)
    return stock_json
    # for key, value in symbols_index.items():
    #     print(key)
    #     print(value)
    # print(len(symbols_index))

# variables initialization #

try:
    # retrieve latest data
    raise Exception # ToDo: remove later (only added for faster execution)
    index_list_json = ss.index_list
    market_list_json = ss.market_list
    index_symbols_json = index_symbols()
    market_symbols_json = market_symbols()
    # stock_indices_json = stock_indices()  # ToDo: rework function to be generic
except Exception as e:
    print(e)
    # read backup data which was retrieved by above functions
    print('WARNING: stock-symbol: API not reachable')
    try:
        with open(os.path.join(os.path.dirname(__file__), 'backup/index_symbols.json'), 'r') as index_s, \
            open(os.path.join(os.path.dirname(__file__),'backup/market_symbols.json'), 'r') as market_s, \
            open(os.path.join(os.path.dirname(__file__),'backup/index_list.json'), 'r') as index_l, \
            open(os.path.join(os.path.dirname(__file__),'backup/market_list.json'), 'r') as market_l, \
            open(os.path.join(os.path.dirname(__file__),'backup/stock_indices.json'), 'r') as stock_i:
            index_list_json = json.load(index_l)
            market_list_json = json.load(market_l)
            index_symbols_json = json.load(index_s)
            market_symbols_json = json.load(market_s)
            stock_indices_json = json.load(stock_i)
    except:
        raise Exception('ERROR: stock-symbol: Backup-files not found')

# example usage of custom functions #

# print(json.dumps(index_symbols(['DAX', 'IXIC']), indent=4))
# print(json.dumps(market_symbols('de'), indent=4))

# file generation #

# with open('index_list.json', 'w') as f:
#     f.write(json.dumps(ss.index_list, indent=4))

# with open('market_list.json', 'w') as f:
#     f.write(json.dumps(ss.market_list, indent=4))

# with open('market_symbols.json', 'w') as f:
#     f.write(json.dumps(market_symbols(), indent=4))

# with open('index_symbols.json', 'w') as f:
#     f.write(json.dumps(index_symbols(), indent=4))

# with open('stock_index.json', 'w') as f:
#     f.write(json.dumps(stock_indices('us'), indent=4))
