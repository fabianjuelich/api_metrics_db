import assets.credential as cred
from src.function import Function
from src.fiscal import Fiscal
from src.indicator import Indicator as Ind, indicators as inds
import requests

def alpha_vantage(function, symbol, interval=None, apikey=cred.apikey) -> dict:
    """
    Calls Alpha Vantage API and returns a JSON object containing the result of the request.
    Args:
        function (Function): An enum value representing the function to be called from the Alpha Vantage API.
        symbol (str): The stock symbol for which the function is to be called.
        interval (int, optional): The time interval (in minutes) for which to get the time series data (default None).
        apikey (str, optional): The API key to be used for authentication (default cred.apikey).
    Returns:
        A JSON object containing the result of the API request.
    Raises:
        Exception: If the API returns an error.
    """
    base = f'https://www.alphavantage.co/query?function={function.upper()}&symbol={symbol}'
    inter = f'&interval={interval}min'
    key = f'&apikey={apikey}'
    url = base + (inter if interval else '') + key
    r = requests.get(url, timeout=60)
    data = r.json()
    if list(data.keys())[0] in ['Information', 'Error Message']:
        raise Exception(data)
    return data

def get_latest_report(symbol, function: Function, fiscal: Fiscal=None, fiscalDateEnding=None, index=None):
    """
    Gets the latest report of a given function for a given symbol and fiscal year ending.
    Args:
        symbol (str): The stock symbol for which to get the report.
        function (Function): An enum value representing the function to be called from the Alpha Vantage API.
        fiscal (Fiscal, optional): An enum value representing the fiscal year for which to get the report (default None).
        fiscalDateEnding (str, optional): A string representing the fiscal year ending for which to get the report (default None).
        index (int, optional): The index of the report to be returned (default None).
    Returns:
        The latest report (, the index in case of periodically reports).
    Args:
        Exception: If an error occurs while getting the report or the fiscal date ending is not found.
    """
    try:
        reports = alpha_vantage(function, symbol)
    except Exception as e:
        raise e
    if function in [Function.BALANCE_SHEET, Function.CASH_FLOW, Function.INCOME_STATEMENT]:
        if fiscal and fiscalDateEnding:
            # return report of given fiscal date
            fiscalReports = reports[fiscal]
            found = False
            for index, report in enumerate(fiscalReports):
                if report['fiscalDateEnding'] == fiscalDateEnding:
                    found = True
                    return report, index
            if not found:
                raise Exception('Fiscal Date Ending not found')
        elif fiscal:
            if index:
                return reports[fiscal][index], index
            else:
                return reports[fiscal][0], 0
        else:
            # return latest report
            if (reports[Fiscal.ANNUAL_REPORTS][0]['fiscalDateEnding'])>=(reports[Fiscal.QUARTERLY_REPORTS][0]['fiscalDateEnding']):
                return reports[Fiscal.ANNUAL_REPORTS][0], 0
            else:
                return reports[Fiscal.QUARTERLY_REPORTS][0], 0
    else:
        return reports

def get_latest_series(symbol, function: Function=Function.TIME_SERIES_INTRADAY, interval=1) -> dict:
    """
    Gets the latest time series data for a given symbol and interval.
    Args:
        symbol (str): The stock symbol for which to get the time series data.
        function (Function, optional): An enum value representing the function to be called from the Alpha Vantage API (default Function.TIME_SERIES_INTRADAY).
        interval (int, optional): The time interval (valid values: 1, 5, 15, 30, 60 minutes) for which to get the time series data (default 1).
    Returns:
        The latest time series data for the given symbol and interval.
    Raises:
        Exception: If an error occurs while getting the time series data.
    """
    try:
        lastTimeSeries = alpha_vantage(function, symbol, interval=interval)[f'Time Series ({interval}min)']
    except Exception as e:
        raise e
    return lastTimeSeries[list(lastTimeSeries)[0]]

def get_currency(report) -> str:
    """
    Gets the currency of the given report.
    Args:
        report (dict): A dictionary representing the report for which to get the currency.
    Returns:
        A string representing the currency of the given report.
    """
    try:
        return report['reportedCurrency']
    except:
        return report['Currency']

def revenue_growth(symbol, fiscal: Fiscal=Fiscal.ANNUAL_REPORTS, fiscalDateEnding=None):
    t0_rep, i = get_latest_report(
        symbol,
        inds[Ind.REVENUE_GROWTH].function,
        fiscal,
        fiscalDateEnding
        )
    t0_rev = int(t0_rep[inds[Ind.REVENUE_GROWTH].key])

    tMin1_rev = int(get_latest_report(
        symbol,
        inds[Ind.REVENUE_GROWTH].function,
        fiscal,
        index=i+1
        )[0][inds[Ind.REVENUE_GROWTH].key])

    return f'{round((t0_rev-tMin1_rev)/tMin1_rev, 4):.0%}'  # maybe better to format later

def gross_profit(symbol, fiscal: Fiscal=None, fiscalDateEnding=None):
    # calc
    totRev_rep, _ = get_latest_report(
        symbol,
        inds[Ind.GROSS_PROFIT][0].function,
        fiscal,
        fiscalDateEnding
        )
    totRev = int(totRev_rep[inds[Ind.GROSS_PROFIT][0].key])

    costOfRev_rep, _ = get_latest_report(
        symbol,
        inds[Ind.GROSS_PROFIT][1].function,
        fiscal,
        fiscalDateEnding
        )
    costOfRev = int(costOfRev_rep[inds[Ind.GROSS_PROFIT][1].key])

    gp = totRev-costOfRev, get_currency(totRev_rep) if get_currency(totRev_rep) == get_currency(costOfRev_rep) else None

    # given
    rep, _ = get_latest_report(symbol, Function.INCOME_STATEMENT, fiscal, fiscalDateEnding)
    gp_av = rep['grossProfit'], get_currency(rep)

    return gp, gp_av

def return_on_equity(symbol, fiscal: Fiscal=None, fiscalDateEnding=None):
    # calc
    netInc = int(get_latest_report(
        symbol,
        inds[Ind.RETURN_ON_EQUITY][0].function,
        fiscal,
        fiscalDateEnding
        )[0][inds[Ind.RETURN_ON_EQUITY][0].key])

    totShareEqu = int(get_latest_report(
        symbol,
        inds[Ind.RETURN_ON_EQUITY][1].function,
        fiscal,
        fiscalDateEnding
        )[0][inds[Ind.RETURN_ON_EQUITY][1].key])

    roe = f'{round(netInc/totShareEqu, 4):.2%}' # maybe better to format later

    # given
    rep = get_latest_report(symbol, Function.COMPANY_OVERVIEW)
    roe_av = float(rep['ReturnOnEquityTTM'])

    return roe, roe_av

def equity_ratio(symbol, fiscal: Fiscal=None, fiscalDateEnding=None):
    # calc with liabilities
    totShareEqu = int(get_latest_report(
        symbol,
        inds[Ind.EQUITY_RATIO][0].function,
        fiscal,
        fiscalDateEnding
        )[0][inds[Ind.EQUITY_RATIO][0].key])

    totLiab = int(get_latest_report(
        symbol,
        inds[Ind.EQUITY_RATIO][1].function,
        fiscal,
        fiscalDateEnding
        )[0][inds[Ind.EQUITY_RATIO][1].key])

    equRat = round(totShareEqu/(totLiab+totShareEqu), 4)

    # calc with current & non current assets
    totCurAss = int(get_latest_report(
        symbol,
        inds[Ind.EQUITY_RATIO][2].function,
        fiscal,
        fiscalDateEnding
        )[0][inds[Ind.EQUITY_RATIO][2].key])

    totNonCurAss = int(get_latest_report(
        symbol,
        inds[Ind.EQUITY_RATIO][3].function,
        fiscal,
        fiscalDateEnding
        )[0][inds[Ind.EQUITY_RATIO][3].key])

    equRat_curr = round(totShareEqu/(totCurAss+totNonCurAss), 4)

    # given
    totAss = int(get_latest_report(
        symbol,
        Function.BALANCE_SHEET,
        fiscal,
        fiscalDateEnding
        )[0]['totalAssets'])

    equRat_av = round(totShareEqu/totAss, 4)

    return equRat, equRat_curr, equRat_av

def market_capitalization(symbol):
    # calc
    close_ser = get_latest_series(
        symbol,
        inds[Ind.MARKET_CAPITALIZATION][0].function)
    close = float(close_ser[inds[Ind.MARKET_CAPITALIZATION][0].key])

    num_rep = get_latest_report(
        symbol,
        inds[Ind.MARKET_CAPITALIZATION][1].function)
    num = int(num_rep[inds[Ind.MARKET_CAPITALIZATION][1].key])

    markCap = round(close*num, 4)

    # given
    rep = get_latest_report(
        symbol,
        Function.COMPANY_OVERVIEW)

    markCap_av = rep['MarketCapitalization']

    return markCap, markCap_av  # how to get currency?


# Test functions
assert(revenue_growth('IBM', Fiscal.ANNUAL_REPORTS, '2022-12-31') == revenue_growth('IBM', Fiscal.ANNUAL_REPORTS) == revenue_growth('IBM'))
assert(revenue_growth('IBM', Fiscal.QUARTERLY_REPORTS, '2022-12-31') == revenue_growth('IBM', Fiscal.QUARTERLY_REPORTS))
print(gross_profit('IBM'))
print(return_on_equity('IBM'))
print(equity_ratio('IBM'))
print(market_capitalization('IBM'))

# Test exceptions
#alpha_vantage(Function.BALANCE_SHEET, "IBZ")
#get_report("IBM", Function.BALANCE_SHEET, Fiscal.ANNUAL_REPORTS, fiscalDateEnding= '2022-08-31')
