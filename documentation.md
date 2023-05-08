# Documentation

# 1. The Problem: What is the actual problem we are facing?

## What is the problem we want to solve with our Work?

The problem we aim to solve with our work is the manual execution of fundamental analysis. When deciding which stocks to invest in, there are numerous key performance indicators that one must know and analyze. Doing this manually and handpicking the indicators requires a lot of effort and concentration. To solve this problem, we aim to implement a solution that allows investors to obtain the most important indicators, in our case the 12 most important indicators selected by us, with just one click and display them in a table, automating the entire manual process.

## Why is this a Problem and why is it important to solve it?

This is a problem because fundamental analysis is very time consuming and labor intensive. Investors would have to collect a large amount of data and analyze it from various sources to make a good and meaningful investment.

In addition, human error can also occur very easily, as it is possible to miss an important metric or make mistakes when analyzing the data manually.

It is important for us to solve this problem because our solution can save investors time and effort by automating the analysis process and providing them with the key indicators they need to make informed decisions. This can help investors make better investment decisions, reduce the risk of errors, and ultimately lead to better investment outcome. It is important for us to solve this problem because our solution can save investors time and effort by automating the analysis process and providing them with the key indicators they need to make informed decisions. This can help investors make better investment decisions, reduce the risk of errors, and ultimately lead to better investment results

# 2. Purpose of the Project: What exactly do we plan to do to solve the problem?

We aim to provide investors with an easier way to perform fundamental analysis by creating a solution that generates a table of the 12 most important stock indicators using a stock ticker such as "IBM". Our solution will utilize the Alpha Vantage API (AVlink) to gather the necessary data for the indicators. Additionally, we will also calculate the indicators ourselves using Alpha Vantage to provide a comparison between the API-generated indicators and our own calculations. This solution will make the process of analyzing stock data more efficient and provide investors with the information they need to make informed investment decisions.

# 3. Approach: How exactly is the goal to be achieved?

To work out the most important stock ratios we watched a video of the Youtuber Finanzfluss (link to the video). After that we had to choose where to get the key figures from, but since our colleague Edgar Kinetz already compared the best APIs for financial data in his project, it was immediately clear that we would use the Alpha Vantage API. This API is very comprehensive and potentially free of charge. The key figures of the companies and their shares can be found in the section "Core Stock APIs" and "Fundamental Data" and can be accessed with the provided API requests.

## Problems with the approach

One problem we encountered right at the beginning is that the free version of the API is very limited. 5 API requests per minute and 500 requests per day was clearly too little for us, because in the worst case we already have 5 API requests in one function. However, we were able to get in touch with a member of staff at Alpha Vantage and with the help of Prof. Schaible and Steve we now have access to the Academic Access version of the API with 150 API requests per minute and no daily limit.

## Data research
