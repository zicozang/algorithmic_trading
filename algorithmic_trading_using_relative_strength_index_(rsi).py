# https://youtu.be/fxLsSax7rvY

import numpy as np
import pandas as pd
import pandas_datareader as pdr
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

df = pdr.DataReader("FB", start='2019-05-20', end='2020-05-20', data_source='yahoo')

plt.figure(figsize=(12.2, 4.5))
plt.plot(df.index, df['Adj Close'], label = 'Adj Close Price')
plt.title('Facebook Adj. Close Price')
plt.xlabel('MAy 20, 2019 ~ May 20, 2020')
plt.ylabel('Adj Close price USD')
plt.legend(loc='upper left')
plt.show()

delta = df['Adj Close'].diff(1)
delta = delta.dropna()

up = delta.copy()
down = delta.copy()

up[up<0] = 0
down[down>0] = 0

period = 14
AVG_Gain = up.rolling(window=period).mean()
AVG_Loss = abs(down.rolling(window=period).mean())

RS = AVG_Gain / AVG_Loss
RSI = 100.0 - (100.0 / (1.0 + RS))

plt.figure(figsize=(12.2, 4.5))
RSI.plot()
plt.show()

new_df = pd.DataFrame()
new_df['Adj Close'] = df['Adj Close']
new_df['RSI'] = RSI

fig, ax1 = plt.subplots()
ax1.set_title('Facebook Adj. Close Price')
ax1.set_xlabel('MAy 20, 2019 ~ May 20, 2020')
ax1.plot(new_df.index, new_df['Adj Close'], label = 'Adj Close Price')
ax1.set_ylabel('Adj Close price USD')
ax1.grid(False)

ax2 = ax1.twinx()
ax2.set_ylabel('RSI')
ax2.plot(new_df.index, new_df['RSI'], color='yellow', label = 'RSI')
ax2.grid(False)
ax2.axhline(0, linestyle='--', alpha=0.5, color='gray')
ax2.axhline(10, linestyle='--', alpha=0.5, color='orange')
ax2.axhline(20, linestyle='--', alpha=0.5, color='green')
ax2.axhline(30, linestyle='--', alpha=0.5, color='red')
ax2.axhline(70, linestyle='--', alpha=0.5, color='red')
ax2.axhline(80, linestyle='--', alpha=0.5, color='green')
ax2.axhline(90, linestyle='--', alpha=0.5, color='orange')
ax2.axhline(100, linestyle='--', alpha=0.5, color='gray')
fig.set_size_inches(12.2, 4.5)
plt.show()



