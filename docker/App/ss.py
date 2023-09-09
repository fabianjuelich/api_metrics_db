from stocksymbol import StockSymbol
import tokens
import json

# insert your API key
api_key = tokens.stocksymbol
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
        indices_json[symbol] = {}
        indices_json[symbol]['information'] = index
        try:
            indices_json[symbol]['components'] = ss.get_symbol_list(index=symbol)
            indices_json[symbol]['information']['totalCount'] = len(indices_json[symbol]['components'])
        except:
            indices_json[symbol]['components'] = None
            print('WARNING:', symbol, 'not found.')
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
        markets_json[country] = {}
        markets_json[country]['information'] = market
        try:
            markets_json[country]['components'] = ss.get_symbol_list(market=country)
        except:
            markets_json[country] = None
            print('WARNING:', country, 'not found.')
    return markets_json

try:
    # retrieve latest data
    index_list_json = ss.index_list
    market_list_json = ss.market_list
    indices_symbols_json = index_symbols()
    markets_symbols_json = market_symbols()
except:
    print('WARNING: API not responding')
    # read backup data which was retrieved by above functions
    try:
        with open('./data/index_symbols.json', 'r') as index_s, open('./data/market_symbols.json', 'r') as market_s, open('./data/index_list.json', 'r') as index_l, open('./data/market_list.json', 'r') as market_l:
            index_list_json = json.load(index_l)
            market_list_json = json.load(market_l)
            indices_symbols_json = json.load(index_s)
            markets_symbols_json = json.load(market_s)
    except:
        raise Exception('ERROR: Backup-files not found')

# lists stock symbols of a market with the indices in which it is listed
def stock_indices(market):
    stock_json = {}
    for component in markets_symbols_json[market]['components']:
        # if not component['market'] == f'{market}_market': continue
        stock_json[component['symbol']] = []
    for symbol in stock_json:
        for index in indices_symbols_json:
            if indices_symbols_json[index]['information']['abbreviation'] != market: continue
            for component in indices_symbols_json[index]['components']:
                if component['symbol'] == symbol:   # and component['market'] == f'{market}_market':
                    stock_json[symbol].append(index)
                    # print(symbol, index)
    return stock_json
    # for key, value in symbols_index.items():
    #     print(key)
    #     print(value)
    # print(len(symbols_index))


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
