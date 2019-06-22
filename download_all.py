import sys
sys.dont_write_bytecode = True
from argparse import ArgumentParser
from lib import helpers, apple, tmdb
from os import listdir, path

# Arguments
def getArguments():
    parser = ArgumentParser(description='{}: download a movie trailer from Apple or YouTube for all folders in a directory'.format(helpers.info()['name']))
    parser.add_argument("-v", "--version", action='version', version='{} {}'.format(helpers.info()['name'], helpers.info()['version']), help="show the version number and exit")
    parser.add_argument("-d", "--directory", dest="directory", help="directory used to find movie titles and years", metavar="DIRECTORY")
    args = parser.parse_args()
    # Python 2.7
    try:
        return {
            'directory': str(args.directory).decode(helpers.format()) if args.directory != None else args.directory
        }
    # Python 3.0 and later
    except:
        return {
            'directory': str(args.directory) if args.directory != None else args.directory
        }

# Main
def main():
    # Arguments
    arguments = getArguments()

    # Settings
    settings = helpers.getSettings()

    # Make sure a directory was passed
    if arguments['directory'] is not None:

        folder = arguments['directory']

        # Make sure folder exists
        if not path.exists(folder):
            print('\033[91mERROR:\033[0m The specified directory does not exist. Check your arguments.')
            sys.exit()

        # Iterate through items in folder
        for item in listdir(folder):

            # Make sure the item is a directory
            if path.isdir(folder+'/'+item):

                # Get variables for the download script
                try:
                    arguments['title'] = item[0:item.rfind('(')].strip()
                    arguments['year'] = item[item.rindex('(')+1:].split(')')[0].strip()
                    arguments['directory'] = folder+'/'+item
                except:
                    print(item)
                    print('\033[93mWARNING:\033[0m Failed to extract title and year from folder name. Skipping.')
                    continue

                # If subfolder setting is set, add it to the directory
                if settings['subfolder'].strip():
                    arguments['directory'] = arguments['directory']+'/'+settings['subfolder']

                # Get formatted filename
                filename = helpers.getFilename(arguments['title'], arguments['year'], settings['custom_formatting'])

                # Make sure the trailer has not already been downloaded
                if not path.exists(arguments['directory']+'/'+filename):

                    print(item)

                    # Download status
                    downloaded = False

                    # Make sure trailer file doesn't already exist in the directory
                    if path.exists(arguments['directory']):
                        for name in listdir(arguments['directory']):
                            if filename[:-4] in name:
                                downloaded = True

                    # Search Apple for trailer
                    if not downloaded:
                        # Search
                        search = apple.search(arguments['title'])

                        # Iterate over search results
                        for result in search['results']:

                            # Filter by year and title
                            if arguments['year'].lower() in result['releasedate'].lower() and helpers.matchTitle(arguments['title']) == helpers.matchTitle(helpers.unescape(result['title'])):

                                file = apple.download('https://trailers.apple.com/'+result['location'], settings['resolution'], arguments['directory'], filename)

                                # Update downloaded status
                                if file:
                                    downloaded = True
                                    break

                        # Search YouTube for trailer
                        if not downloaded:
                            # Search
                            search = tmdb.search(arguments['title'], settings['api_key'])

                            # Iterate over search results
                            for result in search['results']:

                                # Filter by year and title
                                if arguments['year'].lower() in result['release_date'].lower() and helpers.matchTitle(arguments['title']) == helpers.matchTitle(result['title']):

                                    # Find trailers for movie
                                    videos = tmdb.videos(result['id'], settings['lang'], settings['region'], settings['api_key'])

                                    for item in videos['results']:
                                        if 'Trailer' in item['type'] and int(item['size']) >= int(settings['min_resolution']):
                                            # Download trailer from YouTube
                                            file = tmdb.download('https://www.youtube.com/watch?v='+item['key'], settings['min_resolution'], settings['max_resolution'], arguments['directory'], filename)

                                            # Update downloaded status
                                            if file:
                                                downloaded = True
                                                break

                                    break

                    else:

                        print('\033[91mERROR:\033[0m the trailer already exists in the selected directory')

    else:

        print('\033[91mERROR:\033[0m you must pass a directory to the script')

# Run
if __name__ == '__main__':
    main()