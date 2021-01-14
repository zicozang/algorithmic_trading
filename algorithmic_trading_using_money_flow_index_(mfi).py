# https://youtu.be/tF1Lz4WBQwM


import numpy as np
import pandas as pd
import pandas_datareader as pdr
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

df = pdr.DataReader("AAPL", start='2010-10-01', end='2011-09-09', data_source='yahoo')

plt.figure(figsize=(12.2, 4.5))
plt.plot(df['Close'], label = 'Close Price')
plt.title('Apple Close Price')
plt.xlabel('Date')
plt.ylabel('Close price USD')
plt.legend(loc='upper left')
plt.show()

typical_price = (df['Close'] + df['High'] + df['Low']) / 3

period = 14

money_flow = typical_price * df['Volume']

positive_flow = []
negative_flow = []

for i in range(1, len(typical_price)):
    if typical_price[i] > typical_price[i-1]:
        positive_flow.append(money_flow[i-1])
        negative_flow.append(0)
    elif typical_price[i] < typical_price[i-1]:
        negative_flow.append(money_flow[i-1])
        positive_flow.append(0)
    else:
        negative_flow.append(0)
        positive_flow.append(0)

positive_mf = []
negative_mf = []

for i in range(period-1, len(positive_flow)):
    positive_mf.append(sum(positive_flow[i+1- period: i+1]))
for i in range(period-1, len(negative_flow)):
    negative_mf.append(sum(negative_flow[i+1- period: i+1]))

mfi = 100 * (np.array(positive_mf) / (np.array(positive_mf) + np.array(negative_mf)))

df2 = pd.DataFrame()
df2['MFI'] = mfi

plt.figure(figsize=(12.2, 4.5))
plt.plot(df2['MFI'], label = 'MFI')
plt.axhline(10, linestyle= '--', color='orange')
plt.axhline(20, linestyle= '--', color='blue')
plt.axhline(80, linestyle= '--', color='blue')
plt.axhline(90, linestyle= '--', color='orange')
plt.title('Money Flow Index')
plt.xlabel('MFI')
plt.ylabel('MFI Values')
plt.show()

new_df = pd.DataFrame()
new_df = df[period:].copy()
new_df['MFI'] = mfi


def get_signal(data, high, low):
    buy_signal = []
    sell_signal = []

    for i in range(len(data['MFI'])):
        if data['MFI'][i] > high:
            buy_signal.append(np.nan)
            sell_signal.append(data['Close'][i])
        elif data['MFI'][i] < low:
            buy_signal.append(data['Close'][i])
            sell_signal.append(np.nan)
        else:
            buy_signal.append(np.nan)
            sell_signal.append(np.nan)

    return buy_signal, sell_signal

new_df['Buy'] = get_signal(new_df, 80, 20)[0]
new_df['Sell'] = get_signal(new_df, 80, 20)[1]


plt.figure(figsize=(12.2, 4.5))
plt.plot(new_df['Close'], label = 'Close Price', alpha=0.5)
plt.scatter(new_df.index, new_df['Buy'], color='green', label='Buy Signal', marker='^', alpha=1)
plt.scatter(new_df.index, new_df['Sell'], color='red', label='Sell Signal', marker='v', alpha=1)
plt.title('Apple Close Price')
plt.xlabel('Date')
plt.ylabel('Close price USD')
plt.legend(loc='upper left')
plt.show()

plt.figure(figsize=(12.2, 4.5))
plt.plot(new_df['MFI'], label = 'MFI')
plt.axhline(10, linestyle= '--', color='orange')
plt.axhline(20, linestyle= '--', color='blue')
plt.axhline(80, linestyle= '--', color='blue')
plt.axhline(90, linestyle= '--', color='orange')
plt.title('Money Flow Index')
plt.xlabel('MFI')
plt.ylabel('MFI Values')
plt.show()







