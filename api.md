![API vergleichs Kategorien](./appendix/categories.jpg)


## **What do the providers state on their website about what is being offered?**

### Alpha Vantage:

-Realtime & historical stock market data APIs

-Forex, commodity & crypto data feeds

-60+ technical & economic indicators

-Market news API & sentiments

-Global coverage

(https://www.alphavantage.co/)

### Financial Modeling Prep:

-Financial statements and multiple metrics for over 30,000 companies across the world

-Stock prices and profile for more than 40,000 symbols

-News and press realeses in real-time categorized by stock symbol

-Multiple economic data like inflation rates, GDP, economic calendar and more

-Many ready to use packages for multiple languages.

-Social sentiment across different social media like Twitter or Reddit

-Insider trading for U.S. stocks gathered from SEC forms

-Processed 13-F forms, mutual fund holders and insitutional holders

-SEC filings, transcripts, etf holders, earnings calendar and many more.

(https://site.financialmodelingprep.com/developer/docs/pricing/)

### Leeway:

-Provides access to comprehensive financial data from over 50 exchanges worldwide. (Among others, in Germany, there are Xetra and Frankfurt Stock Exchange, the Euronext exchanges in Paris and Amsterdam, and of course, in the USA, including New York Stock Exchange (NYSE) and NASDAQ.)

-fundamental data, including annual and quarterly financial statement data with up to 20 years of history, closing prices with the complete historical record, interval price data, and much more.

-Stocks, ETFs, indices, funds, currencies, and cryptocurrencies. For stocks and ETFs, also master data, and for stocks, fundamental data as well.

-Price data API, Fundamental data API, live delayed prices, interval price data, forex, crypto, and commodities, funds & ETF API, bonds, macroeconomic data, event calendar, event history.

(https://leeway.tech/data-api)


# **Is the fundamental data available to calculate the 12 key indicators yourself?**

| Alpha Vantage | FMP | Leeway |
| --- | --- | --- |
| totalRevenue (Income Statement) | revenue (Income Statement) | totalRevenue (Fundamentals → Income Statement) |
| costOfRevenue (Income Statement) | costOfRevenue (Income Statement) | costOfRevenue (Fundamentals → Income Statement) |
| netIncome (Income Statement) | netIncome (Income Statement) | netIncome (Fundamentals → Income Statement) |
| totalShareholderEquity (Balance Sheet) | totalStockholdersEquity (Balance Sheet) | totalStockholdersEquity (Fundamentals → Balance Sheet) |
| totalLiabilities (Balance Sheet) | totalLiabilities (Balance Sheet) | totalLiab (Fundamentals → Balance Sheet) |
| totalCurrentAssets (Balance Sheet) | totalCurrentAssets (Balance Sheet) | totalCurrentAssets (Fundamentals → Balance Sheet) |
| totalNonCurrentAssets (Balance Sheet) | totalNonCurrentAssets (Balance Sheet) | nonCurrentAssetsTotal (Fundamentals → Balance Sheet) |
| longTermDebtNoncurrent (Balance Sheet) | longtermdebtnoncurrent (Balance Sheet as Reported) | longTermDebt (Fundamentals → Balance Sheet) |
| Close (Time Series Intraday) | Close (1 minute technical indicator) | Close (Intraday) |
| SharesOutstanding (Company Overview) | weightedaveragenumberofdilutedsharesoutstanding(financial statement full as reported (nicht so aktuell wie alpha vantage)) | SharesOutstanding ( Fundamentals → SharesStats) |
| cashAndCashEquivalentsAtCarryingValue (Balance Sheet) | cashandcashequivalentsatcarryingvalue (balance sheet as reported) | cashAndEquivalents (Fundamentals → Balance Sheet) |
| depreciationAndAmortization (Income Statement) | depreciationAndAmortization (Income Statement) | deprecationAndAmortization (Fundamentals → Income Statement |
| incomeTaxExpense (Income Statement) | incomeTaxExpense (Income Statement) | IncomeTaxEspense (Fundamentals → Income Statement) |
| interestExpense (Income Statement) | interestExpense (Income Statement) | InterestExpense (Fundamentals → Income Statement) |
| EPS (Company Overview) | earningspersharebasic (financial statement full as reported) | EarningsShare (Fundamentals → Highlights) |
| commonStockSharesOutstanding (Balance Sheet) | commonstocksharesoutstanding (Balance Sheet as reported) | commonStockSharesOutstanding (Fundamentals → Balance Sheet) |
| operatingCashflow (Cash flow) | operatingCashFlow (Cash flow) | totalCashFromOperatingActivities (Fundamentals → Cash Flow) |