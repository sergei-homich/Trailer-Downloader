from __future__ import unicode_literals
from json import loads
from lib import helpers
from os import makedirs, path
from shutil import move
from sys import exit

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
        'restrictfilenames': 'TRUE',
        'prefer_ffmpeg': 'TRUE',
        'quiet': 'TRUE',
        'no_warnings': 'TRUE',
        'ignoreerrors': 'TRUE',
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
    try:
        tmdb.API_KEY = api_key
        movie = tmdb.Movies(id)
        return movie.videos(language=lang+'-'+region)
    except:
        print('\033[91mERROR:\033[0m Failed to connect to TMDB. Check your api key.')
        exit()

# Search
def search(query, api_key):
    query = helpers.removeSpecialChars(query)
    try:
        tmdb.API_KEY = api_key
        search = tmdb.Search()
        return search.movie(query=query)
    except:
        print('\033[91mERROR:\033[0m Failed to connect to TMDB. Check your api key.')
        exit()