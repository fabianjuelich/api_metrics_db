from enum import StrEnum, auto
import requests
import tokens

class METRICS(StrEnum):
    REVENUE_GROWTH = auto()
    GROSS_PROFIT = auto()
    RETURN_ON_EQUITY = auto()
    EQUITY_RATIO = auto()
    GEARING_RATIO = auto()
    MARKET_CAPITALIZATION = auto()
    ENTERPRISE_VALUE = auto()
    EV_TO_SALES = auto()
    EV_TO_EBITDA = auto()
    PRICE_TO_EARNINGS = auto()
    PRICE_TO_BOOK_VALUE = auto()
    PRICE_TO_CASHFLOW = auto()

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

    leeway = dict(zip(list(METRICS), [
            ('Highlights', 'QuarterlyRevenueGrowthYOY'),
            ('Highlights', 'grossProfit'),
            ('Highlights', 'ReturnOnEquityTTM'),
            (),
            (),
            ('Highlights', 'MarketCapitalization'),
            ('Valuation', 'EnterpriseValue'),
            ('Valuation', 'EnterpriseValueRevenue'),
            ('Valuation', 'EnterpriseValueEbitda'),
            ('Highlights', 'PERatio'),
            ('Valuation', 'PriceBookMRQ'),
            ()
    ]))

    def __init__(self):
        self.url = 'https://api.leeway.tech/api/v1/public/'
        self.data = None

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
                print('INFO: OK')   # ToDo: use custom exceptions
            case 401:
                raise Exception('ERROR: UNAUTHORIZED')
            case 429:
                raise Exception('ERROR: TOO MANY REQUESTS')
        self.data = r.json()
        
    def metrics(self):
        return(self.data)
