import sys
import time 
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
import reformatter 

class renamer(LoggingEventHandler):
    def on_created(self,event):
        super(LoggingEventHandler,self).on_created(event)
        if event.is_directory:
            what = 'directory'
        else:
            what = 'file'
        logging.info("Created %s: %s" % (what, event.src_path))
        extension = event.src_path.split('.')
        if extension[-1] == "jpg" or extension[-1] == "png":
            reformatter.reformat(event.src_path)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = '.'
    
    event_handler = renamer()

    observer = Observer()

    observer.schedule(event_handler,path,recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

