import findata as findata
import ss as ss
from sort import Sort

def document(sort: Sort, symbols: str, country_codes: str, api: findata.Findata):
    # transfrom symbols
    if symbols:
        if not type(symbols) == list:
            symbols = [symbols]
        for i, s in enumerate(symbols):
            symbols[i] = s.upper()
    # transform country codes
    if country_codes:
        if not type(country_codes) == list:
            country_codes = [country_codes]
        for i, c in enumerate(country_codes):
            country_codes[i] = c.lower()
    # result list
    data = []
    # match sort
    match(sort):
        case Sort.INDEX:
            for s in symbols:
                index_symbols = ss.index_symbols_json[s]
                stock_indices = ss.stock_indices(index_symbols['information']['abbreviation'])
                for component in index_symbols['components']:
                    try:
                        api.get(component, exchange=index_symbols['components'][component]['exchange'])
                        new = {}
                        new['symbol'] = component
                        new['sector'] = api.sector()
                        new['industry'] = api.industry()
                        new['indices'] = stock_indices[component]
                        new['metrics'] = api.metrics()
                        data.append(new)
                    except:
                        print(component, 'not found')
        case Sort.MARKET:
            for c in country_codes:
                market_symbols = ss.market_symbols_json[c]
                stock_indices = ss.stock_indices(c)
                for component in market_symbols['components']:
                    try:
                        api.get(component, exchange=market_symbols['components'][component]['exchange'])
                        new = {}
                        new['symbol'] = component
                        new['sector'] = api.sector()
                        new['industry'] = api.industry()
                        new['indices'] = stock_indices[component]
                        new['metrics'] = api.metrics()
                        data.append(new)
                    except:
                        print(component, 'not found')
        case Sort.STOCK:
            for s in symbols:
                try:
                    api.get(s, exchange=ss.market_symbols_json[country_codes]['components'][s]['exchange'])
                    new = {}
                    new['symbol'] = s
                    new['sector'] = api.sector()
                    new['industry'] = api.industry()
                    new['indices'] = ss.stock_indices(country_codes)[s]
                    new['metrics'] = api.metrics()
                    data.append(new)
                except:
                    print(s, 'not found')
    return data
