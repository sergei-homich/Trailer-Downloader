import sys
sys.dont_write_bytecode = True
from argparse import ArgumentParser
from lib import helpers, apple, tmdb
from os import listdir, path

# Arguments
def getArguments():
    parser = ArgumentParser(description='{}: download a movie trailer from Apple or YouTube'.format(helpers.info()['name']))
    parser.add_argument("-v", "--version", action='version', version='{} {}'.format(helpers.info()['name'], helpers.info()['version']), help="show the version number and exit")
    parser.add_argument("-l", "--logging", action="append_const", const="logging", help="display additional logging information")
    parser.add_argument("-d", "--directory", dest="directory", help="full path of directory to copy downloaded trailer", metavar="DIRECTORY")
    parser.add_argument("-f", "--file", dest="file", help="full path of movie file", metavar="FILE")
    parser.add_argument("-t", "--title", dest="title", help="title of movie", metavar="TITLE")
    parser.add_argument("-y", "--year", dest="year", help="release year of movie", metavar="YEAR")
    args = parser.parse_args()
    # Python 2.7
    try:
        return {
            'logging': True if args.logging else False,
            'directory': str(args.directory).decode(helpers.format()) if args.directory != None else args.directory,
            'file': str(args.file).decode(helpers.format()) if args.file != None else args.file,
            'title': str(args.title).decode(helpers.format()) if args.title != None else args.title,
            'year': str(args.year).decode(helpers.format()) if args.year != None else args.year
        }
    # Python 3.0 and later
    except:
        return {
            'logging': True if args.logging else False,
            'directory': str(args.directory) if args.directory != None else args.directory,
            'file': str(args.file) if args.file != None else args.file,
            'title': str(args.title) if args.title != None else args.title,
            'year': str(args.year) if args.year != None else args.year
        }

# Main
def main():
    # Arguments
    arguments = getArguments()

    # Settings
    settings = helpers.getSettings()

    # If directory argument is not set, get directory from file
    if arguments['directory'] is None and arguments['file'] is not None:
        arguments['directory'] = path.abspath(path.dirname(arguments['file']))

    # If subfolder setting is set, add it to the directory
    if settings['subfolder'].strip():
        arguments['directory'] = arguments['directory']+'/'+settings['subfolder']

    # Make sure a movie directory or file, title, and year was passed
    if (arguments['directory'] is not None or arguments['file'] is not None) and arguments['title'] is not None and arguments['year'] is not None:
        # Logging
        helpers.logging(arguments['logging'], 'primary', 'Title', arguments['title']+'  ', False)
        helpers.logging(arguments['logging'], 'primary', 'Year', arguments['year']+'  ', False)
        helpers.logging(arguments['logging'], 'primary', 'Destination', arguments['directory'], True)

        # Get formatted filename
        filename = helpers.getFilename(arguments['title'], arguments['year'], settings['custom_formatting'])

        # Download status
        downloaded = False

        # Make sure trailer file doesn't already exist in the directory
        if path.exists(arguments['directory']):
            for name in listdir(arguments['directory']):
                if filename[:-4] in name:
                    downloaded = True

        # Search Apple for trailer
        if not downloaded:
            # Logging
            helpers.logging(arguments['logging'], 'primary', str('{0: <22}').format('Searching Apple...'), None, False)

            # Search
            search = apple.search(arguments['title'])

            # Iterate over search results
            for result in search['results']:
                # Filter by year and title
                if arguments['year'].lower() in result['releasedate'].lower() and helpers.matchTitle(arguments['title']) == helpers.matchTitle(helpers.unescape(result['title'])):
                    # Logging
                    helpers.logging(arguments['logging'], 'default', str('{0: <15}').format('Downloading'), None, False)

                    # Download trailer
                    file = apple.download('https://trailers.apple.com/'+result['location'], settings['resolution'], arguments['directory'], filename)

                    if file:
                        # Logging
                        helpers.logging(arguments['logging'], 'success', 'Done '+u'\u2713', None, True)

                        # Update downloaded status
                        downloaded = True
                        break

                    else:
                        # Logging
                        helpers.logging(arguments['logging'], 'error', 'Failed', None, True)

            if not downloaded:
                # Logging
                helpers.logging(arguments['logging'], 'warning', str('{0: <15}').format('No Results'), None, True)

            # Search YouTube for trailer
            if not downloaded:
                # Logging
                helpers.logging(arguments['logging'], 'primary', str('{0: <22}').format('Searching TMDB...'), None, False)

                # Search
                search = tmdb.search(arguments['title'], settings['api_key'])

                # Iterate over search results
                for result in search['results']:
                    # Filter by year and title
                    if arguments['year'].lower() in result['release_date'].lower() and helpers.matchTitle(arguments['title']) == helpers.matchTitle(result['title']):
                        # Find trailers for movie
                        videos = tmdb.videos(result['id'], settings['lang'], settings['region'], settings['api_key'])

                        # Iterate over video results
                        for item in videos['results']:
                            if 'Trailer' in item['type'] and int(item['size']) >= int(settings['min_resolution']):
                                # Logging
                                helpers.logging(arguments['logging'], 'default', str('{0: <15}').format('Downloading'), None, False)

                                # Download trailer
                                file = tmdb.download('https://www.youtube.com/watch?v='+item['key'], settings['min_resolution'], settings['max_resolution'], arguments['directory'], filename)

                                if file:
                                    # Logging
                                    helpers.logging(arguments['logging'], 'success', 'Done '+u'\u2713', None, True)

                                    # Update downloaded status
                                    downloaded = True
                                    break

                                else:
                                    # Logging
                                    helpers.logging(arguments['logging'], 'error', 'Failed', None, True)

                        break

                if not downloaded:
                    # Logging
                    helpers.logging(arguments['logging'], 'warning', str('{0: <15}').format('No Results'), None, True)

        else:
            # Logging
            helpers.logging(True, 'warning', 'WARNING', 'The trailer already exists in the selected directory. Skipping.', True)

    else:
        # Logging
        helpers.logging(True, 'danger', 'ERROR', 'You must pass a movie directory or file, title, and year to the script.', True)

# Run
if __name__ == '__main__':
    main()