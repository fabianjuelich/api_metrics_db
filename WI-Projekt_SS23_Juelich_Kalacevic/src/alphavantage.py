from assets import credential as cred
from src.enums.fiscal import Fiscal
from src.enums.function import Function
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
    url = 'https://www.alphavantage.co/query'
    params = {
        'function': function.upper(),
        'symbol': symbol,
        'interval': f'{interval}min',
        'apikey': apikey
    }
    r = requests.get(url, params={key: val for key, val in params.items() if val is not None}, timeout=60)
    data = r.json()
    if not data:
        raise Exception('Invalid symbol')
    if list(data.keys())[0] in ['Information', 'Error Message']:
        raise Exception(data)
    return data

# -------------------------------------------------Common queries------------------------------------------------- #

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
    Raises:
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
