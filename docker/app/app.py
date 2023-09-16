import findata as findata
import ss as ss
from type import TYPE

def document(typ: TYPE, symbol: str, country_code: str, api: findata.Findata):
    symbol = symbol.upper() if symbol else None
    country_code = country_code.lower() if country_code else None
    data = {}
    match(typ):
        case TYPE.INDEX:
            index_symbols = ss.index_symbols_json[symbol]
            stock_indices = ss.stock_indices(index_symbols['information']['abbreviation'])
            for component in index_symbols['components']:
                api.get(component, index_symbols['components'][component]['exchange'])
                if not api.sector() in data:
                    data[api.sector()] = {}
                data[api.sector()][component] = {}
                data[api.sector()][component]['indices'] = stock_indices[component]
                data[api.sector()][component]['metrics'] = api.metrics()
        case TYPE.MARKET:
            market_symbols = ss.market_symbols_json[country_code]
            stock_indices = ss.stock_indices(country_code)
            for component in market_symbols['components']:
                api.get(component, market_symbols['components'][component]['exchange'])
                if not api.sector() in data:
                    data[api.sector()] = {}
                data[api.sector()][component] = {}
                data[api.sector()][component]['indices'] = stock_indices[component]
                data[api.sector()][component]['metrics'] = api.metrics()
                break
        case TYPE.STOCK:
            api.get(symbol, ss.market_symbols_json[country_code]['components'][symbol]['exchange'])
            if not api.sector() in data:
                data[api.sector()] = {}
            data[api.sector()]['indices'] = ss.stock_indices(country_code)[symbol]
            data[api.sector()]['metrics'] = api.metrics()
    return data

# tests #
# print(document(TYPE.INDEX, 'NDX', None, findata.Leeway()))
# print(document(TYPE.MARKET, None, 'de', findata.Leeway()))
# print(document(TYPE.STOCK, 'IBM', 'US', findata.Leeway()))