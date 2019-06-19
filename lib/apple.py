from __future__ import unicode_literals
from json import loads
from os import makedirs, path
from shutil import copyfileobj, move
import helpers

# Python 3.0 and later
try:
    from configparser import ConfigParser
    from urllib.request import *
    from urllib.error import *

# Python 2.7
except ImportError:
    from ConfigParser import ConfigParser
    from urllib2 import *

# Load json from url
def loadJson(url):
    response = urlopen(url).read().decode('utf-8')
    return loads(response)

# Get file url
def getUrl(page_url, resolution):
    urls = []
    film_data = loadJson(page_url + '/data/page.json')
    title = film_data['page']['movie_title']
    apple_size = mapResolution(resolution)

    for clip in film_data['clips']:
        video_type = clip['title']
        if apple_size in clip['versions']['enus']['sizes']:
            file_info = clip['versions']['enus']['sizes'][apple_size]
            file_url = file_info['src'].replace("_%sp.mov" % resolution, "_h%sp.mov" % resolution)
            video_type = video_type.lower()
            if (video_type.startswith('trailer')):
                urls.append(file_url)

    if len(urls) >= 1:
        return urls[len(urls)-1]
    else:
        return False

# Map resolution
def mapResolution(resolution):
    mapping = {'480': u'sd', '720': u'hd720', '1080': u'hd1080'}
    if resolution not in mapping:
        raise ValueError("Invalid resolution. Valid values: %s" % ', '.join(mapping.keys()))
    return mapping[resolution]

# Download
def download(page_url, resolution, directory, filename):
    trailer_url = getUrl(page_url, resolution)

    # Make sure a url was found
    if trailer_url.strip():
        headers = {'User-Agent': 'Quick_time/7.6.2'}
        request = Request(trailer_url, None, headers)
        chunk_size = 1024 * 1024

        # Create downloads directory if it doesn't already exist
        if not path.exists('downloads'):
            makedirs('downloads')

        # Download the file
        try:
            server_file = urlopen(request)
        except HTTPError as error:
            return False
        except URLError as error:
            return False
        try:
            with open('downloads/'+filename, 'wb') as local_file:
                file = copyfileobj(server_file, local_file, chunk_size)
        except socket.error as error:
            return False

        # Create destination directory if it doesn't already exist
        if not path.exists(directory):
            makedirs(directory)

        # Move downloaded trailer to directory
        move('downloads/'+filename, directory+'/'+filename)

        return True

# Search
def search(query):
    query = helpers.removeSpecialChars(query)
    query = helpers.removeAccents(query)
    query = query.replace(' ', '+')
    url = 'https://trailers.apple.com/trailers/home/scripts/quickfind.php?q='+query
    return loadJson(url)