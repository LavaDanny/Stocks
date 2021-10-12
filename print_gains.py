import matplotlib.pyplot as plt
import sqlite3

# make db connection
con = sqlite3.connect('stock.db')
c = con.cursor()
d = con.cursor()

# get min and max price data
c.execute("SELECT ticker, price, MIN(Date)\
FROM prices GROUP BY ticker")

buyDate = []
for row in c.fetchall():
    buyDate.append(row)

c.execute("SELECT ticker, price, MAX(Date)\
FROM prices GROUP BY ticker")

sellDate = []
for row in c.fetchall():
    sellDate.append(row)

#calculate net gain/loss

i = 0
sum = 0
for x in range(len(buyDate)):
    sum = sellDate[i][1] - buyDate[i][1] + sum
    i += 1

print(sum) 