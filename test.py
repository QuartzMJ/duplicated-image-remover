import os
import hashlib
import sqlConnector
import reformatter 

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
    file_name = reformatter.reformat(file_path)
    dir_path = os.path.dirname(file_path)
    #print("Dir path: %s" %dir_name, "File name: %s" % file_name,"  File size: %s" % (file_size), "File MD5: %s" % (file_md5))
    return file_name,dir_path,file_size,file_md5


def main():
    base = 'C:/Users/Remi/Desktop/原神'
    count = 1
    conn = sqlConnector.open_connection("genshin.db")
    cursor = conn.cursor()
    table = "PIC";
    sqlConnector.create_table(conn,table)
    for file_path in findFiles(base):
        file_name,dir_path,file_size,file_md5 = process_file(file_path)
        #cursor.execute("INSERT INTO PIC (NAME,FILEPATH,FILESIZE,MD5) VALUES (?,?,?,?)",(file_name,dir_path,file_size,file_md5))
        #conn.commit()
        print(count)
        count += 1
if __name__ == '__main__':
    main()