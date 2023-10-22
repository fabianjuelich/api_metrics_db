from enum import StrEnum, auto
import requests
import tokens
# include previous project #
from archive.WI_Projekt_SS23_Juelich_Kalacevic.src.table import Table
from archive.WI_Projekt_SS23_Juelich_Kalacevic.src.enums.source import Source

# exceptions #

class UNAUTHORIZED(Exception):
    pass

class TOO_MANY_REQUESTS(Exception):
    pass

# metrics #

class Metrics(StrEnum):
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

def status(code):
    match(code):
        case 200:
            print('INFO: OK')
        case 401:
            raise UNAUTHORIZED
        case 429:
            raise TOO_MANY_REQUESTS

# interface #

class Findata():

    def get(self) -> None:
        pass
    def metrics(self, symbol: str, *args) -> dict:
        pass
    def sector(self) -> str:
        pass
    def industry(self) -> str:
        pass
    def ipo(self) -> str:
        pass

# implementations #

class AlphaVantage(Findata):

    def get(self, symbol, exchange=None, *_):
        self.data = Table(symbol).get_dict_meta(Source.GIVEN)[symbol]

    def metrics(self):
        return self.data['metrics']
    
    def sector(self):
        return self.data['metadata']['sector']
    
    def industry(self):
        return self.data['metadata']['industry']
    
    def ipo(self):
        return self.data['metadata']['ipoDate']


class FinancialModelingPrep(Findata):

    __financialmodellingprep = dict(zip(list(Metrics), [
        ('income-statement-growth', 0, 'growthRevenue'),
        ('income-statement', 0, 'grossProfit'),
        ('key-metrics', 0, 'roe'),
        {
            'STOCKHOLDERS_EQUITY': ('balance-sheet-statement', 0, 'totalStockholdersEquity'),  
            'ASSETS': ('balance-sheet-statement', 0, 'totalAssets')
        },
        ('key-metrics', 0, 'debtToEquity'),
        ('key-metrics', 0, 'marketCap'),
        ('key-metrics', 0, 'enterpriseValue'),
        ('key-metrics', 0, 'evToSales'),
        ('key-metrics', 0, 'enterpriseValueOverEBITDA'),
        ('key-metrics', 0, 'peRatio'),
        ('key-metrics', 0, 'pbRatio'),
        ('key-metrics', 0, 'operatingCashFlowPerShare')
    ]))
    
    def __init__(self):
        self.url = 'https://financialmodelingprep.com/api/'

    def get(self, symbol, exchange=None, docs=['profile', 'income-statement', 'income-statement-growth', 'balance-sheet-statement', 'key-metrics'], version=3, key=tokens.financial_modeling_prep):
        self.data = {}
        params = {
            'apikey': key
        }
        for doc in docs:
            url = self.url + f'v{version}/{doc}/{symbol}'
            res = requests.get(url, params=params, timeout=60)
            self.data[doc] = res.json()
            status(res.status_code)

    def metrics(self):
        result = {}
        for metric in Metrics:
            match(metric):
                # not give
                case Metrics.EQUITY_RATIO:
                    stockholders_equity = get_value_by_list(self.data, self.__financialmodellingprep[metric]['STOCKHOLDERS_EQUITY'])
                    assets = get_value_by_list(self.data, self.__financialmodellingprep[metric]['ASSETS'])
                    res = stockholders_equity / assets
                # given
                case _:
                    res = get_value_by_list(self.data, self.__financialmodellingprep[metric])
            result[metric.value] = res
        return(result)
    
    def sector(self):
        return self.data['profile'][0]['sector']
    
    def industry(self):
        return self.data['profile'][0]['industry']
    
    def ipo(self):
        return None # self.data['company-outlook'][0]['ipoDate'] # premium feature


class Leeway(Findata):

    __leeway = dict(zip(list(Metrics), [
        ('Highlights', 'QuarterlyRevenueGrowthYOY'),
        ('Highlights', 'GrossProfitTTM'),
        ('Highlights', 'ReturnOnEquityTTM'),
        {
            'SHAREHOLDERS_EQUITY':('Financials', 'Balance_Sheet', 'quarterly', 0, 'totalStockholderEquity'),
            'ASSETS': ('Financials', 'Balance_Sheet', 'quarterly', 0, 'totalAssets')
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

    def get(self, symbol, exchange, doc='fundamentals', token=tokens.leeway, lang='english', fmt='JSON'):
        url = self.url + f'{doc}/{symbol}.{exchange}'
        params = {
            'apitoken': token,
            'lang': lang,
            'fmt': fmt
        }
        res = requests.get(url, params=params, timeout=60)
        status(res.status_code)
        self.data = res.json()

    def metrics(self):
        result = {}
        for metric in Metrics:
            match(metric):
                # not given
                case Metrics.EQUITY_RATIO:
                    shareholders_equity = get_value_by_list(self.data, self.__leeway[metric]['SHAREHOLDERS_EQUITY'])
                    assets = get_value_by_list(self.data, self.__leeway[metric]['ASSETS'])
                    res = shareholders_equity / assets
                case Metrics.GEARING_RATIO:
                    shareholders_equity = get_value_by_list(self.data, self.__leeway[metric]['SHAREHOLDERS_EQUITY'])
                    debt = get_value_by_list(self.data, self.__leeway[metric]['DEBT'])
                    res = debt / shareholders_equity
                case Metrics.PRICE_TO_CASHFLOW:
                    market_capitalization = get_value_by_list(self.data, self.__leeway[metric]['MARKET_CAPITALIZATION'])
                    cashflow = get_value_by_list(self.data, self.__leeway[metric]['CASHFLOW'])
                    res = market_capitalization / cashflow
                # given
                case _:
                    res = get_value_by_list(self.data, self.__leeway[metric])
            result[metric.value] = res
        return(result)

    def sector(self):
        return self.data['General']['Sector']

    def industry(self):
        return self.data['General']['Industry']

    def ipo(self):
        return self.data['General']['IPODate']
