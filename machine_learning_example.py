import matplotlib.pyplot as plt
from pandas.core.frame import DataFrame
import aws_config
import mysql.connector
import pandas as pd

def exponential_smooth(data, alpha):
    """
    Function that exponentially smooths dataset so values are less 'rigid'
    :param alpha: weight factor to weight recent values more
    """
    
    return data.ewm(alpha=alpha).mean()

def produce_prediction(data, window):
    """
    Function that produces the 'truth' values
    At a given row, it looks 'window' rows ahead to see if the price increased (1) or decreased (0)
    :param window: number of days, or rows to look ahead to see what the price did
    """
    window = 15

    prediction = (data.shift(-window) >= data)
    prediction = prediction.iloc[:-window]
    data['pred'] = prediction.astype(int)
    
    return data

# connect to aws rds
con = mysql.connector.connect(
        host = aws_config.host,
        user = aws_config.user,
        password = aws_config.pw)

c = con.cursor()

# select and print all data
c.execute("USE db1")
c.execute("SELECT * FROM prices")

allData = []
prices = []
dates = []
tickers = []

# save data in arrays
for row in c.fetchall():
    # allData.append(row)
    prices.append(row[3])
    if(row[2] not in tickers):
        tickers.append(row[2])
    dates.append(row[1])

# change price data to dataframe and smooth
data = pd.DataFrame(prices)
data = exponential_smooth(data, 0.65)

prices = data.values.tolist()

# get list lengths
numTickers = len(tickers)
numPricesPerTicker = len(prices) / numTickers

# display data per ticker
startIndex = 0
endIndex = int(numPricesPerTicker)
for x in range(numTickers):
    plt.plot(dates[startIndex:endIndex], prices[startIndex:endIndex], label = tickers[x])
    plt.title(tickers[x])

    startIndex += int(numPricesPerTicker)
    endIndex += int(numPricesPerTicker)

plt.ylabel('Prices ($)')
plt.xlabel('Date')
plt.legend()
plt.show()

data = produce_prediction(data, window=15)
data = data.dropna() # Some indicators produce NaN values for the first few rows, we just remove them here
data.tail()