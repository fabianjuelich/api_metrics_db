from src.table import Table
from src.symbol import Symbol

tickers = ['IBM', 'AAPL']
dax = 'IXIC'

table_tickers = Table(tickers)    # creating table object from tickers
# table_index = Table(dax, Symbol.INDEX)    # creating table object from index
print(table_tickers.json['IBM']['price_to_book']['calculated']) # accessing data
print(table_tickers.to_dataframe()) # generating pandas dataframe
