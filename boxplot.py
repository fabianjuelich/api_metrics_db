import requests
import json
from datetime import datetime, timedelta
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# elasticsearch
url = 'http://139.6.56.155:9200/lazy-investor'
header = {"Content-Type": "application/json"}
# user input
ticker = 'AAPL'
request = 'INDEX_NDX_ALPHA_VANTAGE'
metric = 'price_to_earnings'
date = "2023-10-20" # note format
size = 1000
# formatting
metrics = 'metrics'
m = metrics + '.' + metric
d_1 = datetime.strptime(date, "%Y-%m-%d").isoformat()
d_2 = (datetime.strptime(date, "%Y-%m-%d") + timedelta(days=1)).isoformat()

request_ticker = json.dumps(
{
  "_source":[
    "sector",
    m
  ],
  "query":{
    "bool":{
      "must":[
        {
          "range":{
            "timestamp":{
              "gte":d_1,
              "lt":d_2
            }
          }
        },
        {
          "match":{
            "symbol":ticker
          }
        },
        {
          "match":{
            "request":request
          }
        }
      ]
    }
  }
}
)
result_ticker = requests.get(url=url+'/_search', data=request_ticker, headers=header).json()

sector = result_ticker['hits']['hits'][0]['_source']['sector']

request_competitors = json.dumps(
{
  "_source":[
    m
  ],
  "query":{
    "bool":{
      "must":[
        {
          "range":{
            "timestamp":{
              "gte":d_1,
              "lt":d_2
            }
          }
        },
        {
          "match":{
            "sector":sector
          }
        },
        {
          "match":{
            "request":request
          }
        }
      ]
    }
  },
  "size":size
}
)
result_competitors = requests.get(url=url+'/_search', data=request_competitors, headers=header).json()

# data
metric_ticker = result_ticker['hits']['hits'][0]['_source'][metrics][metric]
metric_competitors = [competitor['_source'][metrics][metric] for competitor in result_competitors['hits']['hits'] if competitor['_source'][metrics][metric]]
# transform to DataFrame
df = pd.DataFrame(metric_competitors)

# configure appearence
sns.set(style="darkgrid")
plt.style.use('dark_background')
plt.rcParams.update({"grid.linewidth":0.5, "grid.alpha":0.5})
# plot data
box = sns.boxplot(data=df, palette='pastel')
box.plot(0, metric_ticker, marker='.', markersize=8, color='#2B8C68', label=ticker)
# set legend/title and show
plt.legend(loc='upper right')
box.set(title= f'Comparison between the {sector.lower()} sectors\n{metric.replace("_", "-")} and that of {ticker}')
plt.show()