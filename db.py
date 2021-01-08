import mysql.connector

mydb1 = mysql.connector.connect(host = "localhost", user = "root", passwd = "", db = "news")

cursor = mydb1.cursor()
