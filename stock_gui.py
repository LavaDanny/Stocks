import matplotlib.pyplot as plt
import sqlite3
#import tkinter as tk
from tkinter import *

# make db connection
def connect_to_db():
    con = sqlite3.connect('C:\\Users\\LavaDanny\\Desktop\\Coding\\Stocks\\stock.db')
    c = con.cursor()
    return c

# create table using sql data (sellDates for now)
class Table:
    def __init__(self, window, data):

        data.sort(key = lambda t: (t[0], t[2]))

        for i in range(len(data)):
            for j in range(len(data[0])):
                self.e = Entry(window, width=20)#, fg='blue', font=('Arial',16,'bold'))
                self.e.grid(row = i, column = j)
                self.e.insert(END, data[i][j])

# make db connection
c = connect_to_db()

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

# tkinter window
window = Tk()

window.title('Hello Python')
window.geometry("1000x300")

# create stock table
frame_data = Frame(window)
frame_data.grid(row = 0, column = 0)
data = buyDate + sellDate
frame_data = Table(window, data)

# tickers drop down
tickers = StringVar(window)
tickers_arr = []

for x in buyDate:
    tickers_arr.append(x[0])
print(tickers_arr)

tickers.set(tickers_arr[0])
menu_ticker = OptionMenu(window, tickers, *tickers_arr)
menu_ticker.grid(row = 10, column = 1, padx = 10, pady = 10)

# start window
window.mainloop()
