import mysql.connector

db=mysql.connector.connect(
     host="localhost",       # or your server IP
    user="root",            # your MySQL username
    password="root" # your MySQL password
)
my_cursor=db.cursor()
# my_cursor.execute("CREATE DATABASE users")
my_cursor.execute("show databases")

for i in my_cursor:
    print(i)