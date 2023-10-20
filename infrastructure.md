__Note:__ Some links can only be accessed in the universities' network (e.g. by connecting via the VPN).

# Infrastructure

![infrastructure](./appendix/infrastructure/infrastructure.png)

## [Docker](https://www.docker.com/)
Docker is used to build and run Linux containers for multiple platforms, while Docker Compose is a tool for defining and managing multi-container applications. Together, they provide a powerful solution for containerization, making it easier to deploy and scale applications.

Our composed Docker application consists of 4 services:
- __Elasticsearch__ (Database)
- __Kibana__ (Frontend)
- __App__ (Logic)
- __Cron__ (Automation)

### Architecture
![docker](./appendix/infrastructure/docker.png)

### [Dockerfile](https://docs.docker.com/engine/reference/builder/)
Contains instructions for building an image.

__FROM__ creates the (Debian) base image.\
__RUN__ executes commands on the OS. (E.g. setting the timezone)\
__ADD__ copies files and directories into the image. (E.g. code)\
__CMD__ defines what to do on start. (E.g. running a loop)

### [Compose file](https://docs.docker.com/compose/compose-file/03-compose-file/)
YAML file that defines the services used in the multi-container application. Therefore, you can use images directly or build from an existing Dockerfile.

The working directory (WORKDIR) is used as the python path (searched for imports instead of the parent directory) unless it is explicitly defined as an environment variable by `ENV PYTHONPATH=<path>`. \
The Elasticsearch data which is located at */usr/share/elasticsearch/data* on the guest machine will be persistently stored at */var/lib/docker/volumes/compose_elasticsearch_volume/_data* on the host machine.

### Networking
Docker Compose maintains a DNS that resolves the `container_name` property used in the [Docker Compose configuration](./compose/docker-compose.yml) to the relevant IP address.
When customizing ports, take a look at [this table](https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers) to avoid jam.

### Docker commands you should know:
Execute in the same directory as the [compose file](./docker/docker-compose.yml) as __root__.

- `docker compose build [--no-cache]` builds all containers [from new]
- `docker compose up [-d]` runs all containers [in background]
- `docker ps` lists running containers
- `docker exec -it <container name> bash` opens shell on the container

## [Elasticsearch](https://www.elastic.co/elasticsearch/)
Elasticsearch is a document-based database search engine that surpasses traditional (relational) databases for processing metrics due to its exceptional speed, scalability, and versatile search capabilities.
The stored documents, which are JSON objects are grouped into so called indeces. Those are comparable to tables. Mapping defines how fields may be used.
It provides a [REST API](https://de.wikipedia.org/wiki/Representational_State_Transfer) that you can send requests to through its HTTP interface.
That way you have different options to communicate with the database: 
1. Transferring data with [cURL](https://curl.se/)
2. Using the [Kibana console](http://139.6.56.155:5601/app/dev_tools#/console)
3. Using a programming languages library like the [python client](https://elasticsearch-py.readthedocs.io/en/v8.9.0/)
4. Saving and sending requests with [postman](https://www.postman.com/)

### Database design
While Elasticsearch can handle unstructured data, our use case is a scenario where a carefully chosen schema and mapping is beneficial to ensure data integretiy, search efficiency and ease of use.
```yaml
{
  # name of the index
  "lazy-investor": {
    # used to provide alternative names or references to the index
    "aliases": {},
    # defines the fields for the index by describing their data type and subfields
    "mappings": {
      "properties": {
        "indices": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        },
        "industry": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        },
        "metrics": {
          "properties": {
            "equity_ratio": {
              "type": "float"
            },
            "ev_to_ebitda": {
              "type": "float"
            },
            "ev_to_sales": {
              "type": "float"
            },
            "gross_profit": {
              "type": "long"
            },
            "market_capitalization": {
              "type": "long"
            },
            "price_to_book_value": {
              "type": "float"
            },
            "price_to_earnings": {
              "type": "float"
            },
            "return_on_equity": {
              "type": "float"
            },
            "revenue_growth": {
              "type": "float"
            }
          }
        },
        "request": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        },
        "sector": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        },
        "symbol": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        },
        "timestamp": {
          "type": "date"
        }
      }
    },
    # contains various configurations for the index
    "settings": {
      "index": {
        "routing": {
          "allocation": {
            "include": {
              "_tier_preference": "data_content"
            }
          }
        },
        "number_of_shards": "1",
        "provided_name": "lazy-investor",
        "creation_date": "1697468673744",
        "number_of_replicas": "1",
        "uuid": "nq4OdF_wRF60M7VP2PDAKw",
        "version": {
          "created": "8090199"
        }
      }
    }
  }
}
```
### Example document
```json
{
  "_index": "lazy-investor",
  "_id": "mtIWT4sBXRCDxZ8MO0Ai",
  "_version": 1,
  "_seq_no": 486,
  "_primary_term": 1,
  "found": true,
  "_source": {
    "symbol": "AAPL",
    "sector": "Technology",
    "industry": "Consumer Electronics",
    "ipo": "1980-12-12",
    "indices": [
      "DJI",
      "S5INFT",
      "IXCO",
      "OEX",
      "NDX",
      "SPX",
      "IXIC",
      "DJA"
    ],
    "metrics": {
      "revenue_growth": -0.014,
      "gross_profit": 170782000000,
      "return_on_equity": 1.6009,
      "equity_ratio": 0.1799019812677965,
      "gearing_ratio": 1.627086305869861,
      "market_capitalization": 2743176790016,
      "enterprise_value": 2789980241920,
      "ev_to_sales": 5.9171,
      "ev_to_ebitda": 23.52,
      "price_to_earnings": 29.3903,
      "price_to_book_value": 44.6301,
      "price_to_cashflow": 103.98698976557999
    },
    "timestamp": "2023-10-20T23:55:38.909939",
    "request": "STOCK_AAPL_US_LEEWAY"
  }
}
```

### Relevant HTTP request methods
__PUT__ replaces a ressource with the payload. \
__GET__ requests a representation of a ressource. \
__DELETE__ deletes a ressource. \
__POST__ submits an change of the ressource.

### Common requests
```yaml
# create index
PUT lazy-investor

# map timestamp to date
PUT /lazy-investor/_mapping
{
  "properties": {
    "timestamp": {
      "type": "date"
    }
  }
}

# show clusters
GET _cluster/health

# show nodes
GET _nodes/stats

# show db schema (as seen above)
GET lazy-investor

# delete index lazy-investor
DELETE /lazy-investor

# show all documents
GET /lazy-investor/_search

# show specific document by id (as seen above)
GET lazy-investor/_doc/mtIWT4sBXRCDxZ8MO0Ai

# search for symbol IBM
GET /lazy-investor/_search
{
  "query": {
    "match": {
      "symbol": "IBM"
    }
  }
}

# search for stocks listed in SPX
GET /lazy-investor/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "indices": "SPX"
          }
        }
      ]
    }
  }
}

# search for minimum price to earnings of 100
GET /lazy-investor/_search
{
  "query": {
    "range" : {
      "metrics.price_to_earnings": {
          "gte" : 100
      }
    }
  }
}

# search for documents created on 2023-10-14
GET /lazy-investor/_search
{
  "query": {
    "range": {
      "timestamp": {
        "gte": "2023-10-14",
        "lt": "2023-10-15"
      }
    }
  }
}

# remove all documents created before 2023-11-01
POST /lazy-investor/_delete_by_query
{
  "query": {
    "range": {
      "timestamp": {
        "lt": "2023-11-01"
      }
    }
  }
}
```

### Security

To make the database more secure, you can set the security environment variable to true and assign a username and password.

```dockerfile
xpack.security.enabled: "true"
ELASTIC_USERNAME: "fabian"
ELASTIC_PASSWORD: "Pa$$w0rd"
```

## [Kibana](https://www.elastic.co/de/kibana)
Browser-based data visualization and analysis tool that is built on Elasticsearch and part of the [Elastic Stack](https://www.elastic.co/en/elastic-stack). The resulting visualizations can be saved and assigned to dashboards for monitoring and benchmarking purposes.

### Example: Proportionally market capitalization grouped by the top 5 sectors for the NASDAQ-100, collected on October 17th using Alpha Vantage

![visualization](./appendix/results/visualization.png)

## App (Server)
Application logic procuring and transforming fundamental data.

__Excursus: [Tickersymbols](https://www.ig.com/en/glossary-trading-terms/stock-symbol-definition)__ \
Those abbreviations (usually 1-6 characters) identify stocks and indeces (mostly within one country). Thus, there may be different symbols for the same company or a company may be known under several symbols.

### [app.py](./docker/app/app.py)
Main program, whose `document()` function is called to receive index, market or stock data including metrics and general information.
Uses ss.py to retrieve basic data such as symbols needed for findata.py to receive financial data for an index or a market.

### [findata.py](./docker/app/findata.py)
Parses [multiple financial APIs](./api.md) to retrieve fundamental data and general information. Encapsulating (and caching) the data into objects provides a call-cost efficient way to calculate metrics.

### [ss.py](./compose/App/ss.py)
Uses a pretty neat API called [StockSymbol](https://github.com/yongghongg/stock-symbol/tree/master) to implement the generation of a JSON file that lists all stock symbols belonging to a given [index](./appendix/index_symbols.json) or [market](./appendix/market_symbols.json). This project saved us a lot of [scraping like we did last time](./archive/WI_Projekt_SS23_Juelich_Kalacevic/src/components.py). However, it should be mentioned that, as is usual with APIs, server failures can occur. That's why we use the files generated once as a backup. \
Attention: [Used *dr_market* instead of *de_market* in **market_list** attribute in case of german stocks](https://github.com/yongghongg/stock-symbol/issues/9).

### [interface.py](./compose/App/interface.py)
XML-RPC server for responding to HTTP requests from Clients.
Enums cannot be used due to lack of encoding from XML. Therefore, their actual values must be used.

### tokens.py (not staged)
API-keys used for Alpha-Vantage, Financial Modeling Prep, Leeway and StockSymbol.

## [Cron](https://wiki.ubuntuusers.de/Cron/) (Client)
Service that enables scheduling the execution of bash commands. \
__Note:__ When working with cronjobs, it's important to explicitly set the timezone on that (virtual) machine.

### [crontab](./docker/cron/crontab)
Table that lists cronjobs specifying the minute, hour, day, month and weekday a command should be executed. They are either system wide or user related.

### [cronjob.py](./docker/cron/cronjob.py)
Implements a XML-RPC client that requests findata from the applications interface and stores it in the database via HTTP request.

##
__Shared__\
Api and Sort Enum.

# Usage
`interface.py`
```python
def metrics(sort: int, symbols: str, country_codes: str, api: int)
```
```
sort        symbols country_codes api
SORT.INDEX     1..*             0   1
SORT.MARKET       0          1..*   1
SORT.STOCK     1..*             1   1
```