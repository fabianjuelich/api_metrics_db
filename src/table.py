from src import indicator
import pandas as pd
from src import context
from src.symbol import Symbol
from src.components import Components

def add_context(table: pd.DataFrame):
    """Adds context information to a table.
    Args:
        table (pd.DataFrame): The input table.
    Returns:
        pd.DataFrame: The updated table with context information.
    """
    definition = {'Ticker': 'Definition'}
    for ind in list(indicator.Indicator):
        definition.update({ind: context.get_indicator_context(ind, 'definition')})
    meaning = {'Ticker': 'Meaning'}
    for ind in list(indicator.Indicator):
        meaning.update({ind: context.get_indicator_context(ind, 'meaning')})
    table = table._append([definition, meaning], ignore_index=True)
    return table

def add_indicators(table: pd.DataFrame, symbols):
    """Adds indicators to a table.
    Args:
        table (pd.DataFrame): The input table.
        symbols (list): A list of symbols.
    Returns:
        pd.DataFrame: The updated table with indicators.
    """
    for symbol in symbols:
        row = {'Ticker': symbol}
        for i, ind in enumerate(list(indicator.Indicator)):
            row.update({ind: eval(f'indicator.{ind}(symbol)')})
        table = table._append(row, ignore_index=True)
    return table

def fill_table(symbols, withContext=False, type=Symbol.SHARE):
    """Fills a table with indicators for symbols.
    Args:
        symbols (list or str): A list of symbols or a single symbol.
        withContext (bool, optional): Specifies whether to add context information (default: False).
        type (Symbol, optional): The type of symbols (default: Symbol.SHARE).
    Returns:
        pd.DataFrame: The table with the indicators for the symbols.
    """
    if symbols is not list:
        symbols = [symbols]

    if type == Symbol.INDEX:
        components = Components()
        tmp_symbols = []
        for symbol in symbols:
            for component in components.get_symbols(symbol):
                tmp_symbols.append(component)
        symbols = tmp_symbols.copy()

    indicators_pd = pd.DataFrame(columns=['Ticker']+list(indicator.Indicator))
    if withContext:
        indicators_pd = add_context(indicators_pd)
    indicators_pd = add_indicators(indicators_pd, symbols)
    return indicators_pd
    
def table_to_excel(table: pd.DataFrame):
    """Saves a table as an Excel file.
    Args:
        table (pd.DataFrame): The input table.
    """
    with pd.ExcelWriter('important-metrics.xlsx') as writer:  
        table.to_excel(writer, sheet_name='indicators')
