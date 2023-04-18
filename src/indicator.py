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
    Indicator.REVENUE_GROWTH: Data(
        'totalRevenue',
        Function.INCOME_STATEMENT),

    Indicator.GROSS_PROFIT: Data(
        'grossProfit',
        Function.INCOME_STATEMENT),

    Indicator.RETURN_ON_EQUITY: Data(
        'ReturnOnEquityTTM',
        Function.COMPANY_OVERVIEW),

    Indicator.EQUITY_RATIO: [
        Data(
            'totalShareholderEquity',
            Function.BALANCE_SHEET),
        Data(
            'totalAssets',
            Function.BALANCE_SHEET)],

    Indicator.GEARING: [
        Data(
            'longTermDebtNoncurrent',
            Function.BALANCE_SHEET),
        Data(
            'totalShareholdersEquity',
        Function.BALANCE_SHEET)],

    Indicator.MARKET_CAPITALIZATION: Data(
        'marketCapitalization',
        Function.COMPANY_OVERVIEW),

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
