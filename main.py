from src.table import Table
from src.symbol import Symbol

tickers = ['IBM', 'AAPL']
dax = 'IXIC'

table = Table(tickers)    # creating table object for tickers
print(table.json['IBM']['price_to_book']['calculated']) # accessing data
print(table.to_dataframe()) # translating to pandas dataframe
