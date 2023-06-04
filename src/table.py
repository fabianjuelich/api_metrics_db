from src import indicator
from src.symbol import Symbol
from src.components import Components
import pandas as pd
from collections import defaultdict

class Table:

    def __init__(self, symbols, symbol_type=Symbol.SHARE):
        """Initialize the Table object with symbols and symbol type.
        Args:
            symbols (list or str): A list of symbols or a single symbol.
            symbol_type (Symbol, optional): The type of symbols (default: Symbol.SHARE).
        """
        if type(symbols) != list:
            symbols = [symbols]
        if symbol_type == Symbol.INDEX:
            components = Components()
            tmp_symbols = []
            for symbol in symbols:
                for component in components.get_symbols(symbol):
                    tmp_symbols.append(component)
            symbols = tmp_symbols.copy()
        self.symbols = symbols

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
        df = self.to_dataframe()
        rows = df.index
        tickers = [row[0] for row in rows]
        number_of_tickers = int(len(rows)/2)
        statistic = {
            'tickers': tickers,
            'number of tickers': number_of_tickers,
            'proportion_of_valid_values': defaultdict(dict)}
        for column in df.columns:
            count_calculated = 0
            count_given = 0
            for row in rows:
                not_null = not pd.isnull(df[column].loc[row])
                match row[1]:
                    case 'calculated':
                        count_calculated += not_null
                    case 'given':
                        count_given += not_null
            statistic['proportion_of_valid_values'][column]['calculated'] = round(count_calculated/number_of_tickers, 2)
            statistic['proportion_of_valid_values'][column]['given'] = round(count_given/number_of_tickers, 2)

        return statistic
