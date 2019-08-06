import os
from requests import exceptions
import shutil
import time
import tmdbsimple as tmdb
from unidecode import unidecode
import youtube_dl
from trailerdl.lib.utilities.logging import Logging
from trailerdl.lib.utilities.matching import Matching

class Tmdb:
    # Initialize
    def __init__(self, settings, lang, verbose, title, year, type, extras, downloaded):
        self.settings = settings
        self.lang = lang
        self.verbose = verbose
        self.title = title
        self.year = year
        self.type = type
        self.extras = extras
        self.downloaded = downloaded
        self.extra_types = {
            self.lang['Trailers']: 'Trailer',
            self.lang['Teasers']: 'Teaser',
            self.lang['Scenes']: 'Clip',
            self.lang['Featurettes']: 'Featurette',
            self.lang['Behind The Scenes']: 'Behind the Scenes',
            self.lang['Bloopers']: 'Blooper'
        }
        self.library_types = [
            self.lang['Movies'],
            self.lang['Series']
        ]
        self.types_needed = {}

    # Has Needed
    def hasNeeded(self):
        response = False
        for key, value in self.extra_types.items():
            if key in self.extras:
                self.types_needed[key]= value
                response = True
        return response

    # Search
    def search(self):
        if self.type in self.library_types:
            if self.hasNeeded():
                self.query = unidecode(self.title)
                retry = True
                while retry:
                    try:
                        tmdb.API_KEY = self.settings['tmdb_api_key']
                        search = tmdb.Search()
                        if self.type == self.lang['Movies']:
                            results = search.movie(query=self.query, language=self.settings['language']+'-'+self.settings['region'])
                        elif self.type == self.lang['Series']:
                            results = search.tv(query=self.query, language=self.settings['language']+'-'+self.settings['region'])
                        retry = False
                    except exceptions.HTTPError as e:
                        if e.response.status_code == 401:
                            Logging.invalidTmdbApiKey(True, self.settings, self.lang)
                        elif e.response.status_code == 429:
                            if "Retry-After" in e.response.headers:
                                time.sleep(int(e.response.headers["Retry-After"]))
                            else:
                                time.sleep(10)
                            retry = True
                        else:
                            retry = False
                for result in results['results']:
                    if self.type == self.lang['Movies'] and Matching.year(self.year, result['release_date']) and Matching.title(self.title, result['title']):
                        return self.videos(result['id'])
                    elif self.type == self.lang['Series'] and Matching.year(self.year, result['first_air_date']) and Matching.title(self.title, result['name']):
                        return self.videos(result['id'])

        return []

    # Videos
    def videos(self, id):
        retry = True
        while retry:
            try:
                tmdb.API_KEY = self.settings['tmdb_api_key']
                if self.type == self.lang['Movies']:
                    item = tmdb.Movies(id)
                elif self.type == self.lang['Series']:
                    item = tmdb.TV(id)
                results = item.videos(language=self.settings['language']+'-'+self.settings['region'])
                retry = False
            except exceptions.HTTPError as e:
                if e.response.status_code == 401:
                    Logging.invalidTmdbApiKey(True, self.settings, self.lang)
                elif e.response.status_code == 429:
                    if "Retry-After" in e.response.headers:
                        time.sleep(int(e.response.headers["Retry-After"]))
                    else:
                        time.sleep(10)
                    retry = True
                else:
                    retry = False
        response = []
        for item in results['results']:
            if item['name'] not in self.downloaded:
                for key, value in self.types_needed.items():
                    if value in item['type'] and int(item['size']) >= int(self.settings['min_resolution']) and int(item['size']) <= int(self.settings['max_resolution']):
                        response.append({
                            'extra': key,
                            'title': item['name'],
                            'size': item['size'],
                            'url': 'https://youtu.be/'+item['key']
                        })
        return response

    # Download
    def download(self, url, destination, filename):
        options = {
            'format': 'bestvideo[ext=mp4][height<='+str(self.settings['max_resolution'])+']+bestaudio[ext=m4a]',
            'default_search': 'ytsearch1:',
            'quiet': True,
            'no_warnings': True,
            'ignoreerrors': True,
            'noplaylist': True,
            'age_limit': 21,
            'prefer_ffmpeg': True,
            'restrictfilenames': True,
            'outtmpl': destination+'/'+filename,
            'logger': Logger()
        }
        try:
            with youtube_dl.YoutubeDL(options) as youtube:
                youtube.extract_info(url, download=True)
        except:
            return False
        return True

class Logger(object):
    def debug(self, msg):
        pass
    def warning(self, msg):
        pass
    def error(self, msg):
        pass