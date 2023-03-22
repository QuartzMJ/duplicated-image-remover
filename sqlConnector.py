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
     MD5            TEXT    NOT NULL,
     SIMILARITY     TEXT    NOT NULL
     );'''.format(table))
     print("Database created!")
     # execute queries on the new database

def detectDuplicationByMD5(dbname):
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()
    query = "SELECT ID, FILEPATH, NAME, FILESIZE, MD5, COUNT(*) as count FROM PIC GROUP BY MD5 HAVING count > 1;"
    cursor.execute(query)
    result = cursor.fetchall()
 
    count = 1
    for row in result:
        print(row)
        print("Duplication counts: " + str(count))
        count += 1
    conn.close()
    return result;
    


def check_existence(file_path,cursor):
    filename=os.path.basename(file_path)
    file_path=os.path.dirname(file_path) 
    query = "SELECT COUNT(*) FROM PIC WHERE FILEPATH = ? AND NAME = ?"
    paras = (file_path,filename)
    cursor.execute(query,paras)
    count = cursor.fetchone()[0]
    return count > 0

def checkExistenceByMD5(md5,cursor):
    query = "SELECT COUNT(*) FROM PIC WHRER MD5 = ?"
    paras = (md5,)
    cursor.execute(query,paras)
    count = cursor.fetchone()[0]
    return count > 0

def checkSimilaritySet(file_path,cursor):
    similarity = str(12345)
    filename=os.path.basename(file_path)
    query = "SELECT COUNT(*) FROM PIC WHERE SIMILARITY= ? AND NAME = ?"
    paras = (similarity,filename)
    cursor.execute(query,paras)
    count = cursor.fetchone()[0]
    return count > 0

def checkColumnExistence(para,cursor):
    query = "PRAGMA table_info(PIC)"
    cursor.execute(query)
    print("testing")
    columns = [column[1] for column in cursor.fetchall()]
    if str(para) not in columns:
       print("Not exists")
       return False
    else:
        print("Exists")
        return True


def deleteDuplicationByMD5(result,dbname):
    
    conn = open_connection(dbname)
    cursor = conn.cursor()
    for file in result:
        filePath = file[1] + '\\' + file[2]
        print(filePath)
        if os.path.exists(filePath):
            os.remove(filePath)

        id = int(file[0])
        cursor.execute("DELETE FROM PIC WHERE ID = ?", (id,))
        print("deleting...")
        conn.commit()
    conn.close()
    