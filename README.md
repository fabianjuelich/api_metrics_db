# WI project in SS 23: Procurement & Analysis of stock key figures

Supervisor: __Prof. Dr. Johann Schaible__\
Elaboration by: __Fabian Jülich and Denis Kalacevic__

### For this elaboration, we have realized the idea of issuing the 12 most important key figures for the valuation of stocks by handing over a ticker. To achieve this goal, we used the Alpha Vantage API to retrieve the required data. This enables us to carry out automated fundamental analysis for stocks.
Building on __[Informatikprojekt im WiSe 22/23: Dateninfrastruktur für die künftige Auswertung & Analyse von Finanzdaten](Informatikprojekt_WS22-23_Kinetz)__

## Documentation
1. [The Problem](./documentation.md#1-the-problem-what-is-the-actual-problem-we-are-facing)
2. [Purpose of the Project](./documentation.md#2-purpose-of-the-project-what-exactly-do-we-plan-to-do-to-solve-the-problem)
3. [Approach](./documentation.md#3-approach-how-exactly-is-the-goal-to-be-achieved)
4. [Methodology](./documentation.md#4-methodology)
4. [Discussion](./documentation.md#5-discussion)

## Project Overview
1. [Documentation](./documentation.md)
2. [Establish connection to Alpha Vantage API](./src/alphavantage.py)
3. [Retrieve necessary data and calculate stock key figures](./src/indicator.py)
5. [Make key figures accessible and apply basic analysis](./src/table.py)
6. [Define and create visualization for comparison](./src/visualization.py)
