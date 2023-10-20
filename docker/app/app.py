import findata as findata
import ss as ss
from sort import Sort
from datetime import datetime

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

    data = []

    def new(symbol: str, indices: list):
        new = {}
        new['symbol'] = symbol
        new['sector'] = api.sector()
        new['industry'] = api.industry()
        new['ipo'] = api.ipo()
        new['indices'] = indices
        new['metrics'] = api.metrics()
        new['timestamp'] = datetime.now().isoformat()
        return new

    match(sort):

        case Sort.INDEX:
            for s in symbols:
                index_symbols = ss.index_symbols_json[s]
                stock_indices = ss.stock_indices(index_symbols['information']['abbreviation'])
                for component in index_symbols['components']:
                    try:
                        api.get(component, exchange=index_symbols['components'][component]['exchange'])
                        data.append(new(component, stock_indices[component]))
                    except Exception as e:
                        # raise e
                        print(component, 'not found')

        case Sort.MARKET:
            for c in country_codes:
                market_symbols = ss.market_symbols_json[c]
                stock_indices = ss.stock_indices(c)
                for component in market_symbols['components']:
                    try:
                        api.get(component, exchange=market_symbols['components'][component]['exchange'])
                        data.append(new(component, stock_indices[component]))
                    except Exception as e:
                        # raise e
                        print(component, 'not found')

        case Sort.STOCK:
            for s in symbols:
                try:
                    api.get(s, exchange=ss.market_symbols_json[country_codes[0]]['components'][s]['exchange'])
                    data.append(new(s, ss.stock_indices(country_codes[0])[s]))
                except Exception as e:
                    # raise e
                    print(component, 'not found')
                    
    return data
