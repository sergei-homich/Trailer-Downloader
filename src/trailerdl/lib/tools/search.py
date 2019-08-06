from multiprocessing import cpu_count, Manager, Queue
from multiprocessing.pool import ThreadPool
import time
from trailerdl.lib.scrapers.apple import Apple
from trailerdl.lib.scrapers.youtube import Youtube
from trailerdl.lib.scrapers.tmdb import Tmdb
from trailerdl.lib.utilities.database import Database
from trailerdl.lib.utilities.logging import Logging
from trailerdl.lib.utilities.matching import Matching

class Search:
    # Initialize
    def __init__(self, settings, lang, verbose):
        self.settings = settings
        self.lang = lang
        self.verbose = verbose
        self.queue = Manager().Queue()
        self.max_processes = cpu_count() * 4
        self.response = Manager().list()
        self.db = Database()

    # Add
    def add(self, title, year, destination, type, extras, mapping, missing, needed_extras):
        item = {
            'title': title,
            'year': year,
            'destination': destination,
            'extras': extras,
            'type': type,
            'mapping': mapping,
            'missing': missing,
            'needed_extras': needed_extras
        }
        self.queue.put(item)

    # Worker
    def worker(self, item):
        Logging.searchingItem(self.verbose, self.settings, self.lang, item)

        downloaded = []
        for key, value in item['mapping'].items():
            downloaded.append(value['downloaded'])

        for scraper in self.settings['scrapers']:
            if item['missing'] > 0:
                if scraper == 'apple':
                    source = Apple(self.settings, self.lang, self.verbose, item['title'], item['year'], item['type'], item['needed_extras'], downloaded)
                elif scraper == 'tmdb':
                    source = Tmdb(self.settings, self.lang, self.verbose, item['title'], item['year'], item['type'], item['needed_extras'], downloaded)
                elif scraper == 'youtube':
                    source = Youtube(self.settings, self.lang, self.verbose, item['title'], item['year'], item['type'], item['needed_extras'], downloaded)
                else:
                    Logging.scraperNotFound(True, self.settings, self.lang, scraper)
                    break

                search = source.search()

                if len(search) > 0:
                    for result in search:
                        if item['mapping'][result['extra']]['needed'] > 0:
                            if not self.db.search(item['title'], item['year'], item['type'], result['extra'], result['title'], item['mapping'][result['extra']]['destination'], scraper):
                                filename = Matching.filename(self.settings['formatting'], result['extra'], item['title'], item['year'], item['mapping'][result['extra']]['downloaded'])
                                self.response.append({
                                    'title': item['title'],
                                    'year': item['year'],
                                    'type': item['type'],
                                    'extra': result['extra'],
                                    'original_name': result['title'],
                                    'scraper': scraper,
                                    'source': source,
                                    'url': result['url'],
                                    'destination': item['mapping'][result['extra']]['destination'],
                                    'filename': filename
                                })

                                item['mapping'][result['extra']]['downloaded'].append(filename)
                                item['mapping'][result['extra']]['needed'] -= 1
                                item['missing'] -= 1

                                if item['mapping'][result['extra']]['needed'] < 1:
                                    item['needed_extras'].remove(result['extra'])

                                if item['missing'] < 1:
                                    break

            else:
                break

    # Run
    def run(self):
        if not self.queue.empty():
            Logging.searching(self.verbose, self.settings, self.lang)
            start = time.time()

            pool = ThreadPool(self.queue.qsize() if self.queue.qsize() < self.max_processes else self.max_processes)
            while not self.queue.empty():
                item = self.queue.get()
                pool.apply_async(self.worker, args=(item,))
            pool.close()
            pool.join()

            end = time.time()
            Logging.time(self.verbose, self.settings, self.lang, end-start)
            Logging.found(self.verbose, self.settings, self.lang, len(self.response))

        return self.response