import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from stockstats import StockDataFrame

def get_historical_data(symbol, start_date):
    api_key = 'a0aedf30a4374fcca42aee432cad8028'
    api_url = f'https://api.twelvedata.com/time_series?symbol={symbol}&interval=1day&outputsize=5000&apikey={api_key}'
    raw_df = requests.get(api_url).json()
    df = pd.DataFrame(raw_df['values']).iloc[::-1].set_index('datetime').astype(float)
    df = df[df.index >= start_date]
    df.index = pd.to_datetime(df.index)
    return df


def createDiagramsFunc(userInputTicker):

    userInputData = get_historical_data(userInputTicker, '2022-04-01')

    userInputDataFrame = StockDataFrame(userInputData)

    buy_signals = userInputDataFrame['close_50_sma_xd_close_20_sma']

    sell_signals = userInputDataFrame['close_20_sma_xd_close_50_sma']

    for i in range(len(buy_signals)):
        if buy_signals.iloc[i] == True:
            buy_signals.iloc[i] = userInputDataFrame.close[i]
        else:
            buy_signals.iloc[i] = np.nan

    for i in range(len(sell_signals)):
        if sell_signals.iloc[i] == True:
            sell_signals.iloc[i] = userInputDataFrame.close[i]
        else:
            sell_signals.iloc[i] = np.nan
            
    plt.plot(userInputDataFrame['close'], linewidth = 2.5, label = userInputTicker + "Price")
    plt.plot(userInputDataFrame['close_20_sma'], linewidth = 2.5, alpha = 0.6, label = 'SMA 20')
    plt.plot(userInputDataFrame['close_50_sma'], linewidth = 2.5, alpha = 0.6, label = 'SMA 50')
    plt.plot(userInputDataFrame.index, buy_signals, marker = '^', markersize = 15, color = 'green', linewidth = 0, label = 'BUY SIGNAL')
    plt.plot(userInputDataFrame.index, sell_signals, marker = 'v', markersize = 15, color = 'r', linewidth = 0, label = 'SELL SIGNAL')
    plt.legend(loc = 'upper left')
    plt.title(userInputTicker + ' SMA 20,50 CROSSOVER STRATEGY SIGNALS')
    figure = plt.gcf()
    figure.set_size_inches(12, 5)
    plt.savefig('stockImageDataFor{}.png'.format(userInputTicker), dpi=100)