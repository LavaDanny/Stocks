import matplotlib.pyplot as plt
import sqlite3

# make db connection
con = sqlite3.connect('C:\\Users\\LavaDanny\\Desktop\\Coding\\Stocks\\stock.db')
c = con.cursor()

# get all data
c.execute("SELECT * FROM prices")

allData = []
for row in c.fetchall():
    allData.append(row)
    print(row)