# Demo of yfinance usage with matplotlib

# Import yfinance and matplotlib
import yfinance as yf  
import matplotlib.pyplot as plt
import sqlite3
from sqlite3 import Error

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

# Get the data for the SPY ETF by specifying the stock ticker, start date, and end date
data = yf.download('SPY','2015-01-01','2015-01-10')

print(data)
print('\n')

for row in data.iterrows():
    print(row[0])

# Plot the close prices
data["Adj Close"].plot()
plt.show()

# Attempt to make connection and add to SQLite db
connection = create_connection("C:\\sqlite\SQLiteStudio\demo.db")
