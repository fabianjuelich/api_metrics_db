from src.function import Function
from src.fiscal import Fiscal
from src.alphavantage import get_latest_report, get_latest_series, get_currency
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

# ---------------------------------------------------Templates--------------------------------------------------- #

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
            Function.BALANCE_SHEET)],

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
            'totalShareholderEquity',
            Function.BALANCE_SHEET)],

    # Market Capitalization = Current Market Price per share * Total Number of Outstanding Shares
    Indicator.MARKET_CAPITALIZATION: [
        Data(
            '4. close',
            Function.TIME_SERIES_INTRADAY),
        Data(
            'SharesOutstanding',
            Function.COMPANY_OVERVIEW)],

    # EV = market capitalization + total debt - cash and cash equivalents
    # Total debt: Current long-term debt, short/long-term debt total, and long-term debt noncurrent
    Indicator.EV: [
        Data(
            'currentLongTermDebt',
            Function.BALANCE_SHEET),
        Data(
            'shortLongTermDebtTotal',
            Function.BALANCE_SHEET),
        Data(
            'longTermDebtNoncurrent',
            Function.BALANCE_SHEET),
        Data(
            'cashAndCashEquivalentsAtCarryingValue',
            Function.BALANCE_SHEET)],

    Indicator.EV_TO_REVENUE: Data(
        'totalRevenue',
        Function.INCOME_STATEMENT),

    # EBITDA = Operating Income + Depreciation and Amortization + Non-Operating Expenses(interestAndDebtExpense)
    Indicator.EV_TO_EBITDA: [
        Data(
            'depreciationAndAmortization',
            Function.INCOME_STATEMENT),
        Data(
            'depreciation',
            Function.INCOME_STATEMENT),
        Data(
            'operatingIncome',
            Function.INCOME_STATEMENT),
        Data(
            'interestAndDebtExpense',
             Function.INCOME_STATEMENT)],    

    #Stock Price / Earnings Per Share
    Indicator.PRICE_TO_EARNING: [
         Data(
            '4. close',
            Function.TIME_SERIES_INTRADAY),
        Data(
            'EPS',
            Function.COMPANY_OVERVIEW)],

    #Market price per share(stock price) / (total shareholder equity / shares outstanding(=book value per share))
    Indicator.PRICE_TO_BOOK: [
         Data(
            '4. close',
            Function.TIME_SERIES_INTRADAY),
        Data(
            'totalShareholderEquity',
            Function.BALANCE_SHEET),
        Data(
            'commonStockSharesOutstanding',
            Function.BALANCE_SHEET)],
        

    # Stock Price / (Operating Cash Flow / Shares Outstanding)
    Indicator.PRICE_TO_CASHFLOW: [
        Data(
            '4. close',
            Function.TIME_SERIES_INTRADAY),
        Data(
            'operatingCashflow',
            Function.CASH_FLOW),
        Data(
            'commonStockSharesOutstanding',
            Function.BALANCE_SHEET,
        )]
}

# -------------------------------------------------Get indicators------------------------------------------------- #

def revenue_growth(symbol, fiscal: Fiscal=Fiscal.ANNUAL_REPORTS, fiscalDateEnding=None):
    t0_rep, i = get_latest_report(
        symbol,
        indicators[Indicator.REVENUE_GROWTH].function,
        fiscal,
        fiscalDateEnding
        )
    t0_rev = int(t0_rep[indicators[Indicator.REVENUE_GROWTH].key])

    tMin1_rev = int(get_latest_report(
        symbol,
        indicators[Indicator.REVENUE_GROWTH].function,
        fiscal,
        index=i+1
        )[0][indicators[Indicator.REVENUE_GROWTH].key])

    return f'{round((t0_rev-tMin1_rev)/tMin1_rev, 4):.0%}'  # maybe better to format later

def gross_profit(symbol, fiscal: Fiscal=None, fiscalDateEnding=None):
    # calc
    totRev_rep, _ = get_latest_report(
        symbol,
        indicators[Indicator.GROSS_PROFIT][0].function,
        fiscal,
        fiscalDateEnding
        )
    totRev = int(totRev_rep[indicators[Indicator.GROSS_PROFIT][0].key])

    costOfRev_rep, _ = get_latest_report(
        symbol,
        indicators[Indicator.GROSS_PROFIT][1].function,
        fiscal,
        fiscalDateEnding
        )
    costOfRev = int(costOfRev_rep[indicators[Indicator.GROSS_PROFIT][1].key])

    gp = totRev-costOfRev, get_currency(totRev_rep) if get_currency(totRev_rep) == get_currency(costOfRev_rep) else None

    # given
    rep, _ = get_latest_report(symbol,
        Function.INCOME_STATEMENT,
        fiscal,
        fiscalDateEnding
        )

    gp_av = rep['grossProfit'], get_currency(rep)

    return gp, gp_av

def return_on_equity(symbol, fiscal: Fiscal=None, fiscalDateEnding=None):
    # calc
    netInc = int(get_latest_report(
        symbol,
        indicators[Indicator.RETURN_ON_EQUITY][0].function,
        fiscal,
        fiscalDateEnding
        )[0][indicators[Indicator.RETURN_ON_EQUITY][0].key])

    totShareEqu = int(get_latest_report(
        symbol,
        indicators[Indicator.RETURN_ON_EQUITY][1].function,
        fiscal,
        fiscalDateEnding
        )[0][indicators[Indicator.RETURN_ON_EQUITY][1].key])

    roe = f'{round(netInc/totShareEqu, 4):.2%}' # maybe better to format later

    # given
    rep = get_latest_report(symbol, Function.COMPANY_OVERVIEW)
    roe_av = float(rep['ReturnOnEquityTTM'])

    return roe, roe_av

def equity_ratio(symbol, fiscal: Fiscal=None, fiscalDateEnding=None):
    # calc with liabilities
    totShareEqu = int(get_latest_report(
        symbol,
        indicators[Indicator.EQUITY_RATIO][0].function,
        fiscal,
        fiscalDateEnding
        )[0][indicators[Indicator.EQUITY_RATIO][0].key])

    totLiab = int(get_latest_report(
        symbol,
        indicators[Indicator.EQUITY_RATIO][1].function,
        fiscal,
        fiscalDateEnding
        )[0][indicators[Indicator.EQUITY_RATIO][1].key])

    equRat = round(totShareEqu/(totLiab+totShareEqu), 4)

    # calc with current & non current assets
    totCurAss = int(get_latest_report(
        symbol,
        indicators[Indicator.EQUITY_RATIO][2].function,
        fiscal,
        fiscalDateEnding
        )[0][indicators[Indicator.EQUITY_RATIO][2].key])

    totNonCurAss = int(get_latest_report(
        symbol,
        indicators[Indicator.EQUITY_RATIO][3].function,
        fiscal,
        fiscalDateEnding
        )[0][indicators[Indicator.EQUITY_RATIO][3].key])

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

def gearing(symbol):
    totDebt = int(get_latest_report(symbol, indicators[Indicator.GEARING][0].function)[0][indicators[Indicator.GEARING][0].key])
    totShareEqau = int(get_latest_report(symbol, indicators[Indicator.GEARING][1].function)[0][indicators[Indicator.GEARING][1].key])

    return round(totDebt/totShareEqau, 4)

def market_capitalization(symbol):
    # calc
    close_ser = get_latest_series(
        symbol,
        indicators[Indicator.MARKET_CAPITALIZATION][0].function)
    close = float(close_ser[indicators[Indicator.MARKET_CAPITALIZATION][0].key])

    num_rep = get_latest_report(
        symbol,
        indicators[Indicator.MARKET_CAPITALIZATION][1].function)
    num = int(num_rep[indicators[Indicator.MARKET_CAPITALIZATION][1].key])

    markCap = round(close*num, 4)

    # given
    rep = get_latest_report(
        symbol,
        Function.COMPANY_OVERVIEW)

    markCap_av = rep['MarketCapitalization']

    return markCap, markCap_av  # how to get currency?

def ev(symbol, fiscal: Fiscal=None, fiscalDateEnding=None):
    # calc
    markCap = market_capitalization(symbol)[0]
   
    currLongDebt = int(get_latest_report(
        symbol,
        indicators[Indicator.EV][0].function,
        fiscal,
        fiscalDateEnding
        )[0][indicators[Indicator.EV][0].key])
   
    shortLongTermDebt = int(get_latest_report(
        symbol,
        indicators[Indicator.EV][1].function,
        fiscal,
        fiscalDateEnding
        )[0][indicators[Indicator.EV][1].key])
    
    longTermDebt = int(get_latest_report(
        symbol,
        indicators[Indicator.EV][2].function,
        fiscal,
        fiscalDateEnding
        )[0][indicators[Indicator.EV][2].key])
    
    cashandCashequ = int(get_latest_report(
        symbol,
        indicators[Indicator.EV][3].function,
        fiscal,
        fiscalDateEnding
        )[0][indicators[Indicator.EV][3].key])

    totDebt = currLongDebt + shortLongTermDebt + longTermDebt

    ev = markCap + totDebt - cashandCashequ

    # given
    ev_av = int(get_latest_report(symbol, Function.BALANCE_SHEET)[0]['totalAssets'])

    return ev, ev_av

def ev_to_revenue(symbol, fiscal: Fiscal=None, fiscalDateEnding=None):
    # calc
    ev1 = ev(symbol)[0]

    totRev = int(get_latest_report(
        symbol,
        indicators[Indicator.EV_TO_REVENUE].function,
        fiscal,
        fiscalDateEnding
        )[0][indicators[Indicator.EV_TO_REVENUE].key])
    
    evToRev = round(ev1 / totRev, 3)

    # given
    evToRev_av = float(get_latest_report(
        symbol,
        Function.COMPANY_OVERVIEW,
        )['EVToRevenue'])

    return evToRev, evToRev_av

def ev_to_ebitda(symbol, fiscal: Fiscal=None, fiscalDateEnding=None):
    # calc
    ev_ = ev(symbol)[0]

    depAndAmo = int(get_latest_report(
    symbol,
    indicators[Indicator.EV_TO_EBITDA][0].function,
    fiscal,
    fiscalDateEnding
    )[0][indicators[Indicator.EV_TO_EBITDA][0].key])

    dep = int(get_latest_report(
    symbol,
    indicators[Indicator.EV_TO_EBITDA][1].function,
    fiscal,
    fiscalDateEnding
    )[0][indicators[Indicator.EV_TO_EBITDA][1].key])

    opInc = int(get_latest_report(
    symbol,
    indicators[Indicator.EV_TO_EBITDA][2].function,
    fiscal,
    fiscalDateEnding
    )[0][indicators[Indicator.EV_TO_EBITDA][2].key])

    intAndDeptExp = int(get_latest_report(
    symbol,
    indicators[Indicator.EV_TO_EBITDA][3].function,
    fiscal,
    fiscalDateEnding
    )[0][indicators[Indicator.EV_TO_EBITDA][3].key])

    ebitda = depAndAmo + dep + opInc + intAndDeptExp
    evToEbitda = ev_ / ebitda

    # given
    evToEbitda_av = float(get_latest_report(
        symbol,
        Function.COMPANY_OVERVIEW
        )['EVToEBITDA'])

    return evToEbitda, evToEbitda_av

def price_to_earning(symbol, fiscal: Fiscal=None, fiscalDateEnding=None):
    close_ser = get_latest_series(
    symbol,
    indicators[Indicator.PRICE_TO_EARNING][0].function)
    close = float(close_ser[indicators[Indicator.PRICE_TO_EARNING][0].key])

    eps = float(get_latest_report(
    symbol,
    indicators[Indicator.PRICE_TO_EARNING][1].function,
    fiscal,
    fiscalDateEnding
    )[indicators[Indicator.PRICE_TO_EARNING][1].key])
   
    priceToEarning = close/eps

    return priceToEarning

def price_to_book(symbol, fiscal: Fiscal=None, fiscalDateEnding=None):
    # calc
    close_ser = get_latest_series(
        symbol,
        indicators[Indicator.PRICE_TO_BOOK][0].function)
    close = float(close_ser[indicators[Indicator.PRICE_TO_BOOK][0].key])

    totShareEqui = int(get_latest_report(
        symbol,
        indicators[Indicator.PRICE_TO_BOOK][1].function,
        fiscal,
        fiscalDateEnding
        )[0][indicators[Indicator.PRICE_TO_BOOK][1].key])

    shareOutSta = int(get_latest_report(
        symbol,
        indicators[Indicator.PRICE_TO_BOOK][2].function,
        fiscal,
        fiscalDateEnding
        )[0][indicators[Indicator.PRICE_TO_BOOK][2].key])
    
    priceToBook = round(close/(totShareEqui/shareOutSta), 2)

    # given
    priceToBook_av = float(get_latest_report(
        symbol,
        Function.COMPANY_OVERVIEW
    )['PriceToBookRatio'])

    return priceToBook, priceToBook_av

def price_to_cashflow(symbol, fiscal: Fiscal=None, fiscalDateEnding=None):
    # calc
    close_ser = get_latest_series(
        symbol,
        indicators[Indicator.PRICE_TO_CASHFLOW][0].function)
    close = float(close_ser[indicators[Indicator.PRICE_TO_CASHFLOW][0].key])

    opCash = int(get_latest_report(
        symbol,
        indicators[Indicator.PRICE_TO_CASHFLOW][1].function,
        fiscal,
        fiscalDateEnding
        )[0][indicators[Indicator.PRICE_TO_CASHFLOW][1].key])
    
    sharesOutst = int(get_latest_report(
        symbol,
        indicators[Indicator.PRICE_TO_CASHFLOW][2].function,
        fiscal,
        fiscalDateEnding
        )[0][indicators[Indicator.PRICE_TO_CASHFLOW][2].key])
    
    priceToCashflow = close/(opCash/sharesOutst)

    return priceToCashflow