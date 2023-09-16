from enum import StrEnum, auto
import requests
import tokens
import json
import os

# exceptions #

class UNAUTHORIZED(Exception):
    pass

class TOO_MANY_REQUESTS(Exception):
    pass

# metrics #

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

# parent class #

class Findata():
    def get():
        pass
    def metrics():
        pass
    def sector():
        pass

# child classes #

class AlphaVantage(Findata):
    pass

class FinancialModelingPrep(Findata):
    pass

class Leeway(Findata):

    __leeway = dict(zip(list(METRICS), [
            ('Highlights', 'QuarterlyRevenueGrowthYOY'),
            ('Highlights', 'GrossProfitTTM'),
            ('Highlights', 'ReturnOnEquityTTM'),
            {'one': (), 'two': ()},
            {'one': (), 'two': ()},
            ('Highlights', 'MarketCapitalization'),
            ('Valuation', 'EnterpriseValue'),
            ('Valuation', 'EnterpriseValueRevenue'),
            ('Valuation', 'EnterpriseValueEbitda'),
            ('Highlights', 'PERatio'),
            ('Valuation', 'PriceBookMRQ'),
            {'one': (), 'two': ()}
    ]))

    def __init__(self):
        self.url = 'https://api.leeway.tech/api/v1/public/'
        self.data = None

        # print(json.dumps(self.__leeway, indent=4))

    def __get(self, symbol, exchange, typ='fundamentals', token=tokens.leeway, lang='english', fmt='JSON'): # ToDo: rename later to get()
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
                raise UNAUTHORIZED
            case 429:
                raise TOO_MANY_REQUESTS
        self.data = r.json()

    def get(self, *args):   # ToDo: remove later
        with open(os.path.join(os.path.dirname(__file__), 'data/leeway.json'), 'r') as f:
            self.data = json.load(f)
        
    def metrics(self):
        result = {}
        for metric in METRICS:
            match(metric):
                case METRICS.EQUITY_RATIO:
                    pass
                case METRICS.GEARING_RATIO:
                    pass
                case METRICS.PRICE_TO_CASHFLOW:
                    pass
                case _:
                    result[metric.name] = self.data[self.__leeway[metric][0]][self.__leeway[metric][1]]
        return(result)

    def sector(self):
        return self.data['General']['Sector']
