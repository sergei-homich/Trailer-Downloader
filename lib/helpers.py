from __future__ import unicode_literals
from os import name
from sys import stdout
from unicodedata import normalize
from unidecode import unidecode

# Python 3.0 and later
try:
    from configparser import ConfigParser
    import html.parser

# Python 2.7
except ImportError:
    from ConfigParser import ConfigParser
    from HTMLParser import HTMLParser

# unidecode
try:
    from unidecode import unidecode
except:
    # Logging
    helpers.logging(True, 'danger', 'ERROR', 'Package unidecode is not installed.', True)
    sys.exit()

# Info
def info():
    return {
        'name': 'Trailer-Downloader',
        'version': '1.05'
    }

# Settings
def getSettings():
    config = ConfigParser()
    config.read('settings.ini')
    return {
        'api_key': config.get('DEFAULT', 'tmdb_api_key'),
        'region': config.get('DEFAULT', 'region'),
        'lang': config.get('DEFAULT', 'lang'),
        'resolution': config.get('DEFAULT', 'resolution'),
        'max_resolution': config.get('DEFAULT', 'max_resolution'),
        'min_resolution': config.get('DEFAULT', 'min_resolution'),
        'subfolder': config.get('DEFAULT', 'subfolder'),
        'custom_formatting': config.get('DEFAULT', 'custom_formatting')
    }

# Format
def format():
    return 'windows-1252' if name == 'nt' else 'utf-8'

# Get filename
def getFilename(title, year, custom_formatting):
    if custom_formatting.strip():
        return custom_formatting.replace('%title%', title.replace(':', '-')).replace('%year%', year)+'.mp4'
    else:
        return title.replace(':', '-')+' ('+year+')-trailer.mp4'

# Remove special characters
def removeSpecialChars(query):
    return "".join([ch for ch in query if ch.isalnum() or ch.isspace()])

# Remove accent characters
def removeAccents(query):
    return unidecode(query)

# Unescape characters
def unescape(query):
    # Python 3.0 and later
    try:
        return html.unescape(query)
    # Python 2.7
    except:
        return HTMLParser().unescape(query)

# Match titles
def matchTitle(title):
    return normalize('NFKD', removeSpecialChars(title).replace('/', '').replace('\\', '').replace('-', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace("'", '').replace('<', '').replace('>', '').replace('|', '').replace('.', '').replace('+', '').replace(' ', '').lower()).encode('ASCII', 'ignore')

# Logging
def logging(logging, type, title, message, newline):
    if logging:
        if type == 'default':
            color = '\033[97m'
        elif type == 'primary':
            color = '\033[94m'
        elif type == 'success':
            color = '\033[92m'
        elif type == 'warning':
            color = '\033[93m'
        elif type == 'danger':
            color = '\033[91m'
        else:
            color = '\033[97m'
        color_end = '\033[0m'

        stdout.write(color+title+(': ' if message != None else '')+color_end+(message if message != None else '')+('\n' if newline else ' '))
        stdout.flush()