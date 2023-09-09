from enum import StrEnum
import requests
import tokens

class Findata():
    def get():
        pass
    def metrics():
        pass

class AlphaVantage(Findata):
    pass

class FinancialModelingPrep(Findata):
    pass

class Leeway(Findata):
    def __init__(self):
        self.url = 'https://api.leeway.tech/api/v1/public/'

    def get(self, symbol, exchange, typ='fundamentals', token=tokens.leeway, lang='english', fmt='JSON'):
        url = self.url + f'{typ}/{symbol}.{exchange}'
        params = {
            'apitoken': token,
            'lang': lang,
            'fmt': fmt
        }
        r = requests.get(url, params=params, timeout=60)
        match(r.status_code):
            case 200:
                print('INFO: OK')
            case 401:
                raise Exception('ERROR: UNAUTHORIZED')
            case 429:
                raise Exception('ERROR: TOO MANY REQUESTS')
        self.metrics(r.json())
        
    def metrics(self, data):
        print(data)
        pass

    # class __METRICS(StrEnum):
    #     REVENUE_GROWTH = 'QuarterlyRevenueGrowthYOY'    # Highlights
    #     GROSS_PROFIT = 'grossProfit'    # Highlights
    #     RETURN_ON_EQUITY = 'ReturnOnEquityTTM'  # Highlights
    #     EQUITY_RATIO = None
    #     GEARING_RATIO = None
    #     MARKET_CAPITALIZATION = 'MarketCapitalization'
    #     ENTERPRISE_VALUE = 'EnterpriseValue'    # Valuation
    #     EV_TO_SALES = 'EnterpriseValueRevenue'  # Valuation
    #     EV_TO_EBITDA = 'EnterpriseValueEbitda'  # Valuation
    #     PRICE_TO_EARNINGS = 'PERatio'           # Highlights
    #     PRICE_TO_BOOK_VALUE = 'PriceBookMRQ'    # Valuation
    #     PRICE_TO_CASHFLOW = None
