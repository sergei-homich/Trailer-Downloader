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
    name = NAME+' Tautulli Integration'
    parser = ArgumentParser(description=name+': '+DESCRIPTION)
    parser.add_argument('-v', '--version', action='version', version=name+' '+VERSION, help='show the version number and exit')
    parser.add_argument('-f', '--file', dest='file', help='full path of movie file', metavar='FILE')
    args = parser.parse_args()
    return {
        'file': str(args.file) if args.file != None else args.file
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
            print('\033[93mWARNING:\033[0m Failed to extract title and year from file. Skipping...')
            sys.exit()

        # Set up arguments for other script
        sys.argv = [os.path.split(os.path.abspath(__file__))[0]+'/download.py', '--title', title, '--year', year, '--directory', directory]

        # Run other script
        downloadItem()

    else:
        print('\033[91mERROR:\033[0m you must pass a file to the script. Are you sure Tautulli fired this?')

# Run
if __name__ == '__main__':
    main()