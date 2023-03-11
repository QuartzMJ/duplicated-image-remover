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


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input_folder',type=str,default= 'c:/Users/Remi/Desktop/原神',help="Folder to test")
    args = parser.parse_args()
    base = args.input_folder
    dbname = os.path.basename(base)+".db"
   
    conn = sqlConnector.open_connection(dbname)
    cursor = conn.cursor()
    table = "PIC";
    query = "SELECT name FROM sqlite_master WHERE type='table' AND name='PIC'"
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
    # The table does not exist
        sqlConnector.create_table(conn,table)


    if not sqlConnector.checkColumnExistence("SIMILARITY",cursor):
        query = "ALTER TABLE PIC ADD COLUMN SIMILARITY TEXT"
        cursor.execute(query)
        print("Adding column SIMILARITY")
        conn.commit()

    
    for file_path in findFiles(base):
        if not sqlConnector.check_existence(file_path,cursor):
            print("FILE NOT STORED IN DATABASE")
            file_name,dir_path,file_size,file_md5 = process_file(file_path)
            cursor.execute("INSERT INTO PIC (NAME,FILEPATH,FILESIZE,MD5) VALUES (?,?,?,?)",(file_name,dir_path,file_size,file_md5))
            conn.commit()
        elif not sqlConnector.checkSimilaritySet(file_path,cursor):
            print("SIMILARITY NOT SET")
            similarity = str(12345)
            file_name = os.path.basename(file_path)
            dir_path = os.path.dirname(file_path)
            paras = (similarity,file_name,dir_path)
            cursor.execute("UPDATE PIC SET SIMILARITY = ? WHERE NAME = ? AND FILEPATH = ?",paras)
            conn.commit()
    sqlConnector.detect_duplication(dbname)
    conn.close()

if __name__ == '__main__':
    main()