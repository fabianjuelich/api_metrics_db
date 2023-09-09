import findata
import ss
import json

# find relevant stock exchange automatically
symbols = ss.markets_symbols_json

def document(symbol: str, country_code: str, api: findata.Findata):
    api.get(symbol, symbols[country_code]['components'][symbol]['exchange'])

leeway = findata.Leeway()
document('IBM', 'us', leeway)
