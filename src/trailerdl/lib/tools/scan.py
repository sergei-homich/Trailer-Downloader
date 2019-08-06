from multiprocessing import Manager, Queue
import time
from trailerdl.lib.utilities.logging import Logging
from trailerdl.lib.utilities.matching import Matching

class Scan:
    # Initialize
    def __init__(self, settings, lang, verbose):
        self.settings = settings
        self.lang = lang
        self.verbose = verbose
        self.queue = Manager().Queue()
        self.response = Manager().list()
        self.missing = 0

    # Add
    def add(self, title, year, destination, type, extras):
        item = {
            'title': title,
            'year': year,
            'destination': destination,
            'extras': extras,
            'type': type
        }
        self.queue.put(item)

    # Worker
    def worker(self):
        while not self.queue.empty():
            item = self.queue.get()

            missing = 0
            mapping = {}
            needed_extras = []
            for extra_type in item['extras']:
                directory = item['destination']+'/'+self.settings['subfolders'][extra_type]
                downloaded = Matching.find(self.settings['formatting'][extra_type], extra_type, item['title'], item['year'], directory)
                needed = int(self.settings['limits'][extra_type]) - len(downloaded)
                if needed > 0:
                    needed_extras.append(extra_type)
                    mapping[extra_type] = {
                        'destination': directory,
                        'downloaded': downloaded,
                        'needed': needed if needed > 0 else 0
                    }
                    missing += needed if needed > 0 else 0
            self.missing += missing

            response = {
                'title': item['title'],
                'year': item['year'],
                'destination': item['destination'],
                'type': item['type'],
                'extras': item['extras'],
                'mapping': mapping,
                'missing': missing,
                'needed_extras': needed_extras
            }

            Logging.scanningItem(self.verbose, self.settings, self.lang, response)

            if missing > 0:
                self.response.append(response)

    # Run
    def run(self):
        if not self.queue.empty():
            Logging.scanning(self.verbose, self.settings, self.lang)
            start = time.time()

            self.worker()

            end = time.time()
            Logging.time(self.verbose, self.settings, self.lang, end-start)
            Logging.missing(self.verbose, self.settings, self.lang, self.missing)

        return self.response