import os
import hashlib
import sqlConnector
import argparse

def findFiles(base):
    for subdir, dirs, files in os.walk(base):
        for file in files:
            file_path = os.path.join(subdir, file)
            yield file_path

def calculate_md5(filename):
    with open(filename, "rb") as f:
        # Read the file in chunks to avoid loading large files into memory all at once
        md5 = hashlib.md5()
        while chunk := f.read(8192):
            md5.update(chunk)
    return md5.hexdigest()

def calculate_size(file_path):
    return os.path.getsize(file_path)

def process_file(file_path):
    file_md5 = calculate_md5(file_path)
    file_size = calculate_size(file_path)
    file_name = os.path.basename(file_path)
    dir_path = os.path.dirname(file_path)
    return file_name,dir_path,file_size,file_md5


def initialize(dbname,base,table):
   
    conn = sqlConnector.open_connection(dbname)
    cursor = conn.cursor()
    query = "SELECT name FROM sqlite_master WHERE type='table' AND name= ? "
    cursor.execute(query,(table,))
    result = cursor.fetchone()
    if result is None:
    # The table does not exist
        sqlConnector.create_table(conn,table)

    count = 0
    for file_path in findFiles(base):
        count += 1
        if not sqlConnector.check_existence(file_path,cursor):
            print("FILE NOT STORED IN DATABASE")
            file_name,dir_path,file_size,file_md5 = process_file(file_path)
            similarity = str(12345)
            cursor.execute("INSERT INTO " + table + "(NAME,FILEPATH,FILESIZE,MD5,SIMILARITY) VALUES (?,?,?,?,?)",(file_name,dir_path,file_size,file_md5,similarity))
            conn.commit()
    conn.close()
    print("Database %s initialized, %d files inserted." % (dbname,count))

