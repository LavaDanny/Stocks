import matplotlib.pyplot as plt
import aws_config
import mysql.connector

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

numTickers = len(tickers)
numPricesPerTicker = len(prices) / numTickers

# display data per ticker
startIndex = 0
endIndex = int(numPricesPerTicker)
for x in range(numTickers):
    plt.plot(dates[startIndex:endIndex], prices[startIndex:endIndex])
    plt.title(tickers[x])
    plt.ylabel('Prices ($)')
    plt.xlabel('Date')
    plt.show()

    startIndex += int(numPricesPerTicker)
    endIndex += int(numPricesPerTicker)

