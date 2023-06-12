if __name__ == "__main__":

    from src.table import Table
    from src.symbol import Symbol
    import json, os

    SINGLE_SHARE = True
    INDEX = True
    PROPORTION = True
    COMPARISON = True

    if SINGLE_SHARE:
        tickers = ['IBM', 'AAPL']
        table_tickers = Table(tickers)    # creates table object from tickers
        print(table_tickers.json['IBM']['price_to_book']['calculated']) # accesses data
        with open(os.path.join(os.path.dirname(__file__), 'results/metrics.json'), 'w') as file:    # writes key metrics to file
            file.write(json.dumps(table_tickers.json, indent=2))

    if INDEX:
        table_index = Table('NASDAQ', Symbol.INDEX, 'csv')    # creates table object from index and retrieves components from our colleague's data
        print(table_index.to_dataframe())   # generates pandas dataframe

        if PROPORTION:
            with open(os.path.join(os.path.dirname(__file__), 'results/proportion.json'), 'w') as file:    # writes proportion to file
                file.write(json.dumps(table_index.proportion_of_valid_values(), indent=2))

        if COMPARISON:
            table_index.compare_to_single_share('AAPL', os.path.join(os.path.dirname(__file__), 'results/comparison.png')) # visualizes and saves comparison as png
