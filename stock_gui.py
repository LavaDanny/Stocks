from os import remove
import matplotlib.pyplot as plt
import sqlite3
#import tkinter as tk
from tkinter import *

# make db connection
def connect_to_db(con):
    c = con.cursor()
    return c

# updates table data
def remove_ticker(db_con, ticker, con, window, frame_data):

    # remove ticker data from sql db
    query = "DELETE FROM prices WHERE ticker = ?"
    c.execute(query, (ticker,))
    con.commit()

    # destroy window
    window.quit()
    window.destroy()

    # create new window and table
    window = Tk()
    window.title('Hello Python')
    window.geometry("1000x300")

    frame_data = Frame(window)
    data = []
    create_table(db_con, data, window, frame_data)
    create_ticker_dropdown(db_con, window)

    # start window
    window.mainloop()
     
# create table
def create_table(db_con, data, window, frame_data):

    # get min and max price data
    db_con.execute("SELECT ticker, price, MIN(Date)\
    FROM prices GROUP BY ticker")

    buyDate = []
    for row in db_con.fetchall():
        buyDate.append(row)

    db_con.execute("SELECT ticker, price, MAX(Date)\
    FROM prices GROUP BY ticker")

    sellDate = []
    for row in db_con.fetchall():
        sellDate.append(row)

    frame_data.grid(row = 0, column = 0)
    data = buyDate + sellDate
    frame_data = Table(window, data)

# create ticker drop down
def create_ticker_dropdown(db_con, window):
    tickers = StringVar(window)
    tickers_arr = []

    db_con.execute("SELECT ticker, price, MIN(Date)\
    FROM prices GROUP BY ticker")

    buyDate = []
    for row in db_con.fetchall():
        buyDate.append(row)

    for x in buyDate:
        tickers_arr.append(x[0])
    print(tickers_arr)

    tickers.set(tickers_arr[0])
    menu_ticker = OptionMenu(window, tickers, *tickers_arr)
    menu_ticker.grid(row = 10, column = 1, padx = 10, pady = 10)

    remove_btn = Button(window, text = "remove selected ticker", command = lambda: remove_ticker(c, tickers.get(), con, window, frame_data))
    remove_btn.grid(row = 10, column = 2)
    #remove_btn.bind('<Button-1', remove_ticker(c))

# class to create table using sql data (sellDates for now)
class Table:
    def __init__(self, window, data):

        data.sort(key = lambda t: (t[0], t[2]))

        for i in range(len(data)):
            for j in range(len(data[0])):
                self.e = Entry(window, width=20)#, fg='blue', font=('Arial',16,'bold'))
                self.e.grid(row = i, column = j)
                self.e.insert(END, data[i][j])

# make db connection
con = sqlite3.connect('C:\\Users\\LavaDanny\\Desktop\\Coding\\Stocks\\stock.db')
c = connect_to_db(con)

# tkinter window
window = Tk()

window.title('Hello Python')
window.geometry("1000x300")

# create stock table
frame_data = Frame(window)
data = []
create_table(c, data, window, frame_data)

# tickers drop down
create_ticker_dropdown(c, window)

# start window
window.mainloop()
