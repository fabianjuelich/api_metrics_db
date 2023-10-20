# Practical project in WS 23/24: Infrastructure for economic fundamentals

Supervisor: __Prof. Dr. Johann Schaible__\
Elaboration by: __Fabian Jülich and Denis Kalacevic__

### This project follows on from the previous one, where we implemented the idea of ​​publishing the 12 most important metrics for evaluating stocks by handing over a ticker. Now we plan to store this data over a longer period of time in order to be able to analyze changes and associated opportunities.

Building on __[Procurement & Analysis of stock key figures](./archive/WI-Projekt_SS23_Juelich_Kalacevic/)__

## [Documentation](./documentation.md)
1. [__Infrastructure__](./documentation.md#) (Fabian Jülich)
- Docker
- Elasticsearch
- Kibana
- App
- Cron
2. [__API Comparison__](./documentation.md#) (Denis Kalacevic)
- xyz
## Project Overview
Infrastructure for collecting the most important key figures that have been "checked" for correctness and persisting them in a database:

- Store data on stocks (including sector) from certain indices in a database (Elasticsearch)
- Collect the data on stocks from certain indices over time using a cron job and pack it into the DB
- Compare data between different APIs (AlphaVantage, Financial Modeling Prep, Leeway)

The persisted data can be used for analysis (Compare P/E ratio of a company with box plot of other P/E ratios in the same sector).