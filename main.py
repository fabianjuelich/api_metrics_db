from src import table
from src.symbol import Symbol

tickers = ['IBM', 'AAPL']
dax = 'IXIC'

table.table_to_excel(table.fill_table('IBM'))
# table.table_to_excel(table.fill_table(tickers, withContext=True))
# table.table_to_excel(table.fill_table(dax, type=Symbol.INDEX))
