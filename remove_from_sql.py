import matplotlib.pyplot as plt
import sqlite3

# make db connection
con = sqlite3.connect('C:\\Users\\LavaDanny\\Desktop\\Coding\\Stocks\\stock.db')
c = con.cursor()

# delete specific data
c.execute("DELETE FROM prices WHERE ticker = 'HD'")

con.commit()
con.close()