from src.table import Table
from src.symbol import Symbol
import json

SINGLE_SHARE = False
INDEX = False
COMPARISON = True

if SINGLE_SHARE:
    tickers = ['IBM', 'AAPL']
    table_tickers = Table(tickers)    # creating table object from tickers
    print(table_tickers.json['IBM']['price_to_book']['calculated']) # accessing data
    print(table_tickers.to_dataframe()) # generating pandas dataframe
if INDEX:
    index = 'IXIC'
    table_index = Table(index, Symbol.INDEX)    # creating table object from index
    print(table_index.to_dataframe())   # generating pandas dataframe
    print(json.dumps(table_index.proportion_of_valid_values(), indent=2))   # printing proportion of valid values to JSON and the console
if COMPARISON:
    index = 'IXIC'
    ticker = 'AAPL'
    table_index = Table(index, Symbol.INDEX).compare_to_single_share(ticker)
