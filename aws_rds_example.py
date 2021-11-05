import mysql.connector
import aws_config
# Import yfinance and matplotlib
import yfinance as yf  
import matplotlib.pyplot as plt
import sqlite3
from sqlite3 import Error
import pandas as pd
from sqlalchemy import create_engine

def download(bt_inputs, proxy = None):
    data = yf.download(tickers= bt_inputs['tickers'],
                       start = bt_inputs['start_date'],   
                       end = bt_inputs['end_date'],
                       interval = '1d',
                       prepost = True,
                       threads = True,
                       proxy = proxy)
    return data

con = mysql.connector.connect(
        host = aws_config.host,
        user = aws_config.user,
        password = aws_config.pw)

c = con.cursor()

c.execute("USE db1")

# create price table
query1 = """CREATE TABLE IF NOT EXISTS prices (
Date VARCHAR(20),
ticker VARCHAR(5),
price REAL,
PRIMARY KEY(Date, ticker)
)"""
c.execute(query1.replace('\n',' '))

# create volume table
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