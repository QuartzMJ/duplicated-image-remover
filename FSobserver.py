import sys
import time 
import os
import argparse
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
import reformatter 

class Renamer(LoggingEventHandler):

    def __init__(self,path_root):
        super(Renamer, self).__init__
        self.path_root = path_root

    def on_created(self,event):
        super(LoggingEventHandler,self).on_created(event)
        if event.is_directory:
            what = 'directory'
        else:
            what = 'file'
        logging.info("Created %s: %s" % (what, event.src_path))
        extension = event.src_path.split('.')
        if extension[-1] == "jpg" or extension[-1] == "png":
            reformatter.reformat(event.src_path,self.path_root)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', type=str,help="Path to observe")
    args = parser.parse_args()
    path = args.path
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

