# https://youtu.be/kz_NJERCgm8


import numpy as np
import pandas as pd
import pandas_datareader as pdr
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

df = pdr.DataReader("AAPL", start='2017-04-20', end='2017-08-24', data_source='yahoo')

plt.figure(figsize=(12.2, 4.5))
plt.plot(df['Close'], label = 'Close Price')
plt.xticks(rotation=45)
plt.title('Apple Close Price')
plt.xlabel('Date')
plt.ylabel('Close price USD')
plt.legend(loc='upper left')
plt.show()

ShortEMA = df.Close.ewm(span=12, adjust=False).mean()
LongEMA = df.Close.ewm(span=26, adjust=False).mean()
MACD = ShortEMA - LongEMA
signal = MACD.ewm(span=9, adjust=False).mean()

plt.figure(figsize=(12.2, 4.5))
plt.plot(df.index, MACD, label='AAPL MACD', color='red')
plt.plot(df.index, signal, label='Signal9', color='blue')
plt.xticks(rotation=45)
plt.legend(loc='upper left')
plt.show()

df['MACD'] = MACD
df['Signal Line'] = signal

def buy_sell(signal):
    buy = []
    sell = []
    flag = -1

    for i in range(0, len(signal)):
        if signal['MACD'][i] > signal['Signal Line'][i]:
            sell.append(np.nan)
            if flag != 1:
                buy.append(signal['Close'][i])
                flag = 1
            else:
                buy.append(np.nan)
        elif signal['MACD'][i] < signal['Signal Line'][i]:
            buy.append(np.nan)
            if flag != 0:
                sell.append(signal['Close'][i])
                flag = 0
            else:
                sell.append(np.nan)
        else:
            buy.append(np.nan)
            sell.append(np.nan)

    return (buy, sell)

a = buy_sell(df)
df['Buy_Signal_Price'] = a[0]
df['Sell_Signal_Price'] = a[1]

plt.figure(figsize=(12.2, 4.5))
plt.scatter(df.index, df['Buy_Signal_Price'], color='green', label='Buy', marker='^', alpha=1)
plt.scatter(df.index, df['Sell_Signal_Price'], color='red', label='Sell', marker='v', alpha=1)
plt.plot(df['Close'], label = 'Close Price')
plt.xticks(rotation=45)
plt.title('Close Price Buy & Sell Signals')
plt.xlabel('Date')
plt.ylabel('Close price USD')
plt.legend('Close', loc='upper left')
plt.show()

