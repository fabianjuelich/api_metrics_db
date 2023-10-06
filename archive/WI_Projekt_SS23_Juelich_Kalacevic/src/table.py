from archive.WI_Projekt_SS23_Juelich_Kalacevic.src import indicator
from archive.WI_Projekt_SS23_Juelich_Kalacevic.src.enums.symbol import Symbol
from archive.WI_Projekt_SS23_Juelich_Kalacevic.src.components import Components
import pandas as pd
from collections import defaultdict
from archive.WI_Projekt_SS23_Juelich_Kalacevic.src.visualization import visualize_comparison
import os
import csv
import json

class Table:

    def __init__(self, symbols, symbol_type=Symbol.SHARE, source='csv'):
        """Initialize the Table object with symbols and symbol type.
        Args:
            symbols (list or str): A list of symbols or a single symbol.
            symbol_type (Symbol, optional): The type of symbols (default: Symbol.SHARE).
            source (str, optional): 'csv' -> reads stocks_data.csv, 'yahoo' -> scrapes yahoo finance for components
        """
        if type(symbols) != list:
            symbols = [symbols]
        if symbol_type == Symbol.INDEX:
            self.index = symbols
            tmp_symbols = []
            if source == 'yahoo':
                components = Components()
                for symbol in symbols:
                    for component in components.get_symbols(symbol):
                        tmp_symbols.append(component)
            elif source == 'csv':
                with open(os.path.join(os.path.dirname(__file__), '../../Informatikprojekt_WS22_23_Kinetz/data/stocks_data.csv')) as stocks_data_csv:
                    stocks_data = csv.reader(stocks_data_csv)
                    for i, row in enumerate(stocks_data):
                        for symbol in symbols:
                            if row[5] == symbol:
                                tmp_symbols.append(row[0])
                                break
                        #if i == 2: break
            else:
                raise Exception('Invalid source')
            symbols = tmp_symbols.copy()
        self.symbols = symbols
        self.symbol_type = symbol_type
        self.__get_dict()

    def __get_dict(self):
        """Get the dictionary representation of the table."""
        dic = {}

        for symbol in self.symbols:
            symbol_data = {}
            for ind in list(indicator.Indicator):
                indicator_data = {}
                values = eval(f'indicator.{ind}(symbol)')
                for i, type in enumerate(['calculated', 'given']):
                    indicator_data[type] = values[i]
                symbol_data[ind.value] = indicator_data
            dic[symbol] = symbol_data
        self.json = dic
    
    def to_dataframe(self):
        """Convert the table to a DataFrame.
        Returns:
            pd.DataFrame: The table represented as a DataFrame.
        """
        matrix = [[] for symbol in range(2*len(self.symbols))]
        for s, symbol in enumerate(self.json):
            for ind in self.json[symbol]:
                for t, type in enumerate(self.json[symbol][ind]):
                    matrix[2*s+t].append(self.json[symbol][ind][type])
        indicators = [indicator.value for indicator in list(indicator.Indicator)]
        sources = ['calculated', 'given']
        table_index = pd.MultiIndex.from_product([self.symbols, sources])
        table_dataframe = pd.DataFrame(data=matrix, index=table_index, columns=indicators)
        table_dataframe.index.names=['symbol', 'source']
        return table_dataframe

    def proportion_of_valid_values(self):
        """Calculate the proportion of valid values for each indicator in the table.
                Returns:
                    dict: A dictionary containing the proportion of valid values for each indicator.
                        The dictionary has the following structure:
                        {
                            'tickers': [list of tickers],
                            'number of tickers': <total number of tickers>,
                            'proportion_of_valid_values': {
                                <indicator>: {
                                    'calculated': <proportion of valid values for calculated data>,
                                    'given': <proportion of valid values for given data>
                                },
                                ...
                            }
                        }
        """
        tickers = list(self.json.keys())
        number_of_tickers = len(tickers)
        proportion = defaultdict(dict)
        for ind in list(indicator.Indicator):
            count_calculated = 0
            count_given = 0
            for ticker in self.json.values():
                count_calculated += bool(ticker[ind]['calculated'])
                count_given += bool(ticker[ind]['given'])
            proportion[ind]['calculated'] = round(count_calculated/number_of_tickers, 2)
            proportion[ind]['given'] = round(count_given/number_of_tickers, 2)
        statistic = {
            'number of tickers': number_of_tickers,
            'tickers': tickers,
            'proportion_of_valid_values': proportion}
        return statistic

    def compare_to_single_share(self, single_share, path='.'):
        """Compare the average of indicators in the table to a single share of it.
        Args:
            single_share (str): The symbol of the share to compare to.
            path (str): The path of the png to be saved
        Raises:
            Exception: If the table contains more than one index or if the single_share argument is not a string.
        """
        if len(self.index) == 1 and type(single_share) == str:
            averages = []
            values = []
            for ind in list(indicator.Indicator):
                number_of_calculated = len(self.json.keys())
                number_of_given = len(self.json.keys())
                sum_calculated = 0
                sum_given = 0
                value_calculated = None
                value_given = None
                for ticker_key, ticker_value in self.json.items():
                    if ticker_value[ind]['calculated']:
                        sum_calculated += float(ticker_value[ind]['calculated'])
                        if ticker_key == single_share:
                            value_calculated = float(ticker_value[ind]['calculated'])
                    else:
                        number_of_calculated-=1
                    if ticker_value[ind]['given']:
                        sum_given += float(ticker_value[ind]['given'])
                        if ticker_key == single_share:
                            value_given = float(ticker_value[ind]['given'])
                    else:
                        number_of_given-=1
                averages.append((sum_calculated/number_of_calculated if number_of_calculated >= 1 else None, sum_given/number_of_given if number_of_given >= 1 else None))
                values.append((value_calculated, value_given))
            visualize_comparison(list(indicator.Indicator), self.index[0], averages, single_share, values, path)
        else:
            raise Exception('Please call on single index table, with single share as argument')
