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


## Quality of the Support:

To test the response time and quality of support, a test email was composed and sent to the four providers. FMP and Leeway provided a reasonable and satisfactory response. There was no response from Alpha Vantage.

### Email for Support Test:

Subject: API Support Responsiveness

Dear …,

We are currently evaluating various Finance/Stock API providers for a project I am working on. As part of this evaluation, I wanted to test the responsiveness of your support team.

Could you please confirm the receipt of this email by replying to it? This will help me determine the efficiency of your support system and give me confidence in considering your API services for integration.

Thank you for your time and attention. I look forward to your response.

Best regards,

Denis


## Is Backtesting possible?

The time period for backtesting with a financial APIs depends on the specific trading or investment strategy and the data you need for the analysis. There isn't a one-size-fits-all answer to how far back the historical data should go, as it can vary based on factors such as your trading frequency, asset class, and the nature of your strategy.

 In this case the answer is still easy because if you wanted to backtest with the 12 Stock key figures we calculated in the last Project, it would not be possible to calculate for example, the Price to Earning with Alpha Vantage, because they only provide the current EPS in the Company Overview. Also the fundamentaldata only goes back to 2018.

FMP provides 15+ years of Financial Statements, including international filings.

Leeway provides fundamental data back up to 30 years and the historical prices of up to 100 years.


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

