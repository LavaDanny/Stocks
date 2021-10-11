# Demo of yfinance usage with matplotlib

# Import yfinance and matplotlib
import yfinance as yf  
import matplotlib.pyplot as plt
import sqlite3
from sqlite3 import Error
import pandas as pd

def download(bt_inputs, proxy = None):
    data = yf.download(tickers= bt_inputs['tickers'],
                       start = bt_inputs['start_date'],   
                       end = bt_inputs['end_date'],
                       interval = '1d',
                       prepost = True,
                       threads = True,
                       proxy = proxy)
    return data

# backtest inputs
bt_inputs = {'tickers': ['BA', 'UNH', 'MCD', 'HD'],
'start_date': '2019-01-01',
'end_date': '2021-08-01'}

# create a sql connection
con = sqlite3.connect('stock.db')
c = con.cursor()

# create price table
# query1 = """CREATE TABLE IF NOT EXISTS prices (
# Date TEXT NOT NULL,
# ticker TEXT NOT NULL,
# price REAL,
# PRIMARY KEY(Date, ticker)
# )"""
# c.execute(query1.replace('\n',' '))

# create volume table
# query2 = """CREATE TABLE IF NOT EXISTS volume (
# Date TEXT NOT NULL,
# ticker TEXT NOT NULL,
# volume REAL,
# PRIMARY KEY(Date, ticker)
# )"""
# c.execute(query2.replace('\n',' '))

test = download(bt_inputs)

adj_close = test['Adj Close']
volume = test['Volume']

# convert wide to long
adj_close_long = pd.melt(adj_close.reset_index(), id_vars='Date', value_vars=bt_inputs['tickers'], var_name ="ticker", value_name="price")
volume_long = pd.melt(volume.reset_index(), id_vars='Date', value_vars=bt_inputs['tickers'], var_name = "ticker", value_name = "volume")

adj_close_long.to_sql('prices', con, if_exists='replace', index=False)
volume_long.to_sql('volume', con, if_exists='replace', index=False)

# inputs
select_tickers = bt_inputs['tickers']
start_date = bt_inputs['start_date']
end_date = bt_inputs['end_date']
# construct query
query = """
select * from prices
where ticker in ('"""+ "','".join(select_tickers) + """')
and Date >= '"""+ start_date + """'
and Date < '""" + end_date + "'"
c.execute(query.replace('\n',' '))
result = pd.DataFrame(c.fetchall(), columns = ['Date', 'ticker', 'price'])
# convert to datetime
result['Date'] = pd.to_datetime(result['Date'])

