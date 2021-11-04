import mysql.connector
import aws_config

cnx = mysql.connector.connect(
        host = aws_config.host,
        user = aws_config.user,
        password = aws_config.pw)
print(cnx)


