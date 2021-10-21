from os import remove
import matplotlib.pyplot as plt
import sqlite3
from tkinter import *

# make a new window
def create_window(db_con):
    # tkinter window
    window = Tk()

    window.title('Hello Python')
    window.geometry("1000x300")

    # create stock table
    create_table(db_con, window)

    # tickers drop down
    create_ticker_dropdown(db_con, window)

    return window

# updates table data
def remove_ticker(db_con, ticker, con, window):

    # remove ticker data from sql db
    query = "DELETE FROM prices WHERE ticker = ?"
    c.execute(query, (ticker,))
    con.commit()

    # destroy window
    window.quit()
    window.destroy()

    # create new window and table
    window = create_window(db_con)

    # start window
    window.mainloop()
     
# create table
def create_table(db_con, window):

    data = []
    frame_data = Frame(window)

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

# create ticker drop down and remove button
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

    remove_btn = Button(window, text = "remove selected ticker", command = lambda: remove_ticker(c, tickers.get(), con, window))
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
c = con.cursor()

window = create_window(c)

# start window
window.mainloop()
