import sys
sys.dont_write_bytecode = True
from argparse import ArgumentParser
from os import listdir, path, system
import lib

# Arguments
def getArguments():
    parser = ArgumentParser(description='{}: download a movie trailer from Apple or YouTube for all folders in a directory'.format(lib.helpers.info()['name']))
    parser.add_argument("-v", "--version", action='version', version='{} {}'.format(lib.helpers.info()['name'], lib.helpers.info()['version']), help="show the version number and exit")
    parser.add_argument("-d", "--directory", dest="directory", help="directory used to find movie titles and years", metavar="DIRECTORY")
    args = parser.parse_args()
    return {
        'directory': str(args.directory).decode(lib.helpers.format())
    }

# Main
def main():
    # Arguments
    arguments = getArguments()

    # Settings
    settings = lib.helpers.getSettings()

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
                filename = lib.helpers.getFilename(arguments['title'], arguments['year'], settings['custom_formatting'])

                # Make sure the trailer has not already been downloaded
                if not path.exists(arguments['directory']+'/'+filename):

                    print(item)

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

        print('\033[91mERROR:\033[0m you must pass a directory to the script')

# Run
if __name__ == '__main__':
    main()