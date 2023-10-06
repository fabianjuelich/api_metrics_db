import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import csv


api_key = open('alphavantage_key.txt').read()

companies_data = []
base_url = 'https://www.alphavantage.co/query?'
function = 'OVERVIEW'

with open("Finance Project/financial_data/data/ticker.txt", "r") as f:
    tickers = f.read().split("\n") # list with all tickers
    
    while len(tickers) > 0:
        next_five = tickers[:5]
        tickers = tickers[5:]
        for ticker in next_five: # only 5 requests per minute are allowed
            response = requests.get(f'{base_url}function={function}&symbol={ticker}&apikey={api_key}')
            companies_data.append(response.json())
        time.sleep(70)
        

labels = list(companies_data[0].keys())

try:
    with open('Finance Project/financial_data/data/stocks_data.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=labels, extrasaction='ignore')
        writer.writeheader()
        for company in companies_data:
            writer.writerow(company)
except IOError:
    print("I/O error")