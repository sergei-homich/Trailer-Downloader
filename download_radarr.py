#!/usr/bin/env python3

from argparse import ArgumentParser
from configparser import *
import os
import sys

# Disable bytecode
sys.dont_write_bytecode = True

# Make sure python 3 is being used
if sys.version_info[0] < 3:
    print('\033[91mERROR:\033[0m you must be running python 3.0 or higher.')
    sys.exit()

# download.py
try:
    from download import main as downloadItem
except:
    print('\033[91mERROR:\033[0m download.py not found')
    sys.exit()

# Arguments
def getArguments():
    name = 'Trailer-Downloader Radarr Integration'
    version = '1.10'
    parser = ArgumentParser(description='{}: download a movie trailer from Apple or YouTube with help from TMDB'.format(name))
    parser.add_argument('-v', '--version', action='version', version='{} {}'.format(name, version), help='show the version number and exit')
    args = parser.parse_args()
    return {
        'file': os.environ.get('radarr_movie_path')
    }

# Main
def main():
    # Arguments
    arguments = getArguments()

    # Make sure a file path was passed from radarr
    if arguments['file'] is not None:

        # Make sure file path exists
        if not os.path.isfile(arguments['file']):
            print('\033[91mERROR:\033[0m The provided file path does not exist. Check your arguments.')
            sys.exit()

        # Get variables for the download script
        try:
            directory = os.path.abspath(os.path.dirname(arguments['file']))
            title = os.path.basename(directory)[0:os.path.basename(directory).rfind('(')].strip()
            year = os.path.basename(directory)[os.path.basename(directory).rindex('(')+1:].split(')')[0].strip()
        except:
            print(arguments['file'])
            print('\033[93mWARNING:\033[0m Failed to extract title and year from radarr movie path. Skipping...')
            sys.exit()

        # Set up arguments for other script
        sys.argv = [os.path.split(os.path.abspath(__file__))[0]+'/download.py', '--title', title, '--year', year, '--directory', directory]

        # Run other script
        downloadItem()

    else:

        print('\033[91mERROR:\033[0m you must pass the radarr movie path environment variable to the script. Are you sure Radarr fired this?')

# Run
if __name__ == '__main__':
    main()