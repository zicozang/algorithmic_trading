# https://youtu.be/rO_cqa4x60o


import numpy as np
import pandas as pd
import pandas_datareader as pdr
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

df = pdr.DataReader("TSLA", start='2019-11-18', end='2020-06-09', data_source='yahoo')

plt.figure(figsize=(12.2, 4.5))
plt.plot(df['Close'], label = 'Close Price')
plt.title('TESLA Close Price')
plt.xlabel('Date')
plt.ylabel('Close price USD')
plt.legend(loc='upper left')
plt.show()

ShortEMA = df.Close.ewm(span=5, adjust=False).mean()
MiddleEMA = df.Close.ewm(span=21, adjust=False).mean()
LongEMA = df.Close.ewm(span=63, adjust=False).mean()

plt.figure(figsize=(12.2, 4.5))
plt.plot(df['Close'], label = 'Close Price', color='blue')
plt.plot(ShortEMA, label='Short/Fast EMA', color='red')
plt.plot(MiddleEMA, label='Middle/Medium EMA', color='orange')
plt.plot(LongEMA, label='Long/Slow EMA', color='green')
plt.title('TESLA Close Price')
plt.xlabel('Date')
plt.ylabel('Close price USD')
plt.legend(loc='upper left')
plt.show()

df['Short'] = ShortEMA
df['Middle'] = MiddleEMA
df['Long'] = LongEMA

def buy_sell_function(data):
    buy_list = []
    sell_list = []
    flag_long = False
    flag_short = False

    for i in range(0, len(data)):

        if data['Middle'][i] < data['Long'][i] and data['Short'][i] < data['Middle'][i] and flag_long == False and flag_short == False:
            buy_list.append(data['Close'][i])
            sell_list.append(np.nan)
            flag_short = True
        elif flag_short == True and data['Short'][i] > data['Middle'][i]:
            sell_list.append(data['Close'][i])
            buy_list.append(np.nan)
            flag_short = False
        elif data['Middle'][i] > data['Long'][i] and data['Short'][i] > data['Middle'][i] and flag_long == False and flag_short == False:
            buy_list.append(data['Close'][i])
            sell_list.append(np.nan)
            flag_long = True
        elif flag_long == True and data['Short'][i] < data['Middle'][i]:
            sell_list.append(data['Close'][i])
            buy_list.append(np.nan)
            flag_long = False
        else:
            sell_list.append(np.nan)
            buy_list.append(np.nan)

    return (buy_list, sell_list)

df['Buy'] = buy_sell_function(df)[0]
df['Sell'] = buy_sell_function(df)[1]


plt.figure(figsize=(12.2, 4.5))
plt.plot(df['Close'], label = 'Close Price', color='blue', alpha=0.35)
plt.plot(ShortEMA, label='Short/Fast EMA', color='red', alpha=0.35)
plt.plot(MiddleEMA, label='Middle/Medium EMA', color='orange', alpha=0.35)
plt.plot(LongEMA, label='Long/Slow EMA', color='green', alpha=0.35)
plt.scatter(df.index, df['Buy'], color='green', marker='^', alpha=1)
plt.scatter(df.index, df['Sell'], color='red', marker='v', alpha=1)
plt.title('TESLA Buy & Sell Plot')
plt.xlabel('Date')
plt.ylabel('Close price USD')
plt.legend(loc='upper left')
plt.show()













