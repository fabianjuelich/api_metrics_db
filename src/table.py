from src import indicator
import pandas as pd
from src import context

def add_context(table: pd.DataFrame):
    definition = {'Ticker': 'Definition'}
    for ind in list(indicator.Indicator):
        definition.update({ind: context.get_indicator_context(ind, 'definition')})
    meaning = {'Ticker': 'Meaning'}
    for ind in list(indicator.Indicator):
        meaning.update({ind: context.get_indicator_context(ind, 'meaning')})
    table = table._append([definition, meaning], ignore_index=True)
    return table

def add_indicators(table: pd.DataFrame, symbols):
    for symbol in symbols:
        row = {'Ticker': symbol}
        for i, ind in enumerate(list(indicator.Indicator)):
            if i<12:
                row.update({ind: eval(f'indicator.{ind}(symbol)')})
        table = table._append(row, ignore_index=True)
    return table

def fill_table(symbols):
    indicators_pd = pd.DataFrame(columns=['Ticker']+list(indicator.Indicator))
    if symbols is not list:
        symbols = [symbols]
    indicators_pd = add_context(indicators_pd)
    indicators_pd = add_indicators(indicators_pd, symbols)
    return indicators_pd
