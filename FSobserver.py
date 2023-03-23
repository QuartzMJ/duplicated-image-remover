import sys
import time 
import os
import sqlite3
import logging
import imageUtils
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
import reformatter 
import sqlConnector

class Renamer(LoggingEventHandler):

    def __init__(self,path_root):
        super(Renamer, self).__init__()
        self.path_root = path_root
        self.dbname  = os.path.basename(self.path_root)+".db"
        self.conn = sqlConnector.connect(self.dbname)
        self.cursor = self.conn.cursor()

    def on_created(self,event):
        super(LoggingEventHandler,self).on_created(event)
        time.sleep(4)
        extension = event.src_path.split('.')
        print("inside of the observer")
        print(extension[-1])
        if extension[-1] == "jpg" or extension[-1] == "png" or extension[-1] == "jpeg":
            print("running")
            filePath = reformatter.reformat(event.src_path,self.path_root)
            file_name,dir_path,file_size,file_md5 = entries = imageUtils.processFile(filePath)    
            similarity = str(12345)
            print (file_md5)
            if not sqlConnector.checkExistenceByMD5(file_md5):
                self.cursor.execute("INSERT INTO " + "PIC" + "(NAME,FILEPATH,FILESIZE,MD5,SIMILARITY) VALUES (?,?,?,?,?)",(file_name,dir_path,file_size,file_md5,similarity))
                print("Inserting into database",entries)
                self.conn.commit()
            else:
                target = dir_path + '\\' + file_name
                os.remove(target)
                print(target + " deleted")
            


def startObserver(path):
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path_ending = os.path.basename(path)
    event_handler = Renamer(path_ending)
    observer = Observer()
    observer.schedule(event_handler,path,recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

