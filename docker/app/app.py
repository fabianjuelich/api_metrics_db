import findata as findata
import ss as ss
from sort import Sort

def document(typ: Sort, symbol: str, country_code: str, api: findata.Findata):
    symbol = symbol.upper() if symbol else None
    country_code = country_code.lower() if country_code else None
    data = {}
    match(typ):
        case Sort.INDEX:
            index_symbols = ss.index_symbols_json[symbol]
            stock_indices = ss.stock_indices(index_symbols['information']['abbreviation'])
            for component in index_symbols['components']:
                api.get(component, index_symbols['components'][component]['exchange'])
                data[component] = {}
                data[component]['sector'] = api.sector()
                data[component]['industry'] = api.industry()
                data[component]['indices'] = stock_indices[component]
                data[component]['metrics'] = api.metrics()
        case Sort.MARKET:
            market_symbols = ss.market_symbols_json[country_code]
            stock_indices = ss.stock_indices(country_code)
            for component in market_symbols['components']:
                api.get(component, market_symbols['components'][component]['exchange'])
                data[component] = {}
                data[component]['sector'] = api.sector()
                data[component]['industry'] = api.industry()
                data[component]['indices'] = stock_indices[component]
                data[component]['metrics'] = api.metrics()
        case Sort.STOCK:
            api.get(symbol, ss.market_symbols_json[country_code]['components'][symbol]['exchange'])
            data[symbol] = {}
            data[symbol]['sector'] = api.sector()
            data[symbol]['industry'] = api.industry()
            data[symbol]['indices'] = ss.stock_indices(country_code)[symbol]
            data[symbol]['metrics'] = api.metrics()
    return data

# tests #
# print(document(Sort.INDEX, 'NDX', None, findata.Leeway()))
# print(document(Sort.MARKET, None, 'de', findata.Leeway()))
# print(document(Sort.STOCK, 'IBM', 'US', findata.Leeway()))