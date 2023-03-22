import imageUtils
import sqlConnector



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
    for file_path in imageUtils.findFiles(base):
        count += 1
        if not sqlConnector.check_existence(file_path,cursor):
            print("FILE NOT STORED IN DATABASE")
            file_name,dir_path,file_size,file_md5 = imageUtils.process_file(file_path)
            similarity = str(12345)
            cursor.execute("INSERT INTO " + table + "(NAME,FILEPATH,FILESIZE,MD5,SIMILARITY) VALUES (?,?,?,?,?)",(file_name,dir_path,file_size,file_md5,similarity))
            conn.commit()
    conn.close()
    print("Database %s initialized, %d files inserted." % (dbname,count))

def removeDuplicationByMD5(dbname):
    result = sqlConnector.detectDuplicationByMD5(dbname)
    sqlConnector.deleteDuplicationByMD5(result,dbname)


