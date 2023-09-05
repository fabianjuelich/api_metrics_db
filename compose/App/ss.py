from stocksymbol import StockSymbol
import json

# insert your API key
api_key = ""
ss = StockSymbol(api_key)

# join index list with symbol list by matching index symbol
def index_symbols(indices=None):
    index_list = ss.index_list
    if indices:
        if type(indices) != list:
            indices = [indices]
        index_list = [index_list[i] for i, index in enumerate(index_list) if index['indexId'] in indices]
    indices_json = {}
    for index in index_list:
        symbol = index['indexId']
        try:
            indices_json[symbol] = {}
            indices_json[symbol]['information'] = index
            indices_json[symbol]['components'] = ss.get_symbol_list(index=symbol)
        except:
            indices_json[symbol] = None
            print(symbol)
    return indices_json

# join market list with symbol list by matching market country
def market_symbols(markets=None):
    market_list = ss.market_list
    if markets:
        if type(markets) != list:
            markets = [markets]
        market_list = [market_list[m] for m, market in enumerate(market_list) if market['abbreviation'] in markets]
    markets_json = {}
    for market in market_list:
        country = market['abbreviation']
        try:
            markets_json[country] = {}
            markets_json[country]['information'] = market
            markets_json[country]['components'] = ss.get_symbol_list(market=country)
        except:
            markets_json[country] = None
            print(country)
    return markets_json

# read backup data which was retrieved by above functions
with open('./../index_symbols.json', 'r') as indices, open('./../market_symbols.json', 'r') as markets:
    indices_json = json.load(indices)
    markets_json = json.load(markets)

# lists stock symbols of a market with the indices in which it is listed
def stock_symbols(market):
    symbols_index = {}
    for component in markets_json[market]['components']:
        if not component['market'] == f'{market}_market': continue  # ToDo: check if filter is necessary
        symbols_index[component['symbol']] = []
    for symbol in symbols_index:
        for index in indices_json:
            if indices_json[index]['information']['abbreviation'] != market: continue
            for component in indices_json[index]['components']:
                if component['symbol'] == symbol and component['market'] == f'{market}_market':   # ToDo: check if second filter is necessary
                    symbols_index[symbol].append(index)
                    # print(symbol, index)
    # for key, value in symbols_index.items():
    #     print(key)
    #     print(value)
    print(len(symbols_index))

stock_symbols('us')

# examples #

# print(json.dumps(market_symbols('de'), indent=4))
# with open('market_symbols.json', 'w') as f:
#     f.write(json.dumps(market_symbols(), indent=4))

# print(json.dumps(index_symbols(['DAX', 'IXIC']), indent=4))
# with open('index_symbols.json', 'w') as f:
#     f.write(json.dumps(index_symbols(), indent=4))
