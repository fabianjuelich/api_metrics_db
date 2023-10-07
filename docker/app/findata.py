from enum import StrEnum, auto
import requests
import tokens
import json
import os
# include previous project #
from archive.WI_Projekt_SS23_Juelich_Kalacevic.src.table import Table
from archive.WI_Projekt_SS23_Juelich_Kalacevic.src.enums.source import Source

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

# save typing #

def get_value_by_list(j: dict, l: list):
    value = j
    for key in l:
        value = value[key]
    return float(value)

# parent class #

class Findata():
    def get():
        pass
    def metrics():
        pass
    def sector():
        pass
    def industry():
        pass

# child classes #

class AlphaVantage(Findata):

    def get(self, symbol):
        self.data = Table(symbol).get_dict_meta(Source.GIVEN)[symbol]

    def metrics(self):
        return self.data['metrics']
    
    def sector(self):
        return self.data['metadata']['sector']
    
    def industry(self):
        return self.data['metadata']['industry']

class FinancialModelingPrep(Findata):
    pass    # ToDo

class Leeway(Findata):

    __leeway = dict(zip(list(METRICS), [
            ('Highlights', 'QuarterlyRevenueGrowthYOY'),
            ('Highlights', 'GrossProfitTTM'),
            ('Highlights', 'ReturnOnEquityTTM'),
            {
             'SHAREHOLDERS_EQUITY':('Financials', 'Balance_Sheet', 'quarterly', 0, 'totalStockholderEquity'),
             'LIABILITIES': ('Financials', 'Balance_Sheet', 'quarterly', 0, 'totalLiab')
             },
            {
             'DEBT': ('Financials', 'Balance_Sheet', 'quarterly', 0, 'longTermDebt'),
             'SHAREHOLDERS_EQUITY': ('Financials', 'Balance_Sheet', 'quarterly', 0, 'totalStockholderEquity')
            },
            ('Highlights', 'MarketCapitalization'),
            ('Valuation', 'EnterpriseValue'),
            ('Valuation', 'EnterpriseValueRevenue'),
            ('Valuation', 'EnterpriseValueEbitda'),
            ('Highlights', 'PERatio'),
            ('Valuation', 'PriceBookMRQ'),
            {
             'MARKET_CAPITALIZATION': ('Highlights', 'MarketCapitalization'),
             'CASHFLOW': ('Financials', 'Cash_Flow', 'quarterly', 0, 'totalCashFromOperatingActivities')
            }
    ]))

    def __init__(self):
        self.url = 'https://api.leeway.tech/api/v1/public/'
        self.data = None

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
                # not given
                case METRICS.EQUITY_RATIO:
                    shareholders_equity = get_value_by_list(self.data, self.__leeway[metric]['SHAREHOLDERS_EQUITY'])
                    total_assets = get_value_by_list(self.data, self.__leeway[metric]['LIABILITIES'])
                    result[metric.name] = shareholders_equity / (total_assets + shareholders_equity)
                case METRICS.GEARING_RATIO:
                    shareholders_equity = get_value_by_list(self.data, self.__leeway[metric]['SHAREHOLDERS_EQUITY'])
                    debt = get_value_by_list(self.data, self.__leeway[metric]['DEBT'])
                    result[metric.name] = debt / shareholders_equity
                case METRICS.PRICE_TO_CASHFLOW:
                    market_capitalization = get_value_by_list(self.data, self.__leeway[metric]['MARKET_CAPITALIZATION'])
                    cashflow = get_value_by_list(self.data, self.__leeway[metric]['CASHFLOW'])
                    result[metric.name] = market_capitalization / cashflow
                # given
                case _:
                    result[metric.name] = get_value_by_list(self.data, self.__leeway[metric])
        return(result)

    def sector(self):
        return self.data['General']['Sector']

    def industry(self):
        return self.data['General']['Industry']
    

# test
alpha = AlphaVantage()
alpha.get('AAPL')
print('AAPL')
print(alpha.metrics())
print(alpha.sector())
print(alpha.industry())
