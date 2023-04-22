from src.function import Function
from dataclasses import dataclass
from enum import StrEnum, auto

class Indicator(StrEnum):
    REVENUE_GROWTH = auto()
    GROSS_PROFIT = auto()
    RETURN_ON_EQUITY = auto()
    EQUITY_RATIO = auto()
    GEARING = auto()
    MARKET_CAPITALIZATION = auto()
    EV = auto()
    EV_TO_REVENUE = auto()
    EV_TO_EBITDA = auto()
    PRICE_TO_EARNING = auto()
    PRICE_TO_BOOK = auto()
    PRICE_TO_CASHFLOW = auto()

@dataclass
class Data:
    def __init__(self, key: str, function: Function):
        self.key = key
        self.function = function
    def __str__(self):
        return (self.key + ': ' + self.function)

indicators = {
    # Revenue growth = (Current Period Revenue - Prior Period revenue) / Prior period revenue
    Indicator.REVENUE_GROWTH: Data(
        'totalRevenue',
        Function.INCOME_STATEMENT),

    # Gross Profit = Revenue – Cost of Revenue
    Indicator.GROSS_PROFIT: [
        Data(
            'totalRevenue',
            Function.INCOME_STATEMENT),
        Data(
            'costOfRevenue',
            Function.INCOME_STATEMENT)],

    # ROE = Net Income / Shareholders' Equity
    Indicator.RETURN_ON_EQUITY: [
        Data(
            'netIncome',
            Function.INCOME_STATEMENT),
        Data(
            'totalShareholderEquity',
            Function.BALANCE_SHEET )],

    # Equity Ratio = Shareholder's Equity / (Liabilities + Shareholders' Equity)
    #              = Shareholder's Equity / (Current Assets + Non Current Assets)
    Indicator.EQUITY_RATIO: [
        Data(
            'totalShareholderEquity',
            Function.BALANCE_SHEET),
        Data(
            'totalLiabilities',
            Function.BALANCE_SHEET),
        Data(
            'totalCurrentAssets',
            Function.BALANCE_SHEET),
        Data(
            'totalNonCurrentAssets',
            Function.BALANCE_SHEET)],

    # Gearing = Total Debt / Total Shareholders' Equity
    Indicator.GEARING: [
        Data(
            'longTermDebtNoncurrent',
            Function.BALANCE_SHEET),
        Data(
            'totalShareholdersEquity',
            Function.BALANCE_SHEET)],

    # Market Capitalization = Current Market Price per share * Total Number of Outstanding Shares
    Indicator.MARKET_CAPITALIZATION: [
        Data(
            '4. close',
            Function.TIME_SERIES_INTRADAY),
        Data(
            'SharesOutstanding',
            Function.COMPANY_OVERVIEW)],

    Indicator.EV: Data(
        'totalAssets',
        Function.BALANCE_SHEET),

    Indicator.EV_TO_REVENUE: Data(
        'EvToRevenue',
        Function.BALANCE_SHEET),

    Indicator.EV_TO_EBITDA: Data(
        'EvToEbitda',
        Function.BALANCE_SHEET),

    Indicator.PRICE_TO_EARNING: Data(
        'PERatio',
        Function.COMPANY_OVERVIEW),

    Indicator.PRICE_TO_BOOK: Data(
        'PriceToBookRatio',
        Function.COMPANY_OVERVIEW),

    Indicator.PRICE_TO_CASHFLOW: [
        Data(
            'marketCapitalization',
            Function.COMPANY_OVERVIEW),
        Data(
            'operatingCashFlow',
            Function.CASH_FLOW)]
}