import os
import sqlite3
import os
import hashlib
import sqlConnector
import argparse
import dbInitialization
import FSobserver

def main():
    print("Starting service")
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input_folder',type=str,default= 'c:/Users/Remi/Desktop/原神',help="Folder to test")
    parser.add_argument('-c','--initial_database',type=bool,default= False,help="Initialize the database or not")
    parser.add_argument('-a','--add_table',type=bool ,default = False,help="Add a new table")
    parser.add_argument('-n ',type=str,help="Table name")
    args = parser.parse_args()
    
    ifInitial = args.initial_database
    path = args.input_folder
    dbname = os.path.basename(path)+".db"
    if (ifInitial):
        table = "PIC"
        dbInitialization.initialize(dbname,path,table)
    dbInitialization.removeDuplicationByMD5(dbname)
    FSobserver.startObserver(path)

if __name__ == '__main__':
    main()