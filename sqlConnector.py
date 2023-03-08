import os
import sqlite3

def open_connection(dbname):
        # check if database file exists
    if os.path.isfile(dbname):
        conn = sqlite3.connect(dbname)
        # execute queries on the database
    else:
        # create new database and connect to it
        conn = sqlite3.connect(dbname) 
    return conn;

def create_table(conn,table):
     cursor = conn.cursor()
     cursor.execute('''CREATE TABLE IF NOT EXISTS {}( 
     ID INTEGER PRIMARY KEY     AUTOINCREMENT,
     NAME           TEXT    NOT NULL,
     FILEPATH       TEXT    NOT NULL,
     FILESIZE       INT     NOT NULL,
     MD5            TEXT    NOT NULL
     );'''.format(table))
     print("Database created!")
     # execute queries on the new database



