from src.table import Table
from src.symbol import Symbol
import json

SINGLE_SHARE = True
INDEX = False

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
