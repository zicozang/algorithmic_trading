# https://youtu.be/SEQbb8w7VTw


import numpy as np
import pandas as pd
import pandas_datareader as pdr
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

df = pdr.DataReader("AAPL", start='2006-10-02', end='2011-12-30', data_source='yahoo')

plt.figure(figsize=(12.5, 4.5))
plt.plot(df['Close'], label = 'Close Price')
plt.xticks(rotation=45)
plt.title('Apple Close Price')
plt.xlabel('Date')
plt.ylabel('Close price USD')
plt.legend(loc='upper left')
plt.show()


SMA30 = pd.DataFrame()
SMA30['Close'] = df['Close'].rolling(window=30).mean()

SMA100 = pd.DataFrame()
SMA100['Close'] = df['Close'].rolling(window=100).mean()

plt.figure(figsize=(12.5, 4.5))
plt.plot(df['Close'], label = 'Close Price')
plt.plot(SMA30['Close'], label = 'SMA 30')
plt.plot(SMA100['Close'], label = 'SMA 100')
plt.xticks(rotation=45)
plt.title('Apple Close Price')
plt.xlabel('Date')
plt.ylabel('Close price USD')
plt.legend(loc='upper left')
plt.show()

data = pd.DataFrame()
data['AAPL'] = df['Close']
data['SMA30'] = SMA30['Close']
data['SMA100'] = SMA100['Close']


def buy_sell(data):

    sigPriceBuy = []    
    sigPriceSell = []
    flag = -1
    
    for i in range(len(data)):
        
        if data['SMA30'][i] > data['SMA100'][i]:
            if flag != 1:
                sigPriceBuy.append(data['AAPL'][i])
                sigPriceSell.append(np.NaN)
                flag = 1
            else:
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(np.nan)
        elif data['SMA30'][i] < data['SMA100'][i]:
            if flag != 0:
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(data['AAPL'][i])
                flag = 0
            else:
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(np.nan)
        else:
            sigPriceBuy.append(np.nan)
            sigPriceSell.append(np.nan)
                
            
    return (sigPriceBuy, sigPriceSell)
                
data['Buy'], data['Sell'] = buy_sell(data)


plt.figure(figsize=(12.5, 4.5))
plt.plot(data['AAPL'], label = 'Close Price', alpha=0.35)
plt.plot(data['SMA30'], label = 'SMA 30', alpha=0.35)
plt.plot(data['SMA100'], label = 'SMA 100', alpha=0.35)
plt.scatter(data.index, data['Buy'], label='Buy', marker='^', color='green')
plt.scatter(data.index, data['Sell'], label='Sell', marker='v', color='red')
plt.xticks(rotation=45)
plt.title('Apple Close Price')
plt.xlabel('Date')
plt.ylabel('Close price USD')
plt.legend(loc='upper left')
plt.show()

