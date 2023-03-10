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

def detect_duplication(dbname):
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()
    query = "SELECT NAME, FILESIZE, MD5, COUNT(*) as count FROM PIC GROUP BY MD5 HAVING count > 1;"
    cursor.execute(query)
    result = cursor.fetchall()
 
    for row in result:
        print(row)
    conn.close()


def check_existence(file_path,cursor):
    filename=os.path.basename(file_path)
    file_path=os.path.dirname(file_path) 
    query = f"SELECT COUNT(*) FROM PIC WHERE FILEPATH = '{file_path}' AND NAME = '{filename}'"
    cursor.execute(query)
    count = cursor.fetchone()[0]
    return count > 0

def delete_duplication():
    print("Placeholder for deletion")