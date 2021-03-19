#!/usr/bin/env python3

# Disable bytecode
import sys
sys.dont_write_bytecode = True

# Modules
from __init__ import NAME, VERSION, DESCRIPTION
from argparse import ArgumentParser
from configparser import *
import os

# download.py
try:
    from download import main as downloadItem
except:
    print('\033[91mERROR:\033[0m download.py not found')
    sys.exit()

# Arguments
def getArguments():
    name = NAME+' Library Integration'
    parser = ArgumentParser(description=name+': '+DESCRIPTION)
    parser.add_argument('-v', '--version', action='version', version=name+' '+VERSION, help='show the version number and exit')
    parser.add_argument('-d', '--directory', dest='directory', help='directory used to find movie titles and years', metavar='DIRECTORY')
    args = parser.parse_args()
    return {
        'directory': args.directory
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
    for key in ['subfolder', 'custom_formatting']:
        response[key]= config.get('DEFAULT', key)
    return response

# Main
def main():
    # Arguments
    arguments = getArguments()

    # Settings
    settings = getSettings()

    # Make sure a directory was passed
    if arguments['directory'] is not None:

        # Make sure directory exists
        if not os.path.exists(arguments['directory']):
            print('\033[91mERROR:\033[0m The specified directory does not exist. Check your arguments.')
            sys.exit()

        # Iterate through items in directory
        for item in os.listdir(arguments['directory']):

            # Make sure the item is a directory
            if os.path.isdir(arguments['directory']+'/'+item):

                # Get variables for the download script
                title = None
                year = None
                directory = None
                try:
                    title = item[0:item.rfind('(')].strip()
                    year = item[item.rindex('(')+1:].split(')')[0].strip()
                    directory = arguments['directory']+'/'+item
                except:
                    print(item)
                    print('\033[93mWARNING:\033[0m Failed to extract title and year from folder name. Skipping.')

                if title is not None and year is not None and directory is not None:
                    # If subfolder setting is set, add it to the destination directory
                    if settings['subfolder'].strip():
                        destination = directory+'/'+settings['subfolder']
                    else:
                        destination = directory

                    # Use custom formatting for filenames or use default if none is set
                    if settings['custom_formatting'].strip():
                        filename_ru = settings['custom_formatting'].replace('%title%', title).replace('%year%', year)+'.mp4'
                    else:
                        filename_ru = title+' ('+year+')-trailer.mp4'

                    # Make sure the trailer has not already been downloaded
                    if not os.path.exists(destination+'/' + filename_ru):
                        # Print current item
                        print(item)

                        # Set up arguments for other script
                        sys.argv = [os.path.split(os.path.abspath(__file__))[0]+'/download.py', '--title', title, '--year', year, '--directory', directory]

                        # Run other script
                        downloadItem()
    else:

        print('\033[91mERROR:\033[0m you must pass a directory to the script')

# Run
if __name__ == '__main__':
    main()