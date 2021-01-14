# https://youtu.be/bdlwwmVWfPg
# Double Exponential Moving Average


import numpy as np
import pandas as pd
import pandas_datareader as pdr
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

df = pdr.DataReader("AMZN", start='2019-03-04', end='2020-08-14', data_source='yahoo')

plt.figure(figsize=(12.2, 4.5))
plt.plot(df['Close'], label = 'Close Price')
plt.xticks(rotation=45)
plt.title('Amazon Close Price')
plt.xlabel('Date')
plt.ylabel('Close price USD')
plt.legend(loc='upper left')
plt.show()

def DEMA(data, time_period, column):
    EMA = data[column].ewm(span=time_period, adjust=False).mean()
    DEMA = 2 * EMA - EMA.ewm(span=time_period, adjust=False).mean()

    return DEMA

df['DEMA_short'] = DEMA(df, 20, 'Close')
df['DEMA_long'] = DEMA(df, 50, 'Close')

plt.figure(figsize=(12.2, 4.5))
plt.plot(df['Close'], label = 'Close Price')
plt.plot(df['DEMA_short'], label = 'DEMA_shortg')
plt.plot(df['DEMA_long'], label = 'DEMA_long')
plt.xticks(rotation=45)
plt.title('Amazon Close Price')
plt.xlabel('Date')
plt.ylabel('Close price USD')
plt.legend(loc='upper left')
plt.show()


def buy_sell(data):
    buy_list = []
    sell_list = []
    flag = False

    for i in range(0, len(data)):
        if (data['DEMA_short'][i] > data['DEMA_long'][i]) and flag == False:
            buy_list.append(data['Close'][i])
            sell_list.append(np.nan)
            flag = True
        elif data['DEMA_short'][i] < data['DEMA_long'][i] and flag == True:
            buy_list.append(np.nan)
            sell_list.append(data['Close'][i])
            flag = False
        else:
            buy_list.append(np.nan)
            sell_list.append(np.nan)
            
    data['Buy'] = buy_list
    data['Sell'] = sell_list


buy_sell(df)

plt.figure(figsize=(12.2, 4.5))
plt.scatter(df.index, df['Buy'], color='green', label='Buy Signal', marker='^', alpha=1)
plt.scatter(df.index, df['Sell'], color='red', label='Sell Signal', marker='v', alpha=1)
plt.plot(df['Close'], label = 'Close Price', alpha=0.35)
plt.plot(df['DEMA_short'], label = 'DEMA_shortg', alpha=0.35)
plt.plot(df['DEMA_long'], label = 'DEMA_long', alpha=0.35)
plt.xticks(rotation=45)
plt.title('Close Price Buy & Sell Signals')
plt.xlabel('Date')
plt.ylabel('Close price USD')
# plt.legend('Close', loc='upper left')
plt.legend()
plt.show()

