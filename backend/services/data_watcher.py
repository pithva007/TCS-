import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading
from .data_ingester import ingest_all, DEFAULT_DATA_DIR

class DataChangeHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_modified = time.time()
        self.debounce_seconds = 1.0
        self.timer = None

    def on_modified(self, event):
        if event.src_path.endswith(".json"):
            self.trigger_ingest()

    def on_created(self, event):
        if event.src_path.endswith(".json"):
            self.trigger_ingest()

    def on_deleted(self, event):
        if event.src_path.endswith(".json"):
            self.trigger_ingest()
            
    def trigger_ingest(self):
        if self.timer is not None:
            self.timer.cancel()
        self.timer = threading.Timer(self.debounce_seconds, ingest_all)
        self.timer.start()

observer = None

def start_watcher():
    global observer
    data_dir = os.getenv("DATA_DIR", str(DEFAULT_DATA_DIR))
    if not os.path.exists(data_dir):
        os.makedirs(data_dir, exist_ok=True)
    event_handler = DataChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, data_dir, recursive=False)
    observer.start()

def stop_watcher():
    global observer
    if observer:
        observer.stop()
        observer.join()
