import sys
sys.dont_write_bytecode = True
from argparse import ArgumentParser
from os import listdir, path
import lib

# Arguments
def getArguments():
    parser = ArgumentParser(description='{}: download a movie trailer from Apple or YouTube'.format(lib.helpers.info()['name']))
    parser.add_argument("-v", "--version", action='version', version='{} {}'.format(lib.helpers.info()['name'], lib.helpers.info()['version']), help="show the version number and exit")
    parser.add_argument("-d", "--directory", dest="directory", help="full path of directory to copy downloaded trailer", metavar="DIRECTORY")
    parser.add_argument("-f", "--file", dest="file", help="full path of movie file", metavar="FILE")
    parser.add_argument("-t", "--title", dest="title", help="title of movie", metavar="TITLE")
    parser.add_argument("-y", "--year", dest="year", help="release year of movie", metavar="YEAR")
    args = parser.parse_args()
    return {
        'directory': str(args.directory).decode(lib.helpers.format()),
        'file': str(args.file).decode(lib.helpers.format()),
        'title': str(args.title).decode(lib.helpers.format()),
        'year': str(args.year).decode(lib.helpers.format())
    }

# Main
def main():
    # Arguments
    arguments = getArguments()

    # Settings
    settings = lib.helpers.getSettings()

    # If directory argument is not set, get directory from file
    if arguments['directory'] is None and arguments['file'] is not None:
        arguments['directory'] = path.abspath(path.dirname(arguments['file']))

    # If subfolder setting is set, add it to the directory
    if settings['subfolder'].strip():
        arguments['directory'] = arguments['directory']+'/'+settings['subfolder']

    # Make sure a movie directory or file, title, and year was passed
    if (arguments['directory'] is not None or arguments['file'] is not None) and arguments['title'] is not None and arguments['year'] is not None:
        # Get formatted filename
        filename = lib.helpers.getFilename(arguments['title'], arguments['year'], settings['custom_formatting'])

        # Download status
        downloaded = False

        # Make sure trailer file doesn't already exist in the directory
        for name in listdir(arguments['directory']):
            if filename[:-4] in name:
                downloaded = True

        # Search Apple for trailer
        if not downloaded:
            search = lib.apple.search(arguments['title'])

            # Iterate over search results
            for result in search['results']:

                # Filter by year and title
                if arguments['year'].lower() in result['releasedate'].lower() and lib.helpers.matchTitle(arguments['title']) == lib.helpers.matchTitle(lib.helpers.unescape(result['title'])):

                    file = lib.apple.download('https://trailers.apple.com/'+result['location'], settings['resolution'], arguments['directory'], filename)

                    # Update downloaded status
                    if file:
                        downloaded = True
                        break

            # Search YouTube for trailer
            if not downloaded:
                try:
                    search = lib.tmdb.search(arguments['title'], settings['api_key'])
                except:
                    print('\033[91mERROR:\033[0m Failed to connect to TMDB. Check your api key.')
                    sys.exit()

                # Iterate over search results
                for result in search['results']:

                    # Filter by year and title
                    if arguments['year'].lower() in result['release_date'].lower() and lib.helpers.matchTitle(arguments['title']) == lib.helpers.matchTitle(result['title']):

                        # Find trailers for movie
                        videos = lib.tmdb.videos(result['id'], settings['lang'], settings['region'], settings['api_key'])

                        for item in videos['results']:
                            if 'Trailer' in item['type'] and int(item['size']) >= int(settings['min_resolution']):
                                video = 'https://www.youtube.com/watch?v='+item['key']

                                # Download trailer from YouTube
                                file = lib.tmdb.download(video, settings['min_resolution'], settings['max_resolution'], arguments['directory'], filename)

                                # Update downloaded status
                                if file:
                                    downloaded = True
                                    break

                        break

        else:

            print('\033[91mERROR:\033[0m the trailer already exists in the selected directory')

    else:

        print('\033[91mERROR:\033[0m you must pass a movie directory or file, title, and year to the script')

# Run
if __name__ == '__main__':
    main()