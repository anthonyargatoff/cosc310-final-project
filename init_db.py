# Description: This script is used to create the database schema.
import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()
connection.commit()
connection.close()