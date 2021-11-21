import matplotlib.pyplot as plt
import aws_config
import mysql.connector

# connect to aws rds
con = mysql.connector.connect(
        host = aws_config.host,
        user = aws_config.user,
        password = aws_config.pw)

c = con.cursor()
c.execute("USE db1")
c.execute("SELECT * FROM prices")

allData = []
for row in c.fetchall():
    allData.append(row)
    print(row)