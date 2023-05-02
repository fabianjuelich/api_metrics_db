from src import indicator
import pandas as pd

def fill_table(symbols):
    indicators_pd = pd.DataFrame(columns=['Ticker']+list(indicator.Indicator))
    for symbol in symbols:
        row = {'Ticker': symbol}
        for i, ind in enumerate(list(indicator.Indicator)):
            if i<8:
                row.update({ind: eval(f'indicator.{ind}(symbol)')})
        indicators_pd = indicators_pd._append(row, ignore_index=True)
    return indicators_pd
