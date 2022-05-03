import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from stockstats import StockDataFrame, unwrap
import csv
import time

#New Headers
newHeader = ['stockTicker', 'stockName', 'RSI', 'MACD',
    'stochasticOperator', 'Volume', 'Price', 'PriceChange']
companies = csv.reader(open('sp500_companies.csv'))

#DO NOT COPY API KEY ANYWHERE UNSECURE ex. THE INTERNET 
#Actual calling of data into a pandas dataframe
def get_historical_data(symbol, start_date):
    api_key = 'a0aedf30a4374fcca42aee432cad8028'
    api_url = f'https://api.twelvedata.com/time_series?symbol={symbol}&interval=1day&outputsize=5000&apikey={api_key}'
    raw_df = requests.get(api_url).json()
    df = pd.DataFrame(raw_df['values']).iloc[::-
                      1].set_index('datetime').astype(float)
    df = df[df.index >= start_date]
    df.index = pd.to_datetime(df.index)
    return df

#Creation of stock data csv and calling of the api and writing to it. Removes the pandas headers and gives it new ones.
#DO NOT REMOVE SLEEP FUNCTION.
#Use only once in 24 hour period due to API restrictions.
def createDataFromAPI():
    i = 0
    # class is stockstats.stockDataframe
    for company in companies:
        historyFile = 'history/stockData.csv'
        
        f = open(historyFile, 'a+')
        
        symbol, name = company
        
        stockPull = get_historical_data(symbol, '2022-03-01')
        
        newStockPull = StockDataFrame(stockPull)
        
        stockData = newStockPull[['rsi_14','macd','stochrsi','volume', 'close', 'close_-1_d']]
        
        unwrappeddf = unwrap(stockData)
        # for some reason these dont work.
        # unwrappeddf.rename(columns=unwrappeddf.iloc[0]).drop(unwrappeddf.index[0])
        # unwrappeddf.rename(columns={'datetime':'date', 'rsi_14' : 'RSI', 'macd' : 'MACD', 'stochrsi' : 'stochasticOperator','volume' : 'Volume','close' : 'Price', 'close_-1_d' : 'Change'})
        unwrappeddf.insert(0,"stockTicker",symbol)
        
        
        unwrappeddf.insert(0,"stockName",name)
        
        unwrappeddf = unwrappeddf.iloc[5:]
            
        # Use this way to influence header columns names...
        if i == 0:
            f.write(unwrappeddf.to_csv(header=newHeader, index_label="stockDate"))
        else:
            f.write(unwrappeddf.to_csv(header=False,index_label = None))
        i = i + 1
        
        print('Ticker {} done!'.format(symbol))
        print(i)
        
        f.close()
        
        time.sleep(8.1)
        
        
createDataFromAPI()