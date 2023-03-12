import os
import sqlite3
import os
import hashlib
import sqlConnector
import argparse
import dbInitialization

def main():
    print("Starting service")
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input_folder',type=str,default= 'c:/Users/Remi/Desktop/原神',help="Folder to test")
    args = parser.parse_args()
    base = args.input_folder
    dbname = os.path.basename(base)+".db"
    table = "PIC"
    dbInitialization.initialize(dbname,base,table)

if __name__ == '__main__':
    main()