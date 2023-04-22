import assets.credential as cred
from src.function import Function
from src.fiscal import Fiscal
from src.indicator import Indicator as Ind, indicators as inds
import requests
import json

def alpha_vantage(function, symbol, interval=None, apikey=cred.apikey):
    base = f'https://www.alphavantage.co/query?function={function.upper()}&symbol={symbol}'
    inter = f'&interval={interval}min'
    key = f'&apikey={apikey}'
    url = base + (inter if interval else '') + key
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

def get_latest_series(symbol, function: Function=Function.TIME_SERIES_INTRADAY, interval=5):
    lastTimeSeries = alpha_vantage(function, symbol, interval=interval)[f'Time Series ({interval}min)']
    return lastTimeSeries[list(lastTimeSeries)[0]]

def get_currency(report):
    try:
        return report['reportedCurrency']
    except:
        return report['Currency']

def revenue_growth(symbol, fiscal: Fiscal, fiscalDateEnding1, fiscalDateEnding2):
    t1 = get_report(symbol, inds[Ind.REVENUE_GROWTH].function, fiscal, fiscalDateEnding1)
    t2 = get_report(symbol, inds[Ind.REVENUE_GROWTH].function, fiscal, fiscalDateEnding2)
    return f'{round((int(t2[inds[Ind.REVENUE_GROWTH].key])-int(t1[inds[Ind.REVENUE_GROWTH].key]))/int(t1[inds[Ind.REVENUE_GROWTH].key]), 4):.0%}'

def gross_profit(symbol, fiscal: Fiscal, fiscalDateEnding):
    # calc
    totRev_rep = get_report(symbol, inds[Ind.GROSS_PROFIT][0].function, fiscal, fiscalDateEnding)
    costOfRev_rep = get_report(symbol, inds[Ind.GROSS_PROFIT][1].function, fiscal, fiscalDateEnding)
    gp = int(totRev_rep[inds[Ind.GROSS_PROFIT][0].key]) - int(costOfRev_rep[inds[Ind.GROSS_PROFIT][1].key]), get_currency(totRev_rep) if get_currency(totRev_rep) == get_currency(costOfRev_rep) else None

    # given
    rep = get_report(symbol, Function.INCOME_STATEMENT, fiscal, fiscalDateEnding)
    gp_av = rep['grossProfit'], get_currency(rep)

    return gp, gp_av

def return_on_equity(symbol, fiscal: Fiscal, fiscalDateEnding):
    # calc
    netInc = int(get_report(symbol, inds[Ind.RETURN_ON_EQUITY][0].function, fiscal, fiscalDateEnding)[inds[Ind.RETURN_ON_EQUITY][0].key])
    totShareEqu = int(get_report(symbol, inds[Ind.RETURN_ON_EQUITY][1].function, fiscal, fiscalDateEnding)[inds[Ind.RETURN_ON_EQUITY][1].key])
    roe = round(netInc/totShareEqu, 4)

    # given
    rep = get_report(symbol, Function.COMPANY_OVERVIEW)
    roe_av = float(rep['ReturnOnEquityTTM'])

    return roe, roe_av

def equity_ratio(symbol, fiscal: Fiscal, fiscalDateEnding):
    # calc with liabilities
    totShareEqu = int(get_report(symbol, inds[Ind.EQUITY_RATIO][0].function, fiscal, fiscalDateEnding)[inds[Ind.EQUITY_RATIO][0].key])
    totLiab = int(get_report(symbol, inds[Ind.EQUITY_RATIO][1].function, fiscal, fiscalDateEnding)[inds[Ind.EQUITY_RATIO][1].key])
    equRat = round(totShareEqu/(totLiab+totShareEqu), 4)

    # calc with current & non current assets
    totCurAss =  int(get_report(symbol, inds[Ind.EQUITY_RATIO][2].function, fiscal, fiscalDateEnding)[inds[Ind.EQUITY_RATIO][2].key])
    totNonCurAss = int(get_report(symbol, inds[Ind.EQUITY_RATIO][3].function, fiscal, fiscalDateEnding)[inds[Ind.EQUITY_RATIO][3].key])
    equRat_curr = round(totShareEqu/(totCurAss+totNonCurAss), 4)

    # given
    totAss = int(get_report(symbol, Function.BALANCE_SHEET, fiscal, fiscalDateEnding)['totalAssets'])
    equRat_av = round(totShareEqu/totAss, 4)

    return equRat, equRat_curr, equRat_av

def market_capitalization(symbol):
    # calc
    close_ser = get_latest_series(symbol, inds[Ind.MARKET_CAPITALIZATION][0].function)
    close = float(close_ser[inds[Ind.MARKET_CAPITALIZATION][0].key])
    num_rep = get_report(symbol, inds[Ind.MARKET_CAPITALIZATION][1].function)
    num = int(num_rep[inds[Ind.MARKET_CAPITALIZATION][1].key])
    markCap = round(close * num, 4)

    # given
    rep = get_report(symbol, Function.COMPANY_OVERVIEW)
    markCap_av = rep['MarketCapitalization']

    return markCap, markCap_av


# Test functions
print(revenue_growth('IBM', Fiscal.ANNUAL_REPORTS, '2021-12-31', '2022-12-31'))
print(gross_profit('IBM', Fiscal.ANNUAL_REPORTS, '2022-12-31'))
print(return_on_equity('IBM', Fiscal.ANNUAL_REPORTS, '2022-12-31'))
print(equity_ratio('IBM', Fiscal.ANNUAL_REPORTS, '2022-12-31'))
print(market_capitalization('IBM'))

# Test exceptions
#alpha_vantage(Function.BALANCE_SHEET, "IBZ")
#get_report("IBM", Function.BALANCE_SHEET, Fiscal.ANNUAL_REPORTS, fiscalDateEnding= '2022-08-31')
