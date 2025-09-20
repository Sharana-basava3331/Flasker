import mysql.connector

check local
)
my_cursor=db.cursor()
# my_cursor.execute("CREATE DATABASE users")
my_cursor.execute("show databases")

for i in my_cursor:
    print(i)
