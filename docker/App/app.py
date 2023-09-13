import findata as findata
import ss as ss
from type import TYPE
from api import API

def document(typ: TYPE, symbol: str, country_code: str, api: findata.Findata):
    data = {}
    symbol = symbol.upper() if symbol else None
    country_code = country_code.lower() if country_code else None
    match(typ):
        case TYPE.INDEX:
            index_symbols = ss.index_symbols_json[symbol]
            for component in index_symbols['components']:
                api.get(component, index_symbols['components'][component]['exchange'])
                data[component] = api.metrics()
        case TYPE.MARKET:
            market_symbols = ss.market_symbols_json[country_code]
            for component in market_symbols['components']:
                api.get(component, market_symbols['components'][component]['exchange'])
                data[component] = api.metrics()
        case TYPE.STOCK:
            api.get(symbol, ss.market_symbols_json[country_code]['components'][symbol]['exchange'])
            data = api.metrics()
    return data

# print(document(TYPE.STOCK, 'AAPL', 'US', findata.Leeway()))