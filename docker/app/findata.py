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

    __financialmodellingprep = dict(zip(list(METRICS), [
        ('income-statement-growth', 0, 'growthRevenue'),
        ('income-statement', 0, 'grossProfit'),
        ('key-metrics', 0, 'roe'),
        ('key-metrics', 0, 'debtToEquity'), # ToDo: equity ratio
        ('key-metrics', 0, 'debtToEquity'), # ToDo
        ('key-metrics', 0, 'marketCap'),
        ('key-metrics', 0, 'enterpriseValue'),
        ('key-metrics', 0, 'evToSales'),
        ('key-metrics', 0, 'enterpriseValueOverEBITDA'),
        ('key-metrics', 0, 'revenuePerShare'),
        ('key-metrics', 0, 'bookValuePerShare'),
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
        for metric in METRICS:
            match(metric):
                # given
                case _:
                    result[metric.value] = get_value_by_list(self.data, self.__financialmodellingprep[metric])
        return(result)
    
    def sector(self):
        return self.data['profile'][0]['sector']
    
    def industry(self):
        return self.data['profile'][0]['industry']
    
    def ipo(self):
        return None # self.data['company-outlook'][0]['ipoDate'] # premium feature


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
        for metric in METRICS:
            match(metric):
                # not given
                case METRICS.EQUITY_RATIO:
                    shareholders_equity = get_value_by_list(self.data, self.__leeway[metric]['SHAREHOLDERS_EQUITY'])
                    total_assets = get_value_by_list(self.data, self.__leeway[metric]['LIABILITIES'])
                    result[metric.value] = shareholders_equity / (total_assets + shareholders_equity)
                case METRICS.GEARING_RATIO:
                    shareholders_equity = get_value_by_list(self.data, self.__leeway[metric]['SHAREHOLDERS_EQUITY'])
                    debt = get_value_by_list(self.data, self.__leeway[metric]['DEBT'])
                    result[metric.value] = debt / shareholders_equity
                case METRICS.PRICE_TO_CASHFLOW:
                    market_capitalization = get_value_by_list(self.data, self.__leeway[metric]['MARKET_CAPITALIZATION'])
                    cashflow = get_value_by_list(self.data, self.__leeway[metric]['CASHFLOW'])
                    result[metric.value] = market_capitalization / cashflow
                # given
                case _:
                    result[metric.value] = get_value_by_list(self.data, self.__leeway[metric])
        return(result)

    def sector(self):
        return self.data['General']['Sector']

    def industry(self):
        return self.data['General']['Industry']

    def ipo(self):
        return self.data['General']['IPODate']
