import assets.credential as cred
from src.function import Function
from src.fiscal import Fiscal
from src.indicator import Indicator as Ind, indicators as inds
import requests
import json

def alpha_vantage(function, symbol, apikey=cred.apikey):
    url = f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={apikey}'
    r = requests.get(url, timeout=60)
    if not r: raise Exception ("False Symbol"+':' + symbol)
    data = r.json()
    return data

def get_report(symbol, function: Function, fiscal: Fiscal=None, fiscalDateEnding=None):
    if function in [Function.BALANCE_SHEET, Function.CASH_FLOW, Function.INCOME_STATEMENT]:
        if fiscal and fiscalDateEnding:
            try:  
                reports = alpha_vantage(function, symbol)[fiscal]
                for report in reports:
                    if report['fiscalDateEnding'] == fiscalDateEnding:
                        return report
            except:
                Exception("Fiscal or FiscaleDateEnding wrong")
        else:
            raise Exception("Fiscal or FiscalDateEnding missing")
    else:
        return alpha_vantage(function, symbol)

def get_currency(report):
    return report['reportedCurrency']

def revenue_growth(symbol, fiscal: Fiscal, fiscalDateEnding1, fiscalDateEnding2):
    t1 = get_report(symbol, inds[Ind.REVENUE_GROWTH].function, fiscal, fiscalDateEnding1)
    t2 = get_report(symbol, inds[Ind.REVENUE_GROWTH].function, fiscal, fiscalDateEnding2)
    return f'{round(int(t2[inds[Ind.REVENUE_GROWTH].key])/int(t1[inds[Ind.REVENUE_GROWTH].key]), 2)-1:.0%}'

def gross_profit(symbol, fiscal: Fiscal, fiscalDateEnding):
    report = get_report(symbol, inds[Ind.GROSS_PROFIT].function, fiscal, fiscalDateEnding)
    return report[inds[Ind.GROSS_PROFIT].key], get_currency(report)

def return_on_equity(symbol):
    report = get_report(symbol, inds[Ind.RETURN_ON_EQUITY].function)
    return report[inds[Ind.RETURN_ON_EQUITY].key]

def equity_ratio(symbol, fiscal: Fiscal, fiscalDateEnding):
    totShareEqu = get_report(symbol, inds[Ind.EQUITY_RATIO][0].function, fiscal, fiscalDateEnding)[inds[Ind.EQUITY_RATIO][0].key]
    totAss = get_report(symbol, inds[Ind.EQUITY_RATIO][1].function, fiscal, fiscalDateEnding)[inds[Ind.EQUITY_RATIO][1].key]
    return round(int(totShareEqu)/int(totAss), 2)

# Test functions
print(revenue_growth('AAPL', Fiscal.ANNUAL_REPORTS, '2021-09-30', '2022-09-30'))
print(gross_profit('IBM', Fiscal.ANNUAL_REPORTS, '2022-12-31'))
print(return_on_equity('AMZN'))
print(equity_ratio('IBM', Fiscal.ANNUAL_REPORTS, '2022-12-31'))

# Test exceptions
# alpha_vantage(Function.BALANCE_SHEET, "IBZ")
# get_report("IBM", Function.BALANCE_SHEET, Fiscal.ANNUAL_REPORTS, fiscalDateEnding= '2022-08-31')
