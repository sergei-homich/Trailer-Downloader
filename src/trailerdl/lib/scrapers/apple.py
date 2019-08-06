import os
import requests
import shutil
from unidecode import unidecode
from urllib.request import Request, urlopen
from trailerdl.lib.utilities.matching import Matching

class Apple:
    # Initialize
    def __init__(self, settings, lang, verbose, title, year, type, extras, downloaded):
        self.settings = settings
        self.lang = lang
        self.verbose = verbose
        self.title = title
        self.year = year
        self.type = type
        self.extras = list(extras)
        self.downloaded = downloaded
        self.extra_types = {
            self.lang['Trailers']: 'Trailer',
            self.lang['Teasers']: 'Teaser',
            self.lang['Scenes']: 'Clip',
            self.lang['Featurettes']: 'Featurette'
        }
        self.library_types = [
            self.lang['Movies']
        ]
        self.quality_labels = {
            u'sd': 480,
            u'hd720': 720,
            u'hd1080': 1080
        }
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
                self.query = unidecode(Matching.removeSpecialChars(self.title).replace(' ', '+'))
                results = requests.get(url='https://trailers.apple.com/trailers/home/scripts/quickfind.php?q='+self.query)
                results = results.json()
                for item in results['results']:
                    if Matching.year(self.year, item['releasedate']) and Matching.title(self.title, item['title']):
                        return self.videos('https://trailers.apple.com/'+item['location'])
        return []

    # Videos
    def videos(self, url):
        response = []
        results = requests.get(url=url+'/data/page.json')
        results = results.json()['clips']
        for item in results:
            if item['title'] not in self.downloaded:
                for key, value in self.types_needed.items():
                    if (item['title'].lower()).startswith(value.lower()):
                        last = None
                        for apple_size in item['versions']['enus']['sizes']:
                            try:
                                resolution = self.quality_labels[apple_size]
                            except:
                                resolution = 0
                            if int(resolution) >= int(self.settings['min_resolution']) and int(resolution) <= int(self.settings['max_resolution']):
                                if last is not None and resolution >= last:
                                    response = response[:-1]
                                last = resolution
                                response.append({
                                    'extra': key,
                                    'title': item['title'],
                                    'size': int(resolution),
                                    'url': item['versions']['enus']['sizes'][apple_size]['src'].replace('_%sp.mov' % resolution, '_h%sp.mov' % resolution).replace('http://', 'https://').replace('https://movietrailers.', 'https://trailers.')
                                })
                        break
        return response

    # Download
    def download(self, url, destination, filename):
        request = Request(url, None, {'User-Agent': 'Quick_time/10.5'})
        source = urlopen(request)
        with open(destination+'/'+filename+'.part', 'wb') as file:
            shutil.copyfileobj(source, file, 1024*1024)
            os.rename(destination+'/'+filename+'.part', destination+'/'+filename)
        return True