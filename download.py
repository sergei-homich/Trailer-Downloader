#!/usr/bin/env python3

# Disable bytecode
import sys
sys.dont_write_bytecode = True

# Modules
from __init__ import NAME, VERSION, DESCRIPTION
from argparse import ArgumentParser
from configparser import *
from urllib.request import *
from urllib.error import *
import html.parser
import json
import os
import shutil
import socket
import time
import unicodedata

# requests
try:
    from requests import exceptions
except:
    print('\033[91mERROR:\033[0m requests is not installed.')
    sys.exit()

# tmdbsimple
try:
    import tmdbsimple as tmdb
except:
    print('\033[91mERROR:\033[0m tmdbsimple is not installed.')
    sys.exit()

# youtube_dl
try:
    import youtube_dl
except:
    print('\033[91mERROR:\033[0m youtube_dl is not installed.')
    sys.exit()

# unidecode
try:
    from unidecode import unidecode
except:
    print('\033[91mERROR:\033[0m unidecode is not installed.')
    sys.exit()

# Arguments
def getArguments():
    parser = ArgumentParser(description=NAME+': '+DESCRIPTION)
    parser.add_argument('-v', '--version', action='version', version=NAME+' '+VERSION, help='show the version number and exit')
    parser.add_argument('-d', '--directory', dest='directory', help='full path of directory to copy downloaded trailer', metavar='DIRECTORY')
    parser.add_argument('-t', '--title', dest='title', help='title of movie', metavar='TITLE')
    parser.add_argument('-y', '--year', dest='year', help='release year of movie', metavar='YEAR')
    args = parser.parse_args()
    return {
        'directory': str(args.directory) if args.directory != None else args.directory,
        'title': str(args.title) if args.title != None else args.title,
        'year': str(args.year) if args.year != None else args.year
    }

# Settings
def getSettings():
    if not os.path.exists(os.path.split(os.path.abspath(__file__))[0]+'/settings.ini'):
        print('\033[91mERROR:\033[0m Could not find the settings.ini file. Create one from the settings.ini.example file to get started.')
        sys.exit()
    try:
        config = RawConfigParser()
        config.read(os.path.split(os.path.abspath(__file__))[0]+'/settings.ini')
    except MissingSectionHeaderError:
        print('\033[91mERROR:\033[0m DEFAULT section could not be found in settings.ini file.')
        sys.exit()
    response = {}
    for key in ['tmdb_api_key', 'region', 'lang', 'resolution', 'max_resolution', 'min_resolution', 'subfolder', 'custom_formatting']:
        response[key]= config.get('DEFAULT', key)
    return response

# Format
def format():
    return 'windows-1252' if os.name == 'nt' else 'utf-8'

# Remove special characters
def removeSpecialChars(query):
    return ''.join([ch for ch in query if ch.isalnum() or ch.isspace()])

# Remove accent characters
def removeAccents(query):
    return unidecode(query)

# Unescape characters
def unescape(query):
    return html.unescape(query)

# Match titles
def matchTitle(title):
    return unicodedata.normalize('NFKD', removeSpecialChars(title).replace('/', '').replace('\\', '').replace('-', '').replace(':', '').replace('*', '').replace('?', '').replace(''', '').replace(''', '').replace('<', '').replace('>', '').replace('|', '').replace('.', '').replace('+', '').replace(' ', '').lower()).encode('ASCII', 'ignore')

# Load json from url
def loadJson(url):
    response = urlopen(url)
    str_response = response.read().decode('utf-8')
    return json.loads(str_response)

# Get file urls
def getUrls(page_url, res):
    urls = []
    film_data = loadJson(page_url + '/data/page.json')
    title = film_data['page']['movie_title']
    apple_size = mapRes(res)

    for clip in film_data['clips']:
        video_type = clip['title']
        if apple_size in clip['versions']['enus']['sizes']:
            file_info = clip['versions']['enus']['sizes'][apple_size]
            file_url = convertUrl(file_info['src'], res)
            video_type = video_type.lower()
            if (video_type.startswith('trailer')):
                url_info = {
                    'res': res,
                    'title': title,
                    'type': video_type,
                    'url': file_url,
                }
                urls.append(url_info)

    final = []
    length = len(urls)

    if length > 1:
        final.append(urls[length-1])
        return final
    else:
        return urls

# Map resolution
def mapRes(res):
    res_mapping = {'480': u'sd', '720': u'hd720', '1080': u'hd1080'}
    if res not in res_mapping:
        res_string = ', '.join(res_mapping.keys())
        raise ValueError('Invalid resolution. Valid values: %s' % res_string)
    return res_mapping[res]

# Convert source url to file url
def convertUrl(src_url, res):
    src_ending = '_%sp.mov' % res
    file_ending = '_h%sp.mov' % res
    return src_url.replace(src_ending, file_ending)

# Download the file
def downloadFile(url, directory, filename):
    data = None
    headers = {'User-Agent': 'Quick_time/7.6.2'}
    req = Request(url, data, headers)
    chunk_size = 1024 * 1024

    try:
        server_file_handle = urlopen(req)
    except HTTPError as error:
        return
    except URLError as error:
        return
    try:
        if not os.path.exists(os.path.split(os.path.abspath(__file__))[0]+'/downloads'):
            os.makedirs(os.path.split(os.path.abspath(__file__))[0]+'/downloads')
        with open(os.path.split(os.path.abspath(__file__))[0]+'/downloads/'+filename, 'wb') as local_file_handle:
            shutil.copyfileobj(server_file_handle, local_file_handle, chunk_size)
    except socket.error as error:
        return

    # Move downloaded trailer to directory
    if not os.path.exists(directory):
        os.makedirs(directory)
    shutil.move(os.path.split(os.path.abspath(__file__))[0]+'/downloads/'+filename, directory+'/'+filename)

# Download from Apple
def appleDownload(page_url, res, directory, filename):
    trailer_urls = getUrls(page_url, res)
    for trailer_url in trailer_urls:
        downloadFile(trailer_url['url'], directory, filename)
        return filename

# Search Apple
def searchApple(query):
    query = removeSpecialChars(query)
    query = removeAccents(query)
    query = query.replace(' ', '+')
    search_url = 'https://trailers.apple.com/trailers/home/scripts/quickfind.php?q='+query
    return loadJson(search_url)

# Search TMDB
def searchTMDB(query, api_key, lang):
    query = removeSpecialChars(query)
    tmdb.API_KEY = api_key
    while True:
        try:
            search = tmdb.Search()
            return search.movie(query=query, language=lang)
        except exceptions.HTTPError as e:
            exceptionsTMDB(e)

# Search TMDB for videos
def videosTMDB(id, lang, region, api_key):
    tmdb.API_KEY = api_key
    while True:
        try:
            movie = tmdb.Movies(id)
            return movie.videos(language=lang+'-'+region)
        except exceptions.HTTPError as e:
            exceptionsTMDB(e)

# Handle TMDB exceptions
def exceptionsTMDB(e):
    if e.response.status_code == 401:
        print('\033[91mERROR:\033[0m Failed to connect to TMDB. Check your api key ('+tmdb.API_KEY+').')
        sys.exit()
    elif e.response.status_code == 429:
        if 'Retry-After' in e.response.headers:
            wait = int(e.response.headers['Retry-After'])
        else:
            wait = 10
        print('\033[93mWARNING:\033[0m Exceeded TMDB api request limit. Waiting for '+str(wait)+' seconds...')
        time.sleep(wait)
    else:
        print('\033[91mERROR:\033[0m Other TMDB Error ('+str(e)+').')
        sys.exit()

# Download file from YouTube
def youtubeDownload(video, min_resolution, max_resolution, directory, filename):
    # YouTube options
    options = {
        'format': 'bestvideo[ext=mp4][height<='+max_resolution+']+bestaudio[ext=m4a]',
        'default_search': 'ytsearch1:',
        'restrict_filenames': 'TRUE',
        'prefer_ffmpeg': 'TRUE',
        # 'quiet': 'TRUE',
        'no_warnings': 'TRUE',
        'ignore_errors': 'TRUE',
        'no_playlist': 'TRUE',
        'outtmpl': os.path.split(os.path.abspath(__file__))[0]+'/downloads/'+filename
    }

    try:
        # Download
        if not os.path.exists(os.path.split(os.path.abspath(__file__))[0]+'/downloads'):
            os.makedirs(os.path.split(os.path.abspath(__file__))[0]+'/downloads')
        with youtube_dl.YoutubeDL(options) as youtube:
            file = youtube.extract_info(video, download=True)
        # Move downloaded trailer to directory
        if not os.path.exists(directory):
            os.makedirs(directory)
        shutil.move(os.path.split(os.path.abspath(__file__))[0]+'/downloads/'+filename, directory+'/'+filename)
        return file
    except:
        return False

# Main
def main():
    # Arguments
    arguments = getArguments()

    # Settings
    settings = getSettings()

    # Make sure a movie directory, title, and year was passed
    if arguments['directory'] != None and arguments['title'] != None and arguments['year'] != None:

        # If subfolder setting is set, add it to the directory
        if settings['subfolder'].strip():
            arguments['directory'] = arguments['directory']+'/'+settings['subfolder']

        # Use custom formatting for filenames or use default if none is set
        if settings['custom_formatting'].strip():
            filename = settings['custom_formatting'].replace('%title%', arguments['title'].replace(':', '-')).replace('%year%', arguments['year'])+'.mp4'
        else:
            filename = arguments['title'].replace(':', '-')+' ('+arguments['year']+')-trailer.mp4'

        # Download status
        downloaded = False

        # Make sure trailer file doesn't already exist in the directory
        if os.path.exists(arguments['directory']):
            for name in os.listdir(arguments['directory']):
                if filename[:-4] in name:
                    downloaded = True

        # Search
        if not downloaded:
            # Search Apple for trailer (if english requested)
            if settings['lang'].lower() == "en":
                search = searchApple(arguments['title'])

                # Iterate over search results
                for result in search['results']:

                    # Filter by year and title
                    if 'releasedate' in result and 'title' in result:
                        if arguments['year'].lower() in result['releasedate'].lower() and matchTitle(arguments['title']) == matchTitle(unescape(result['title'])):

                            file = appleDownload('https://trailers.apple.com/'+result['location'], settings['resolution'], arguments['directory'], filename)

                            # Update downloaded status
                            if file:
                                downloaded = True
                                break

            # Search TMDB/YouTube for trailer
            if not downloaded:
                search = searchTMDB(arguments['title'], settings['tmdb_api_key'], settings['lang'])

                # Iterate over search results
                for result in search['results']:

                    # Filter by year and title
                    if 'release_date' in result and 'title' in result:
                        if arguments['year'].lower() in result['release_date'].lower() and \
                                (matchTitle(arguments['title']) == matchTitle(result['title']) or matchTitle(arguments['title']) == matchTitle(result['original_title'])):

                            # Find trailers for movie
                            videos = videosTMDB(result['id'], settings['lang'], settings['region'], settings['tmdb_api_key'])

                            for item in videos['results']:
                                if 'Trailer' in item['type'] and int(item['size']) >= int(settings['min_resolution']):
                                    video = 'https://www.youtube.com/watch?v='+item['key']

                                    # Download trailer from YouTube
                                    file = youtubeDownload(video, settings['min_resolution'], settings['max_resolution'], arguments['directory'], filename)

                                    # Update downloaded status
                                    if file:
                                        downloaded = True
                                        break
                    if downloaded:
                        break

            if downloaded:
                print('\033[92mSUCCESS:\033[0m Trailer downloaded.')

            else:
                print('\033[91mERROR:\033[0m No trailer found.')

        else:
            print('\033[93mWARNING:\033[0m Already downloaded.')

    else:
        print('\033[91mERROR:\033[0m You must pass a directory, title, and year to the script.')

# Run
if __name__ == '__main__':
    main()
