
# Libraries und APIs die für Analysen von Aktien verwendet werden können

## Yahoo Finance API & yfinance Library

Die Yahoo Finance bietet eine Vielzahl von Bibliotheken und APIs an, um historische und Echtzeitdaten von Finanzmärkten zu erhalten, wie sie auch auf der offiziellen Seite von Yahoo Finance angezeigt werden. Zu den Angeboten gehören Marktdaten zu Kryptowährungen, regulären Währungen, Aktien und Anleihen, Fundamentaldaten und Optionsdaten sowie Marktanalysen und Nachrichten. Die Daten sind grundsätzlich kostenlos, jedoch hat Yahoo den Dienst für seine API seit einigen Jahren eingestellt.  Derzeit werden die Daten mittels Web & Pandas Table Scriping Methoden von der offiziellen Yahoo Seite extrahiert. Von daher ist die API sehr fragil und fehleranfällig. Bei minimalen Änderungen auf der Seite, können wichtige Funktionalitäten nicht mehr gewährleistet werden. Aus diesem Grund sollte die API nicht im Produktiveinsatz verwendet werden. 

## Wieso verzichte ich auf die Yahoo Finance API?
Wie oben angerissen ist die API sehr fragil und fehleranfällig. Hinzu kommt, dass die Performance bei umfangreichen Anfragen schlecht ist. Threading beschleunigt den Prozess zwar, allerdings verwendet die API Web Scraping, wodurch die eigene IP-Adresse bei jeder Anfrage an Yahoo übermittelt wird. Wenn also durch das Threading mehr Anfragen in kurzer Zeit an Server gesendet werden, besteht die Gefahr, auf die Blacklist von Yahoo gesetzt zu werden. Ab dem Zeitpunkt hat man nur noch einen eingeschränkten Zugriff auf die Daten. Aus diesem Grund verwende ich nur die Ticker-Listen von Yahoo und speichere diese in einer txt-Datei ab. 




   
```python
    import yahoo_fin.stock_info as si

    dow_ticker_list = si.tickers_dow()
    sp500_ticker_list = si.tickers_sp500()
    nasdaq_ticker_list = si.tickers_nasdaq()

    combined_list = dow_ticker_list + sp500_ticker_list + nasdaq_ticker_list
```

```python
    import csv

    with open('ticker.txt', 'w') as file:
    for ticker in combined_list:
        file.write(ticker + '\n')
```


## Alpha Vantage API

Alpha Vantage ist eine API, die Echtzeit- und historische Finanzdaten für Aktien, Devisen, Kryptowährungen und mehr bereitstellt. Zusätzlich gibt es mehr als 50 technische Indikatoren sowie Leistungsdaten für 10 US-Equity-Sektoren. Die Daten lassen sich direkt in Python oder in einer anderen Programmiersprache abrufen, manipulieren oder für spätere Verwendungen z.B. in CSV oder JSON-Dateien speichern. Die API ist grundsätzlich kostenlos, bietet aber auch kostenpflichtige Pläne an. Die kostenlose Variante hat eine begrenzte Anzahl von API-Calls. So können pro Minute 5 Anfragen und täglich bis zu 500 Anfragen gestellt werden. Die Premium-Pläne beginnen bei 29,99$ pro Monat und gehen bis zu 249,99$ pro Monat für 1200 Anfragen pro Minute. Des Weiteren bieten die Premium-Pläne auch rund um die Uhr technischen Support an. Für eine fundierte Analyse der verschiedenen Aktien würde sich hier eine Investion durchaus lohnen. 

<br>

### Welche Vorteile bietet die Verwendung der Alpha Vantage API?



Einer der größten Vorteile ist, dass die API kostenlos ist und die Daten sehr umfangreich sind. Für Aktien und Divisen gibt sogar teilweise Kursdaten die 20 Jahre zurückreichen. Die Daten für Kryptowährungen wie Bitcoin reichen bis ins Jahr 2011 zurück, was die täglichen Preisdaten betrifft. Es kann außerdem entschieden werden, ob die API-Aufrufe direkt durchgeführt werden sollen oder über die bereitgestellte Bibliothek. Die Library ist so eingerichtet, dass jeder der 5 Abschnitte innerhalb der Alpha Vantage API-Dokumentation in einer separaten Datei innerhalb der Bibliothek codiert wurde. Mit den unten aufgeführten Befehlen lassen diese Abschnitte importieren. Der einzige Nachteil ist, dass für jeden API-Call ein API-Key angegeben werden muss. Dieser lässt sich allerdings in einer Umgebungsvariablen speichern und wird von der API auch automatisch gefunden.


| Alpha Vantage | Import statement for library |
| --- | --- |
| Stock Time Series | from alpha_vantage.timeseries import TimeSeries |
| Forex (FX) | from alpha_vantage.foreignexchange import ForeignExchange |
| Cryptocurrencies | from alpha_vantage.cryptocurrencies import CryptoCurrencies |
| Technical Indicators | from alpha_vantage.techindicators import TechIndicators |
| Sector Performances | from alpha_vantage.sectorperformance import SectorPerformances |

## Extraktion der Daten

Grundsätzlich sind Abfragen auf Alpha-Vantage nach dem gleichen Schema aufgebaut. Sie bestehen zum einen aus der Base-URL, der Funktion und dem Ticker. Alpha Vantage gibt bei einer Anfrage ein JSON-Objekt zurück.

```python
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=OVERVIEW&symbol=IBM&apikey=api_key'
r = requests.get(url)
data = r.json()
```

Um an die wichtigsten Kennzahlen eines Unternehmen zu gelangen, reicht die Funktion __Overview__ für diesen Zweck vollkommen aus. Die Ticker erhalten wir aus der Yahoo Finance Libary. Anschließend kann dann über die zuvor angelegte Liste iteriert werden und alle notwendingen Daten  in einer CSV-Datei gespeichert werden.





<br>

Neben den oben aufgeführten APIs und Libaries gibt es noch eine Vielzahl weiterer Finanzbibliotheken und APIs für Python. Allerdings bieten diese i.d.R. nur eine 30 tägige Testversion an und sind anschließend nur gegen einen monatlichen Aufpreis nutzbar. Außerdem haben die meisten eine eingeschränkte Request Anzahl. Hier einige Beispiele: [The Investors Exchange (IEX)](https://iexcloud.io/docs/api/#intraday-news), [marketstack](https://marketstack.com) und [EODHD](https://eodhistoricaldata.com). 







<br>

# Quellen: 

[Yahoo Finance API – A Complete Guide](https://algotrading101.com/learn/yahoo-finance-api-guide/)

[yfinance Library – A Complete Guide](https://algotrading101.com/learn/yfinance-guide/)

[Alpha Vantage Introduction Guide](https://algotrading101.com/learn/alpha-vantage-guide/)

[Offical Alpha Vantage Documentation](https://algotrading101.com/learn/alpha-vantage-guide/)


[IEX API Introduction Guide](https://algotrading101.com/learn/iex-api/)


[Offical IEX Documentation](https://iexcloud.io/docs/api/#intraday-news)




