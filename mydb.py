import mysql.connector

dataBasw = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Wjdals@1129",
)

# Prepare a cursor object using cursor() method
cursorObject = dataBasw.cursor()

# Drop the database if it exists
cursorObject.execute("DROP DATABASE IF EXISTS elderco")

# Create the database
cursorObject.execute("CREATE DATABASE elderco")
print("Database created successfully")
