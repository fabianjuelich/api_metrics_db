# Practical project in WS 23/24: Infrastructure for economic fundamentals

Supervisor: __Prof. Dr. Johann Schaible__\
Elaboration by: __Fabian Jülich and Denis Kalacevic__

### This project follows on from the previous one, where we implemented the idea of ​​publishing the 12 most important metrics for evaluating stocks by handing over a ticker. Now we plan to store this data over a longer period of time in order to be able to analyze changes and associated opportunities.

Building on __[Procurement & Analysis of stock key figures](./archive/WI-Projekt_SS23_Juelich_Kalacevic/)__

## [Documentation](./documentation.md)
1. [__Infrastructure__](./documentation.md#) (Jülich)
    - [Docker](./documentation.md#)
    - [Elasticsearch](./documentation.md#)
    - [Kibana](./documentation.md#)
    - [App](./documentation.md#)
    - [Cron](./documentation.md#)
    - [Analysis](./documentation.md#)
2. [__API Comparison__](./documentation.md#) (Kalacevic)
    - [xyz](./documentation.md#xyz)

## Project Overview
- Collecting data on stocks of specific indices over time in a database using a cron job.
- Comparing between different APIs (AlphaVantage, Financial Modeling Prep, Leeway).

The persistent data should be usable for analysis (e.g. comparing a company's P/E ratio with the boxplot of other P/E ratios in the same sector).