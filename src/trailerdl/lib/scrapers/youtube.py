from bs4 import BeautifulSoup, SoupStrainer
import json
import os
import requests
import shutil
from unidecode import unidecode
from urllib.request import pathname2url
import youtube_dl
from trailerdl.lib.utilities.matching import Matching

class Youtube:
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
        }
        self.library_types = [
            self.lang['Movies']
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
                self.query = pathname2url(unidecode(self.title)+' movie')
                response = requests.get('https://www.youtube.com/results?search_query='+self.query)
                html = response.content
                where = SoupStrainer(id='results')
                soup = BeautifulSoup(html, 'html.parser', parse_only=where)
                results = soup.findAll('div', attrs={'class':'yt-lockup yt-lockup-tile yt-lockup-movie-vertical-poster vve-check clearfix yt-uix-tile'})
                try:
                    for result in results:
                        id = result['data-context-item-id']
                        title = result.findAll('a', attrs={'class': 'yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 yt-uix-sessionlink spf-link'})[0]['title'].replace(str(self.year), '')
                        info = result.findAll('div', attrs={'class': 'yt-lockup-meta'})[0].find('li').contents[0]
                        if Matching.year(self.year, info) and Matching.title(unidecode(self.title), unidecode(title)):
                            return self.videos('https://www.youtube.com/watch?v='+id, title)
                except:
                    return []
        return []

    # Videos
    def videos(self, url, title):
        response = []
        results = requests.get(url)
        where = SoupStrainer('script')
        soup = BeautifulSoup(results.content, 'html.parser', parse_only=where)
        for script in soup.find_all('script'):
            if 'var ytplayer = ytplayer' in script.text:
                url_start_id = script.text.find('trailerVideoId')+19
                url = "https://youtu.be/" + script.text[url_start_id:url_start_id+11]
                results = requests.get(url)
                if results.status_code == 200:
                    response.append({
                        'extra': self.lang['Trailers'],
                        'title': title,
                        'size': 0,
                        'url': url
                    })
                break
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