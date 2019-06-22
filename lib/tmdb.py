from __future__ import unicode_literals
from json import loads
from os import makedirs, path
from shutil import move
from sys import exit
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

# tmdbsimple
try:
    import tmdbsimple as tmdb
except:
    print('\033[91mERROR:\033[0m tmdbsimple is not installed.')
    exit()

# youtube_dl
try:
    import youtube_dl
except:
    print('\033[91mERROR:\033[0m youtube_dl is not installed.')
    exit()

# Download
def download(video, min_resolution, max_resolution, directory, filename):
    # Create downloads directory if it doesn't already exist
    if not path.exists('downloads'):
        makedirs('downloads')

    # Options
    options = {
        'format': 'bestvideo[ext=mp4][height<='+max_resolution+']+bestaudio[ext=m4a]',
        'default_search': 'ytsearch1:',
        'restrict_filenames': 'TRUE',
        'prefer_ffmpeg': 'TRUE',
        'quiet': 'TRUE',
        'no_warnings': 'TRUE',
        'ignore_errors': 'TRUE',
        'no_playlist': 'TRUE',
        'outtmpl': 'downloads/'+filename
    }

    # Download the file
    try:
        with youtube_dl.YoutubeDL(options) as youtube:
            youtube.extract_info(video, download=True)
    except:
        return False

    # Create destination directory if it doesn't already exist
    if not path.exists(directory):
        makedirs(directory)

    # Move downloaded trailer to directory
    move('downloads/'+filename, directory+'/'+filename)

    return True

# Get videos
def videos(id, lang, region, api_key):
    tmdb.API_KEY = api_key
    movie = tmdb.Movies(id)
    return movie.videos(language=lang+'-'+region)

# Search
def search(query, api_key):
    query = helpers.removeSpecialChars(query)
    tmdb.API_KEY = api_key
    search = tmdb.Search()
    return search.movie(query=query)