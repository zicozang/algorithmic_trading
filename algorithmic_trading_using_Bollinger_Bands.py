# https://youtu.be/gEIw2iUlFYc


import numpy as np
import pandas as pd
import pandas_datareader as pdr
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

df = pdr.DataReader("TSLA", start='2016-02-01', end='2017-12-29', data_source='yahoo')

periods = 20
df['SMA'] = df['Close'].rolling(window=periods).mean()
df['STD'] = df['Close'].rolling(window=periods).std()
df['Upper'] = df['SMA'] + (df['STD'] * 2)
df['Lower'] = df['SMA'] - (df['STD'] * 2)

column_list = ['Close', 'SMA', 'Upper', 'Lower']
df[column_list].plot(figsize=(12.2, 4.5))
plt.title('Bollinger Bands for TESLA')
plt.xlabel('Date')
plt.ylabel('Close price USD')
plt.legend(loc='upper left')
plt.show()

fig = plt.figure(figsize=(12.2, 4.5))
ax = fig.add_subplot(1,1,1)
x_axis = df.index
ax.fill_between(x_axis, df['Upper'], df['Lower'], color='gray')
ax.plot(x_axis, df['Close'], color='gold', lw=3, label='Close Price')
ax.plot(x_axis, df['SMA'], color='blue', lw=3, label='Simple Moving Average')
ax.set_title('Bollinger Bands for TESLA')
ax.set_xlabel('Date')
ax.set_ylabel('USD Price')
plt.xticks(rotation=45)
ax.legend()
plt.show()

new_df = df[periods-1:]


def get_signal(data):

    buy_signal = []
    sell_signal = []
    
    for i in range(len(data['Close'])):
        
        if data['Close'][i] > data['Upper'][i]:
            buy_signal.append(np.nan)
            sell_signal.append(data['Close'][i])
        elif data['Close'][i] < data['Lower'][i]:
            buy_signal.append(data['Close'][i])
            sell_signal.append(np.nan)
        else:
            buy_signal.append(np.nan)
            sell_signal.append(np.nan)
        
    return(buy_signal, sell_signal)
            
new_df['Buy'], new_df['Sell'] = get_signal(new_df)


fig = plt.figure(figsize=(12.2, 4.5))
ax = fig.add_subplot(1,1,1)
x_axis = new_df.index
ax.fill_between(x_axis, new_df['Upper'], new_df['Lower'], color='gray')
ax.plot(x_axis, new_df['Close'], color='gold', lw=3, label='Close Price', alpha=0.5)
ax.plot(x_axis, new_df['SMA'], color='blue', lw=3, label='Simple Moving Average', alpha=0.5)
ax.scatter(x_axis, new_df['Buy'], color='green', lw=3, label='Buy', marker='^', alpha=1)
ax.scatter(x_axis, new_df['Sell'], color='red', lw=3, label='Sell', marker='v', alpha=1)
ax.set_title('Bollinger Bands for TESLA')
ax.set_xlabel('Date')
ax.set_ylabel('USD Price')
plt.xticks(rotation=45)
ax.legend()
plt.show()


