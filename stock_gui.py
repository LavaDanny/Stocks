import matplotlib.pyplot as plt
import sqlite3
import tkinter as tk

# create table using sql data (sellDates for now)
class Table:
    def __init__(self, window, data):

        data.sort(key = lambda t: (t[0], t[2]))

        for i in range(len(data)):
            for j in range(len(data[0])):
                self.e = tk.Entry(window, width=20, fg='blue', font=('Arial',16,'bold'))
                self.e.grid(row = i, column = j)
                self.e.insert(tk.END, data[i][j])

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

# rows = len(sellDate)
# columns = len(sellDate[0])

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
window.geometry("1000x300")

frame_data = tk.Frame(window)
data = buyDate + sellDate
frame_data = Table(window, data)


window.mainloop()
