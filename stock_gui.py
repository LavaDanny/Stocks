from os import remove
import matplotlib.pyplot as plt
import sqlite3
from tkinter import *
import mysql.connector
import aws_config
from sqlalchemy import create_engine
import yfinance as yf  
import pandas as pd

# download data from yahoo based on tickers and dates
def download(bt_inputs, proxy = None):
    data = yf.download(tickers= bt_inputs['tickers'],
                       start = bt_inputs['start_date'],   
                       end = bt_inputs['end_date'],
                       interval = '1d',
                       prepost = True,
                       threads = True,
                       proxy = proxy)
    return data

# make a new window
def create_window(db_con):
    # tkinter window
    window = Tk()

    # define window
    window.title('Stock Window')
    window.geometry("1000x1000")

    # create stock table
    create_table(db_con, window)

    # tickers drop down
    create_ticker_dropdown(db_con, window)

    # create text entry to get new tickers
    create_text_entry(window)

    # create button to reset db
    reset_db_button(window, db_con)

    return window

# button to reset db to default
def reset_db_button(window, db_con):
    reset_btn = Button(window, text = "reset db", command = lambda: reset_db(window, db_con))
    reset_btn.grid(row = 11, column = 1)

# set db with default values
def reset_db(window, db_con):

    # create price table if non existent
    query1 = """CREATE TABLE IF NOT EXISTS prices (
    Date VARCHAR(20),
    ticker VARCHAR(5),
    price REAL,
    PRIMARY KEY(Date, ticker)
    )"""
    c.execute(query1.replace('\n',' '))

    # create volume table if nonexistent 
    query2 = """CREATE TABLE IF NOT EXISTS volume (
    Date VARCHAR(20),
    ticker VARCHAR(5),
    volume REAL,
    PRIMARY KEY(Date, ticker)
    )"""
    c.execute(query2.replace('\n',' '))

    # backtest inputs
    bt_inputs = {'tickers': ['BA', 'UNH', 'MCD', 'HD'],
    'start_date': '2018-01-01',
    'end_date': '2019-08-01'}

    test = download(bt_inputs)

    adj_close = test['Adj Close']
    volume = test['Volume']

    # convert wide to long
    adj_close_long = pd.melt(adj_close.reset_index(), id_vars='Date', value_vars=bt_inputs['tickers'], var_name ="ticker", value_name="price")
    volume_long = pd.melt(volume.reset_index(), id_vars='Date', value_vars=bt_inputs['tickers'], var_name = "ticker", value_name = "volume")

    # add data to aws rds
    engine = create_engine('mysql://' + aws_config.user + ':' + aws_config.pw + '@' + aws_config.host + '/' + aws_config.database)
    con = engine.connect()
    adj_close_long.to_sql(name='prices', con=con, if_exists='replace')
    volume_long.to_sql(name='volume', con=con, if_exists='replace')

    # destroy window
    window.quit()
    window.destroy()

    # create new window and table
    window = create_window(db_con)
    window.mainloop()


# updates table data by creating new window
def remove_ticker(db_con, ticker, con, window):

    # remove ticker data from sql db
    query = "DELETE FROM prices WHERE ticker = %s"
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

# create text entry field
def create_text_entry(window):
    text_entry = Text(window, height = 1, width = 10)
    text_entry.grid(row = 12, column = 1, padx = 10, pady = 10)

    # text indicating use for right box
    l = Label(window, text = "Ticker to be added: ")
    l.grid(row = 12, column = 0, padx = 10, pady = 10)


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
    menu_ticker.grid(row = 10, column = 0, padx = 10, pady = 10)

    remove_btn = Button(window, text = "remove selected ticker", command = lambda: remove_ticker(c, tickers.get(), con, window))
    remove_btn.grid(row = 10, column = 1)
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
# con = sqlite3.connect('C:\\Users\\LavaDanny\\Desktop\\Coding\\Stocks\\stock.db')
# c = con.cursor()

# connect to aws rds
con = mysql.connector.connect(
        host = aws_config.host,
        user = aws_config.user,
        password = aws_config.pw)

c = con.cursor()
c.execute("USE db1")

window = create_window(c)

# start window
window.mainloop()
