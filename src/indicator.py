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
    # Total debt:  long-term debt noncurrent
    Indicator.EV: [    
        Data(
            'longTermDebtNoncurrent',
            Function.BALANCE_SHEET),
        Data(
            'cashAndCashEquivalentsAtCarryingValue',
            Function.BALANCE_SHEET)],

    Indicator.EV_TO_REVENUE: Data(
        'totalRevenue',
        Function.INCOME_STATEMENT),

    # EBITDA = neue rechnung!!!: incomeTaxExpense+ interestExpense + netincome + depreciationAndAmortization 
    Indicator.EV_TO_EBITDA: [                                                                                                      
        Data(
            'depreciationAndAmortization',
            Function.INCOME_STATEMENT),
        Data(
            'incomeTaxExpense',
            Function.INCOME_STATEMENT),
        Data(
            'netIncome',
            Function.INCOME_STATEMENT),
        Data(
            'interestExpense',
             Function.INCOME_STATEMENT)],    

    # Stock Price / Earnings Per Share
    Indicator.PRICE_TO_EARNING: [
         Data(
            '4. close',
            Function.TIME_SERIES_INTRADAY),
        Data(
            'EPS',
            Function.COMPANY_OVERVIEW)],

    # Market price per share(stock price) / (total shareholder equity / shares outstanding(=book value per share))
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

def revenue_growth(symbol, fiscal: Fiscal=Fiscal.QUARTERLY_REPORTS, fiscalDateEnding=None):
    # calc
    try:
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
            index=i+4
            )[0][indicators[Indicator.REVENUE_GROWTH].key])
        
        revenueGrowth = round((t0_rev-tMin1_rev)/tMin1_rev, 3)
    except:
        revenueGrowth = None

    # given
    try:
        revenueGrowth_av = get_latest_report(
            symbol,
            Function.COMPANY_OVERVIEW
        )['QuarterlyRevenueGrowthYOY']
    except:
        revenueGrowth_av = None

    return revenueGrowth, revenueGrowth_av

def gross_profit(symbol, fiscal: Fiscal=None, fiscalDateEnding=None):
    # calc
    try:
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

        gp = totRev-costOfRev
    except:
        gp = None

    # given
    try:
        rep, _ = get_latest_report(symbol,
            Function.INCOME_STATEMENT,
            fiscal,
            fiscalDateEnding
            )

        gp_av = rep['grossProfit']
    except:
        gp_av = None

    return gp, gp_av

def return_on_equity(symbol, fiscal: Fiscal=Fiscal.QUARTERLY_REPORTS, fiscalDateEnding=None):
    # calc TTM
    try:
        netInc = 0
        totShareEqu = 0
        for quarter in range(4):
            netInc += int(get_latest_report(
                symbol,
                indicators[Indicator.RETURN_ON_EQUITY][0].function,
                fiscal,
                fiscalDateEnding,
                index=quarter
                )[0][indicators[Indicator.RETURN_ON_EQUITY][0].key])

            totShareEqu += int(get_latest_report(
                symbol,
                indicators[Indicator.RETURN_ON_EQUITY][1].function,
                fiscal,
                fiscalDateEnding,
                index=quarter
                )[0][indicators[Indicator.RETURN_ON_EQUITY][1].key])

        roe = round(netInc/totShareEqu, 3)
    except:
        roe = None

    # given TTM
    try:
        rep = get_latest_report(symbol, Function.COMPANY_OVERVIEW)
        roe_av = float(rep['ReturnOnEquityTTM'])
    except:
        roe_av = None

    return roe, roe_av

def equity_ratio(symbol, fiscal: Fiscal=None, fiscalDateEnding=None):
    # calc with liabilities
    try:
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
    except:
        equRat = None

    # calc with current & non current assets
    try:
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
    except:
        equRat_curr = None

    # given
    try:
        totAss = int(get_latest_report(
            symbol,
            Function.BALANCE_SHEET,
            fiscal,
            fiscalDateEnding
            )[0]['totalAssets'])

        equRat_av = round(totShareEqu/totAss, 4)
    except:
        equRat_av = None

    return equRat, equRat_av

def gearing(symbol):
    try:
        totDebt = int(get_latest_report(symbol, indicators[Indicator.GEARING][0].function)[0][indicators[Indicator.GEARING][0].key])
        totShareEqau = int(get_latest_report(symbol, indicators[Indicator.GEARING][1].function)[0][indicators[Indicator.GEARING][1].key])
        gearing = round(totDebt/totShareEqau, 4)
    except:
        gearing = None

    return gearing, None

def market_capitalization(symbol):
    # calc
    try:
        close_ser = get_latest_series(
            symbol,
            indicators[Indicator.MARKET_CAPITALIZATION][0].function)
        close = float(close_ser[indicators[Indicator.MARKET_CAPITALIZATION][0].key])

        num_rep = get_latest_report(
            symbol,
            indicators[Indicator.MARKET_CAPITALIZATION][1].function)
        num = int(num_rep[indicators[Indicator.MARKET_CAPITALIZATION][1].key])

        markCap = round(close*num)
    except:
        markCap = None

    # given
    try:
        rep = get_latest_report(
            symbol,
            Function.COMPANY_OVERVIEW)

        markCap_av = rep['MarketCapitalization']
    except:
        markCap_av = None

    return markCap, markCap_av

def ev(symbol, fiscal: Fiscal=None, fiscalDateEnding=None):
    # calc
    try:
        markCap = market_capitalization(symbol)[0]
       
        longTermDebt = int(get_latest_report(
            symbol,
            indicators[Indicator.EV][0].function,
            fiscal,
            fiscalDateEnding
            )[0][indicators[Indicator.EV][0].key])
        
        cashandCashequ = int(get_latest_report(
            symbol,
            indicators[Indicator.EV][1].function,
            fiscal,
            fiscalDateEnding
            )[0][indicators[Indicator.EV][1].key])

        totDebt = longTermDebt

        ev = markCap + totDebt - cashandCashequ
    except:
        ev = None

    return ev, None

def ev_to_revenue(symbol, fiscal: Fiscal=Fiscal.ANNUAL_REPORTS, fiscalDateEnding=None):
    # calc
    try:
        ev1 = ev(symbol)[0]

        totRev = int(get_latest_report(
            symbol,
            indicators[Indicator.EV_TO_REVENUE].function,
            fiscal,
            fiscalDateEnding
            )[0][indicators[Indicator.EV_TO_REVENUE].key])
        
        evToRev = round(ev1 / totRev, 3)
    except:
        evToRev = None

    # given
    try:
        evToRev_av = float(get_latest_report(
            symbol,
            Function.COMPANY_OVERVIEW,
            )['EVToRevenue'])
    except:
        evToRev_av = None

    return evToRev, evToRev_av

def ev_to_ebitda(symbol, fiscal: Fiscal=Fiscal.ANNUAL_REPORTS, fiscalDateEnding=None):
    # calc
    ev_ = ev(symbol)[0]

    try:
        depAndAmo = int(get_latest_report(
            symbol,
            indicators[Indicator.EV_TO_EBITDA][0].function,
            fiscal,
            fiscalDateEnding
        )[0][indicators[Indicator.EV_TO_EBITDA][0].key])

        incTaxExp = int(get_latest_report(
            symbol,
            indicators[Indicator.EV_TO_EBITDA][1].function,
            fiscal,
            fiscalDateEnding
        )[0][indicators[Indicator.EV_TO_EBITDA][1].key])

        netInc = int(get_latest_report(
            symbol,
            indicators[Indicator.EV_TO_EBITDA][2].function,
            fiscal,
            fiscalDateEnding
        )[0][indicators[Indicator.EV_TO_EBITDA][2].key])

        intExp = int(get_latest_report(
            symbol,
            indicators[Indicator.EV_TO_EBITDA][3].function,
            fiscal,
            fiscalDateEnding
        )[0][indicators[Indicator.EV_TO_EBITDA][3].key])

        ebitda = depAndAmo + incTaxExp + netInc + intExp
        evToEbitda = ev_ / ebitda
    except:
        evToEbitda = None

    # given
    try:
        evToEbitda_av = float(get_latest_report(
            symbol,
            Function.COMPANY_OVERVIEW
        )['EVToEBITDA'])
    except:
        evToEbitda_av = None

    return evToEbitda, evToEbitda_av

def price_to_earning(symbol, fiscal: Fiscal=None, fiscalDateEnding=None):
    # calc
    try:
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
    except:
        priceToEarning = None

    # given
    try:
        priceToEarning_av = float(get_latest_report(
            symbol,
            Function.COMPANY_OVERVIEW
        )['PERatio'])
    except:
        priceToEarning_av = None

    return priceToEarning, priceToEarning_av

def price_to_book(symbol, fiscal: Fiscal=None, fiscalDateEnding=None):
    # calc
    try:
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
    except:
        priceToBook = None

    # given
    try:
        priceToBook_av = float(get_latest_report(
            symbol,
            Function.COMPANY_OVERVIEW
        )['PriceToBookRatio'])
    except:
        priceToBook_av = None

    return priceToBook, priceToBook_av

def price_to_cashflow(symbol, fiscal: Fiscal=None, fiscalDateEnding=None):
    # calc
    try:
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
    except:
        priceToCashflow = None

    return priceToCashflow, None