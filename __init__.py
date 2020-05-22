#!/usr/bin/env python3

# Disable bytecode
import sys
sys.dont_write_bytecode = True

# Make sure python 3 is being used
if sys.version_info[0] < 3:
    print('\033[91mERROR:\033[0m you must be running python 3.0 or higher.')
    sys.exit()

# Defaults
NAME = 'Trailer-Downloader'
VERSION = '1.14'
DESCRIPTION = 'download a movie trailer from Apple or YouTube with help from TMDB'