# Practical project in WS 23/24: Infrastructure for economic fundamentals

Supervisor: __Prof. Dr. Johann Schaible__\
Elaboration by: __Fabian Jülich and Denis Kalacevic__

### This project follows on from the previous one, where we implemented the idea of ​​publishing the 12 most important metrics for evaluating stocks by handing over a ticker. Now we plan to store this data over a longer period of time in order to be able to analyze changes and associated opportunities.

Building on __[Procurement & Analysis of stock key figures](./archive/WI_Projekt_SS23_Juelich_Kalacevic/)__

## [Documentation](./documentation.md)
1. [__Infrastructure__](./documentation.md#infrastructure) (Jülich)
    - [Docker](./documentation.md#docker)
    - [Elasticsearch](./documentation.md#elasticsearch)
    - [Kibana](./documentation.md#kibana)
    - [App](./documentation.md#app-server)
    - [Cron](./documentation.md#cron-client)
2. [__Usage__](./documentation.md#usage)

3. [__API Comparison__](./documentation.md#api-comparison) (Kalacevic)
    - [Introduction](./documentation.md#introduction)
    - [Methodology](./documentation.md#methodology)
    - [Approach](./documentation.md#approach)
    - [Results](./documentation.md#results)
    - [Discussion](./documentation.md#discussion)
    - [Conclusion](./documentation.md#conclusion)

## Project Overview
- Collecting data on stocks of specific indices over time in a database using a cron job.
- Comparing between different APIs (AlphaVantage, Financial Modeling Prep, Leeway).

The persistent data should be usable for analysis (e.g. comparing a company's P/E ratio with the boxplot of other P/E ratios in the same sector).