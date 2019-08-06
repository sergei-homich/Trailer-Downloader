from multiprocessing import cpu_count, Manager, Queue
from multiprocessing.pool import ThreadPool
import os
import threading
import time
from trailerdl.lib.utilities.database import Database
from trailerdl.lib.utilities.logging import Logging

class Download:
    # Initialize
    def __init__(self, settings, lang, verbose):
        self.settings = settings
        self.lang = lang
        self.verbose = verbose
        self.db = Database()
        self.queue = Manager().Queue()
        self.max_processes = cpu_count() * 4
        self.response = []

    # Add
    def add(self, title, year, type, extra, original_name, scraper, source, url, destination, filename):
        item = {
            'title': title,
            'year': year,
            'type': type,
            'extra': extra,
            'original_name': original_name,
            'scraper': scraper,
            'source': source,
            'url': url,
            'destination': destination,
            'filename': filename
        }
        self.queue.put(item)

    # Worker
    def worker(self, item):
        try:
            if not os.path.exists(item['destination']):
                os.makedirs(item['destination'])
        except:
            pass

        Logging.downloadingItem(self.verbose, self.settings, self.lang, item)

        download = item['source'].download(item['url'], item['destination'], item['filename'])

        if download:
            self.db.store(item['title'], item['year'], item['type'], item['extra'], item['original_name'], item['filename'], item['destination'], item['scraper'])
            self.response.append(item)

    # Run
    def run(self):
        if not self.queue.empty():
            Logging.downloading(self.verbose, self.settings, self.lang)
            start = time.time()

            pool = ThreadPool(self.queue.qsize() if self.queue.qsize() < self.max_processes else self.max_processes)
            while not self.queue.empty():
                item = self.queue.get()
                pool.apply_async(self.worker, args=(item,))
            pool.close()
            pool.join()

            end = time.time()
            Logging.time(self.verbose, self.settings, self.lang, end-start)
            Logging.downloaded(self.verbose, self.settings, self.lang, len(self.response))