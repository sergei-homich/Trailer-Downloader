from argparse import ArgumentParser
import os
import sys

# Python 3.0 and later
try:
    from configparser import *

# Python 2.7
except ImportError:
    from ConfigParser import *

# Arguments
def getArguments():
    name = 'Trailer-Downloader'
    version = '1.06'
    parser = ArgumentParser(description='{}: download a movie trailer from Apple or YouTube for all folders in a directory'.format(name))
    parser.add_argument("-v", "--version", action='version', version='{} {}'.format(name, version), help="show the version number and exit")
    parser.add_argument("-d", "--directory", dest="directory", help="directory used to find movie titles and years", metavar="DIRECTORY")
    args = parser.parse_args()
    return {
        'directory': args.directory
    }

# Settings
def getSettings():
    config = ConfigParser()
    config.read(os.path.split(os.path.abspath(__file__))[0]+'/settings.ini')
    return {
        'subfolder': config.get('DEFAULT', 'subfolder'),
        'custom_formatting': config.get('DEFAULT', 'custom_formatting'),
        'python_path': config.get('DEFAULT', 'python_path')
    }

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

        # Make sure specified python path exists or attempt to use default if none is set
        if settings['python_path'].strip() and not os.path.exists(settings['python_path']):
            print('\033[91mERROR:\033[0m The specified path to python does not exist. Check your settings.')
            sys.exit()
        else:
            settings['python_path'] = 'python'

        # Iterate through items in directory
        for item in os.listdir(arguments['directory']):

            # Make sure the item is a directory
            if os.path.isdir(arguments['directory']+'/'+item):

                # Get variables for the download script
                try:
                    title = item[0:item.rfind('(')].strip()
                    year = item[item.rindex('(')+1:].split(')')[0].strip()
                    directory = arguments['directory']+'/'+item
                except:
                    print(item)
                    print('\033[93mWARNING:\033[0m Failed to extract title and year from folder name. Skipping.')
                    continue

                # If subfolder setting is set, add it to the destination directory
                if settings['subfolder'].strip():
                    destination = directory+'/'+settings['subfolder']
                else:
                    destination = directory

                # Use custom formatting for filenames or use default if none is set
                if settings['custom_formatting'].strip():
                    filename = settings['custom_formatting'].replace('%title%', title).replace('%year%', year)+'.mp4'
                else:
                    filename = title+' ('+year+')-trailer.mp4'

                # Make sure the trailer has not already been downloaded
                if not os.path.exists(destination+'/'+filename):

                    # Print current item
                    print(item)

                    # Download trailer for item
                    os.system(settings['python_path']+' '+os.path.split(os.path.abspath(__file__))[0]+'/download.py --title "'+title+'" --year "'+year+'" --directory "'+directory+'"')

    else:

        print('\033[91mERROR:\033[0m you must pass a directory to the script')

# Run
if __name__ == '__main__':
    main()