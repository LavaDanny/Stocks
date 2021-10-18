import matplotlib.pyplot as plt
import sqlite3
import tkinter as tk

# create table using sql data (sellDates for now)
class Table:
    def __init__(self, window):
        for i in range(rows):
            for j in range(columns):
                self.e = tk.Entry(window, width=20, fg='blue', font=('Arial',16,'bold'))
                self.e.grid(row = i, column = j)
                self.e.insert(tk.END, sellDate[i][j])

# make db connection
con = sqlite3.connect('C:\\Users\\LavaDanny\\Desktop\\Coding\\Stocks\\stock.db')
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

rows = len(sellDate)
columns = len(sellDate[0])

#calculate net gain/loss

i = 0
sum = 0
for x in range(len(buyDate)):
    sum = sellDate[i][1] - buyDate[i][1] + sum
    i += 1

print(sum) 

# tkinter window
window = tk.Tk()

window.title('Hello Python')
window.geometry("1000x200+10+20")

frame_data = tk.Frame(window)
frame_data = Table(window)


window.mainloop()
