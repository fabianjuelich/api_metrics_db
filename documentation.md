# Documentation

## 1. The Problem: What is the actual problem we are facing?

### What is the problem we want to solve with our Work?

The problem we aim to solve with our work is the manual execution of fundamental analysis. When deciding which stocks to invest in, there are numerous key performance indicators that one must know and analyze. Doing this manually and handpicking the indicators requires a lot of effort and concentration. To solve this problem, we aim to implement a solution that allows investors to obtain the most important indicators, in our case the 12 most important indicators selected by us, with just one click and display them in a table, automating the entire manual process.

### Why is this a Problem and why is it important to solve it?

This is a problem because fundamental analysis is very time consuming and labor intensive. Investors would have to collect a large amount of data and analyze it from various sources to make a good and meaningful investment.

In addition, human error can also occur very easily, as it is possible to miss an important metric or make mistakes when analyzing the data manually.

It is important for us to solve this problem because our solution can save investors time and effort by automating the analysis process and providing them with the key indicators they need to make informed decisions. This can help investors make better investment decisions, reduce the risk of errors, and ultimately lead to better investment outcome. It is important for us to solve this problem because our solution can save investors time and effort by automating the analysis process and providing them with the key indicators they need to make informed decisions. This can help investors make better investment decisions, reduce the risk of errors, and ultimately lead to better investment results

## 2. Purpose of the Project: What exactly do we plan to do to solve the problem?

We aim to provide investors with an easier way to perform fundamental analysis by creating a solution that generates a table of the 12 most important stock indicators using a stock ticker such as "IBM". Our solution will utilize the [Alpha Vantage API](https://www.alphavantage.co/) to gather the necessary data for the indicators. Additionally, we will also calculate the indicators ourselves using Alpha Vantage to provide a comparison between the API-generated indicators and our own calculations. This solution will make the process of analyzing stock data more efficient and provide investors with the information they need to make informed investment decisions.

## 3. Approach: How exactly is the goal to be achieved?

To work out the most important stock ratios we will use a [video of the Youtuber Finanzfluss](https://www.youtube.com/watch?v=qie9sxCIhHM) as a reference.

### The 12 Most important Financial Ratios (regarding to Finanzfluss)

Assumption: Compare and understand companies within their respective industries.

Profitability Ratios:

- Revenue growth (e.g. compared to previous year)
- Gross profit (EBITDA margin)
- Return on equity (ROE)

Balance Sheet Ratios:

- Equity ratio
- Gearing ratio (debt-to-equity ratio)

Valuation Ratios:

- Market capitalization
- Enterprise value (EV)
- EV/sales
- EV/EBITDA
- Price-to-earnings ratio (P/E ratio)
- Price-to-book value ratio (P/BV ratio)
- Price-to-cash flow ratio (P/CF ratio)

After that we had to choose where to get the key figures from, but since our colleague [Edgar Kinetz already compared the best APIs for financial data in his project](./Informatikprojekt_WS22-23_Kinetz/), it was immediately clear that we would use the Alpha Vantage API. This API is very comprehensive and potentially free of charge. The key figures of the companies and their shares can be found in the section "Core Stock APIs" and "Fundamental Data" and can be accessed with the provided API requests.

The Data research came to the following results, which we will present in a table for better overview.

| Stock key figure <br/>________________ | What does it mean for the investor <br/>_____________________________________________ | Description <br/>_____________________ | Positive <br/>________ | Data for calculation <br/>___________________________________ | Data given <br/>____________________ |
|---|---|---|---|---|---|
| Revenue Growth | If a company is consistently growing its revenue over time, it can signal to investors that the company is successful and has a strong competitive position in its industry.Moreover, revenue growth can indicate an expanding customer base, increasing market share, or launching new products or services. | Revenue Growth is the increase in revenue over a period of time. | > 0 | [TotalRevenue](https://www.alphavantage.co/documentation/#income-statement) (new) - [TotalRevenue](https://www.alphavantage.co/documentation/#income-statement) (old) / [TotalRevenue](https://www.alphavantage.co/documentation/#income-statement) (old) | [QuarterlyRevenueGrowthYOY](https://www.alphavantage.co/documentation/#company-overview) |
| Gross profit | Gross profit is important to investors because it is a key driver of a company's net income or profitability. With a high gross profit margin, a company generates more revenue from each unit of product or service sold, resulting in a higher net income and higher stock price. If a company has a low gross profit margin, it may indicate that it is not managing its costs efficiently, resulting in lower profitability and a lower stock price. | A company's gross profit is its financial gain after deduction of manufacturing and distribution costs. | > 0 | [totalRevenue](https://www.alphavantage.co/documentation/#income-statement) - [costOfRevenue](https://www.alphavantage.co/documentation/#income-statement) | [grossProfit](https://www.alphavantage.co/documentation/#income-statement) |
| Return on Equity | Investors use ROE to evaluate a company's financial performance over time and to compare it with other companies in the same field. A consistently high ROE may suggest that a company has a competitive advantage or a strong business model that allows it to generate higher profits with less shareholder equity. It could indicate that the company will generate higher returns in the future, which is a positive sign for investors. | Return on equity (ROE) is a financial performance measure calculated by dividing net income by shareholders' equity. | > 1 | [netIncome](https://www.alphavantage.co/documentation/#income-statement) / [totalShareholdersEquity](https://www.alphavantage.co/documentation/#income-statement) | [returnOnEquityTTM](https://www.alphavantage.co/documentation/#company-overview) |
| Equity ratio | Investors should pay attention to the equity ratio because it shows how much of a company's assets are financed by equity as opposed to debt. Being less dependent on borrowing money to finance its operations, a company with a high equity ratio is likely to have lower debt levels and be more financially stable. Investors may find this encouraging because it may mean that the business is less vulnerable to financial risks and may be better able to withstand economic downturns. | The equity ratio is a way to show how much of a company's assets were financed through equity. | > 1 | [totalShareholderEquity](https://www.alphavantage.co/documentation/#balance-sheet) / [totalLiabilities](https://www.alphavantage.co/documentation/#balance-sheet) + [totalShareholderEquity](https://www.alphavantage.co/documentation/#balance-sheet) | [totalShareholderEquity](https://www.alphavantage.co/documentation/#balance-sheet) / [totalAssets](https://www.alphavantage.co/documentation/#balance-sheet) |
| Gearing | Gearing is important to investors because it can affect a company's ability to generate profits and pay dividends. When a company is heavily geared, it may be necessary to use a sizeable portion of its profits to pay the interest on its debt, which reduces the amount of money that can be used to pay dividends or reinvest in the company. In addition, businesses that are heavily leveraged may be more vulnerable to recessions or an increase in interest rates, which can make it challenging to repay debt. | Gearing is the ratio of a company's debt-to-equity (D/E). It shows how much of a company's operations are financed by creditors versus shareholders. In other words, it measures a company's financial leverage. | < 1 | [longTermDebtNoncurrent](https://www.alphavantage.co/documentation/#balance-sheet) / [totalShareholderEquity](https://www.alphavantage.co/documentation/#balance-sheet) | [longTermDebtNoncurrent](https://www.alphavantage.co/documentation/#balance-sheet) / [totalShareholderEquity](https://www.alphavantage.co/documentation/#balance-sheet) |
| Market capitalization | The total value of a company's equity as judged by the market is reflected in market capitalization, which is crucial to investors. In general, bigger companies are viewed as being more established, reliable, and risk-free than smaller companies with smaller market capitalizations. As a result, investors might be more inclined to invest in larger businesses because they might provide a higher level of security and long-term stability. Market capitalization can also be used to group businesses into various market segments, such as small-cap, mid-cap, and large-cap. These classifications, which are based on a company's market capitalization in relation to competing companies, can give investors a general idea of the risk and return potential associated with various investment opportunities. | Market capitalization refers to the total market value of a company that is traded on the stock market. | depends | [4. close](https://www.alphavantage.co/documentation/#intraday) * [SharesOutstanding](https://www.alphavantage.co/documentation/#company-overview) | [MarketCapitalization](https://www.alphavantage.co/documentation/#company-overview) |
| EV | Because it can be used as a benchmark when comparing various companies or when estimating the value of a potential acquisition or merger, EV is a crucial metric for investors. A company that has a lower EV in comparison to its competitors may be undervalued and offer a potential investment opportunity. Enterprise Value can also be used by investors to determine crucial valuation ratios like EV/EBITDA or EV/Sales, which can help to shed more light on a company's financial stability and future growth prospects. A lower EV/EBITDA or EV/Sales ratio, in general, may show that a company is undervalued or has better growth prospects than its competitors. On the other hand, a higher ratio might point to an overvalued company or one with slower growth prospects. | Enterprise Value is the total value of a company. | > | ([4. close](https://www.alphavantage.co/documentation/#intraday) * [SharesOutstanding](https://www.alphavantage.co/documentation/#company-overview)) + [currentLongTermDebt](https://www.alphavantage.co/documentation/#balance-sheet) + [shortLongTermDebtTotal](https://www.alphavantage.co/documentation/#balance-sheet) + [longTermDebtNoncurrent](https://www.alphavantage.co/documentation/#balance-sheet) - [cashAndCashEquivalentsAtCarryingValue](https://www.alphavantage.co/documentation/#balance-sheet) | [totalAsset](https://www.alphavantage.co/documentation/#balance-sheet) |
| EV to Revenue | Investors use the EV to revenue ratio to compare the companys valuation in relation to its competitors in the same sector. A high EV to revenue ratio suggests that the market values the company’s ravenue higher than its competitors. In contrast, a low ratio could mean that the company is overvalued in comparison to its competitors. Investors can get a sense of how much they are paying for each dollar of revenue generated by the company. | Enterprise Value to Revenue indicates if the company is Under or overvalued. | < | (([4. close](https://www.alphavantage.co/documentation/#intraday) * [SharesOutstanding](https://www.alphavantage.co/documentation/#company-overview)) + [currentLongTermDebt](https://www.alphavantage.co/documentation/#balance-sheet) + [shortLongTermDebtTotal](https://www.alphavantage.co/documentation/#balance-sheet) + [longTermDebtNoncurrent](https://www.alphavantage.co/documentation/#balance-sheet) - [cashAndCashEquivalentsAtCarryingValue](https://www.alphavantage.co/documentation/#balance-sheet)) / [totalRevenue](https://www.alphavantage.co/documentation/#income-statement) | [EVToRevenue](https://www.alphavantage.co/documentation/#balance-sheet) |
| EV to EBITDA | The EV to EBITDA is used to assess how much a company is valued in relation to its competitors in the same sector. A high EV to EBITDA ratio suggests that the market values the companys earnings higher than that of its competitors, while a low ratio could suggest that the company is undervalues in relation to its competitors. It gives investors a clearer picture of a company's profitability, as it focuses on the core earnings of the business. | The Enterprise Value to EBITDA ratio compares a company's value (including debt) to its cash earnings minus non-cash expenses. | < | (([4. close](https://www.alphavantage.co/documentation/#intraday) * [SharesOutstanding](https://www.alphavantage.co/documentation/#company-overview)) + [currentLongTermDebt](https://www.alphavantage.co/documentation/#balance-sheet) + [shortLongTermDebtTotal](https://www.alphavantage.co/documentation/#balance-sheet) + [longTermDebtNoncurrent](https://www.alphavantage.co/documentation/#balance-sheet) - [cashAndCashEquivalentsAtCarryingValue](https://www.alphavantage.co/documentation/#balance-sheet)) / ([operatingIncome](https://www.alphavantage.co/documentation/#income-statement) + [depreciationAndAmortization](https://www.alphavantage.co/documentation/#income-statement) + [interestAndDebtExpense](https://www.alphavantage.co/documentation/#income-statement)) | [EvToEBIDTA](https://www.alphavantage.co/documentation/#balance-sheet) |
| Price/Earnings | The Price to Earnings ratio compares a stock’s price to its earnings performance. Investors can use P/E ratios to determine wether a stock is overvalued or undervalued. An investor’s expectations for the comapny’s future growth may be lower if the P/E ratio is low, on the other hand Investors may have high expectations for the company’s potential for future growth if the P/E ratio is high. | The Price to Earnings ratio shows the investor how much he can expect to invest in a company in order to gain $1 of that comapnys earnings. | < | [4. close](https://www.alphavantage.co/documentation/#intraday) / [EPS](https://www.alphavantage.co/documentation/#company-overview) | [PERatio](https://www.alphavantage.co/documentation/#company-overview) |
| Price/Book | The P/B ratio is frequently used by investors to evaluate wether a stock is overvalued or undervalued by comparing the stock prise with the book value of a company. A high P/B ratio may indicate that investors have high expectations for the company’s future growth prospects. On the other hand, a low P/B ratio may suggest that investors have lower epxectiations for the company’s future growth. | The Price to book ratio compares the price of a stock to its book value. | < 1 | [4. close](https://www.alphavantage.co/documentation/#intraday) / ([totalShareholderEquity](https://www.alphavantage.co/documentation/#balance-sheet) / [commonStockSharesOutstanding](https://www.alphavantage.co/documentation/#balance-sheet)) | [PriceToBookRatio](https://www.alphavantage.co/documentation/#company-overview) |
| Price/Cash-Flow | The P/CF ratio is used by investors to determine wether a stock is overvalued or undervalued. It compare’s a companys stock price with its cashflow. It helps investors understand how much they are paying for each dollar of the company’s cash flow. As the cash flow is crucial sign of a company’s financial health and sustainability, this could be a useful indicator of company’s value. | The Price to cashflow ratio measures the value of a stocks price in relation to its operating cash flow. | < | [4. close](https://www.alphavantage.co/documentation/#intraday) / ([operatingCashflow](https://www.alphavantage.co/documentation/#cash-flow) / [commonStockSharesOutstanding](https://www.alphavantage.co/documentation/#balance-sheet)) | [marketCapitalization](https://www.alphavantage.co/documentation/#company-overview) / [operatingCashFlow](https://www.alphavantage.co/documentation/#cash-flow) |

### Problems with the approach

One problem we encountered right at the beginning is that the free version of the API is very limited. 5 API requests per minute and 500 requests per day was clearly too little for us, because in the worst case we already have 5 API requests in one function. However, we were able to get in touch with a member of staff at Alpha Vantage and with the help of Prof. Schaible and Steve we now have access to the Academic Access version of the API with 150 API requests per minute and no daily limit.

While developing an [interface to get the latest reports](src/alphavantage.py) from the API, we came across the fact that not every company publishes the same data at the same regular intervals. That is, IBM reports depreciation quarterly, but Apple doesn't, and others don't report it at all. There are many, even more serious, of these irregularities and missing data.

When implementing the option to analyze stocks belonging to an index, we tried to use the Alpha Vantage API to collect symbols from companies in an index. It has the [Listing & Delisting Status](https://www.alphavantage.co/documentation/#listing-status), which returns a [CSV file](https://www.alphavantage.co/query?function=LISTING_STATUS&apikey=demo) with the attributes 'Exchange' and 'Type', but unfortunately it only returns stocks listed in the US. Researching further, we came across [stock-symbol](https://github.com/yongghongg/stock-symbol), an API specifically designed for this use case. Given the dependency on multiple APIs that require partially registered keys, we decided to manage this ourselves. So we [webscraped Yahoo Finance](src/components.py) for a list of the top 30 stocks in terms of an index. We later found out that not all of them have data given, but we also faced the fact that Alphavantage only accepts symbols listed on NASDAQ, so the german [DAX](https://finance.yahoo.com/quote/%5EGDAXI/components), whose symbols look like BMW.DE, doesn't meet those needs, which makes the need to analyze stocks other than those returned by [NASDAQ](https://finance.yahoo.com/quote/%5EIXIC/components) obsolete.

Thats because in the financial world the companies listed on different stock exchanges have different abbreviations or ticker symbols. A ticker symbol is usually an abbreviation used to identify a listed company. This symbol consists of a letter combination of 1-6 numbers and letters, depending on the type of stock exchange. It's unique for every company on every stock exchange. This discrepancy in ticker symbols can create challenges when collecting and analyzing stock data across different exchanges. For example, a company listed as "XYZ Corporation" on the NASDAQ exchange might have a ticker symbol of "XYZ" on NASDAQ. However, the same company could be listed as "XYZ Corp." on the New York Stock Exchange (NYSE) with a ticker symbol of "XYZC." These different variations of ticker symbols make it difficult to analyze and track data consistently.
As mentionend before, Alpha Vantage adressed this issue and is aiming to provide standardized data and simplify the process of retrieving and analyzing stock information by only using ticker symbols used on NASDAQ, which is one of the major stock exchanges in the US.

Even if you get the desired indicator for the correct ticker, you have to consider that indicators are often put into a context. So there is not e.g. the revenue growth but many, each covering another dimension and each being correct. So they obviously can not be compared just as you want. For that reason, we tried to approach the contexts used by Alpha Vantage the best we could - not only for better comparisson, but, not to be neglected, as well because we think, that those are the most meanignful to the investor. To stay with the example: Instead of comparing the revenue of one report with the one released in the report released before, we used the year over year growth for the latest quarter.

However, it is still important for users to be aware of potential variations and take the necessary steps to ensure data consistency when working with stock data from several stock exchanges.

## 4. Methodology

We choose to develope a [Python](https://www.python.org/) script because the language is widely spread and pretty handy for such tasks, like working with data. [Jupyter notebooks](https://jupyter.org/) might be good for demonstration purposes but not eligible for production.
The goal to reach is a function that takes a single or list of symbols and returns a json containing the [12 most important metrics mentioned before](#the-12-most-important-financial-ratios-regarding-to-finanzfluss), both, calculated and given by the API.

For this case we designed the class Table, https://github.com/WanjaSchaible/important-metrics/blob/248e50634f16b7e6784af77d1e93d32926ce6427/src/table.py#L6 which is the one the user interacts with. Instantiating it, returns an object having the desired json attribute. If the user wishes to analyze the data using pandas, the method to_dataframe https://github.com/WanjaSchaible/important-metrics/blob/248e50634f16b7e6784af77d1e93d32926ce6427/src/table.py#L39 can be called to open the door for a lot of data science related options or converting it into e.g. a csv file easily.
For enabling handling huge numbers of symbols belonging to an index like NASDAQ, we implemented the possibility to create the table object for such one. In the background the components will be scraped from yahoo finance like explained before. The Components class https://github.com/WanjaSchaible/important-metrics/blob/81c39baf92ea573b3580467d6478850336686205/src/components.py#L4 offers the method get_symbols https://github.com/WanjaSchaible/important-metrics/blob/81c39baf92ea573b3580467d6478850336686205/src/components.py#L10 for requesting the html file including the rendered js code which will be parsed and its relationl data temporarily stored in a sqlite database https://github.com/WanjaSchaible/important-metrics/blob/81c39baf92ea573b3580467d6478850336686205/src/components.py#L29 for accessing easily.

The core of the program lives in the [indicator.py](src/indicator.py) file, which is seperated into the required data as well as its source section and its actual retrieving and calculation section of the stock key figures. For consistency and to accelerate the developement, we created enums like Function https://github.com/WanjaSchaible/important-metrics/blob/f7476cc9f23cc52fd65ac426f17ba458cc8b33ed/src/function.py#L3-L8

In short, the following abstract shows how simple it is to interact with the code introduced before: https://github.com/WanjaSchaible/important-metrics/blob/f7476cc9f23cc52fd65ac426f17ba458cc8b33ed/main.py#L4-L9

# What did [Alpha Vantage](https://www.alphavantage.co/) Provide?

As we looked into Alpha Vantage for the stock figures, we noticed that the API doesn't provide every stock figure directly and we had to calculate some of them completely by ourselves. Even if the stock figure was provided, we still calculated it ourselves using the formula that is needed. We always tried to use the smallest and most atomic possible way to calculate the metric.

In the following, we will explain in detail if the key stock figures were given or not and which other key figures we used for our own calculation.

Revenue Growth:

- The [QuarterlyRevenueGrowthYOY](https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol=IBM&apikey=demo) provided by Alpha Vantage represents the percentage change in revenue compared to the same quarter of the previous year. It helps assess the company's growth rate.
- To calculate the revenue growth ourselves, we use the formula: (Current Period Revenue - Prior Period Revenue) / Prior Period Revenue.
- The Current Period Revenue and Prior Period Revenue are obtained from the [Income Statement](https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol=IBM&apikey=demo) provided by Alpha Vantage.

Gross Profit:

- The Gross Profit provided by Alpha Vantage in the [Income Statement](https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol=IBM&apikey=demo) represents the revenue remaining after deducting the cost of goods sold. It indicates the profitability of the core business operations.
- To calculate the gross profit ourselves, we use the formula: Revenue - Cost of Revenue.
- We obtain the Revenue and Cost of Revenue figures from the [Income Statement](https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol=IBM&apikey=demo) provided by Alpha Vantage.

Return on Equity:

- The [ReturnOnEquityTTM](https://www.alphavantage.co/query?function=OVERVIEW&symbol=IBM&apikey=demo) (Trailing Twelve Months) provided by Alpha Vantage in the [Company Overview](https://www.alphavantage.co/query?function=OVERVIEW&symbol=IBM&apikey=demo) represents the profitability of shareholders' investment in the company over the past year.
- To calculate the return on equity ourselves, we use the formula: Net Income / Shareholders' Equity.
- The Net Income is obtained from the [Income Statement](https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol=IBM&apikey=demo), and Shareholders' Equity is obtained from the [Balance Sheet](https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol=IBM&apikey=demo) provided by Alpha Vantage.

Equity Ratio:

- Alpha Vantage partially provides the Equity Ratio. For the given Equity Ratio, we use Shareholders' Equity / Total Assets from the [Balance Sheet](https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol=IBM&apikey=demo).
- To calculate the Equity Ratio ourselves, we use the formula: Shareholders' Equity / (Liabilities + Shareholders' Equity).
- We obtain the Shareholders' Equity, Liabilities, and Total Assets figures from the [Balance Sheet](https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol=IBM&apikey=demo) provided by Alpha Vantage.

Gearing:

- Alpha Vantage does not provide the Gearing (debt to equity ratio).
- To calculate the gearing ourselves, we use the formula: Total Debt / Total Shareholders' Equity.
- We obtain the Total Debt and Total Shareholders' Equity figures from the [Balance Sheet](https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol=IBM&apikey=demo) provided by Alpha Vantage.

Market Capitalization:

- The Market Capitalization provided by Alpha Vantage in the [Company Overview](https://www.alphavantage.co/query?function=OVERVIEW&symbol=IBM&apikey=demo) represents the total value of a company's outstanding shares in the stock market.
- To calculate the market capitalization ourselves, we use the formula: Current Market Price per Share * Total Number of Outstanding Shares.
- We obtain the Current Market Price per Share from the [Time Series Intraday](https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&apikey=demo) and the Total Number of Outstanding Shares from the [Company Overview](https://www.alphavantage.co/query?function=OVERVIEW&symbol=IBM&apikey=demo) provided by Alpha Vantage.

Enterprise Value:

- Alpha Vantage does not provide the Enterprise Value.
- To calculate the enterprise value ourselves, we use the formula: Market Capitalization + Total Debt - Cash and Cash Equivalents.
- We obtain the Market Capitalization, Total Debt, and Cash and Cash Equivalents figures from the [Balance Sheet](https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol=IBM&apikey=demo) provided by Alpha Vantage.

Enterprise Value to Revenue Ratio:

- The EvToRevenue Ratio provided by Alpha Vantage in the [Company Overview](https://www.alphavantage.co/query?function=OVERVIEW&symbol=IBM&apikey=demo) represents the valuation multiple of enterprise value to total revenue.
- To calculate the enterprise value to revenue ratio ourselves, we use the formula: Enterprise Value / Total Revenue.
- We use the calculated Enterprise Value and Total Revenue from the [Income Statement](https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol=IBM&apikey=demo) provided by Alpha Vantage.

Enterprise Value to EBITDA:

- The EvToEBITDA provided by Alpha Vantage in the [Company Overview](https://www.alphavantage.co/query?function=OVERVIEW&symbol=IBM&apikey=demo) represents the valuation multiple of enterprise value to EBITDA (Earnings Before Interest, Taxes, Depreciation, and Amortization).
- To calculate the enterprise value to EBITDA ourselves, we calculate EBITDA using the formula: Income Tax Expense + Interest Expense + Net Income + Depreciation and Amortization.
- We then divide our calculated Enterprise Value by EBITDA to obtain the ratio.

Price to Earnings:

- The P/E ratio provided by Alpha Vantage in the [Company Overview](https://www.alphavantage.co/query?function=OVERVIEW&symbol=IBM&apikey=demo) represents the valuation multiple of price per share to earnings per share.
- To calculate the price to earnings ratio ourselves, we use the formula: Stock Price / Earnings Per Share.
- We obtain the Stock Price from the [Time Series Intraday](https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&apikey=demo) and the Earnings Per Share from the [Company Overview](https://www.alphavantage.co/query?function=OVERVIEW&symbol=IBM&apikey=demo) provided by Alpha Vantage.

Price to Book:

- The P/B ratio provided by Alpha Vantage in the [Company Overview](https://www.alphavantage.co/query?function=OVERVIEW&symbol=IBM&apikey=demo) represents the valuation multiple of price per share to book value per share.
- To calculate the price to book ratio ourselves, we use the formula: Market Price per Share / (Total Shareholders' Equity / Shares Outstanding).
- We obtain the Market Price per Share from the [Time Series Intraday](https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&apikey=demo), the Total Shareholders' Equity, and the Shares Outstanding from the [Balance Sheet](https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol=IBM&apikey=demo) provided by Alpha Vantage.

Price to Cashflow:

- The Price to Cashflow ratio is not provided by Alpha Vantage.
- To calculate it ourselves, we use the formula: Stock Price / (Operating Cash Flow / Shares Outstanding).
- We obtain the Stock Price from the [Time Series Intraday](https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&apikey=demo), the Operating Cash Flow from the [Cash Flow statement](https://www.alphavantage.co/query?function=CASH_FLOW&symbol=IBM&apikey=demo), and the Shares Outstanding from the [Balance Sheet](https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol=IBM&apikey=demo) provided by Alpha Vantage.

## 5. Discussion

### Threats to validity 

When doing a stock key figure analysis with an API there are several threats to validity that should be taken into consideration.
1. Data Coverage: All stock key figures may not be completely covered by APIs. The analysis may be constrained and could result in skewed or incomplete conclusions if some crucial data points are missing or not available via the API. 
2. Data Accuracy: It is essential that the API's data is accurate. Data that is inaccurate or unreliable can result in incorrect analysis and decisions. It's crucial to evaluate the credibility and dependability of the data source.
3. API Limitations: The quantity of requests, data points, or available historical data may be constrained by APIs. The extent and depth of the analysis may be constrained by these restrictions. It's crucial to be aware of any restrictions put forward by the API and take into account how they might affect the analysis.
4. Data Consistency: The validity of data can be threatened by differences in how it is presented and formatted among various API endpoints or sources. It's crucial to guarantee that the data obtained from various API calls can be properly integrated and analyzed and is consistent
5. API Reliability and Downtime: The process of analyzing data may be obstructed by API outages or other disruptions. To reduce the risk of interruptions, it is crucial to take the API provider's dependability and stability into account.
