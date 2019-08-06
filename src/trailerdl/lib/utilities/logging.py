import click
import sys
import unicodedata

class Logging:
    # Settings
    @staticmethod
    def settings(verbose, settings, lang, directory, type, extra):
        if verbose:
            click.secho(message='\033[94m'+settings['name']+'\033[0m v'+settings['version'], nl=True)
            click.secho(message='\n'+lang['settings'], fg='blue', nl=True)
            click.secho(message=lang['tmdb_api_key']+': '+str(settings['tmdb_api_key']), nl=True)
            click.secho(message=lang['region']+': '+str(settings['region']), nl=True)
            click.secho(message=lang['language']+': '+str(settings['language']), nl=True)
            click.secho(message=lang['min_resolution']+': '+str(settings['min_resolution']), nl=True)
            click.secho(message=lang['max_resolution']+': '+str(settings['max_resolution']), nl=True)
            click.secho(message=lang['scrapers']+': '+str(', '.join(settings['scrapers'])), nl=True)
            click.secho(message=lang['limits']+':\n'+str('\n'.join('    {}: {}'.format(key, value) for key, value in settings['limits'].items())), nl=True)
            click.secho(message=lang['subfolders']+':\n'+str('\n'.join('    {}: {}'.format(key, value) for key, value in settings['subfolders'].items())), nl=True)
            click.secho(message=lang['formatting']+':\n'+str('\n'.join('    {}: {}'.format(key, value) for key, value in settings['formatting'].items())), nl=True)
            click.secho(message='\n'+lang['selection'], fg='blue', nl=True)
            click.secho(message=lang['directory']+': '+directory, nl=True)
            click.secho(message=lang['library_type']+': '+type, nl=True)
            click.secho(message=lang['extra_types']+': '+str(', '.join(extra)), nl=True)

    # Scanning
    @staticmethod
    def scanning(verbose, settings, lang):
        if verbose:
            click.secho(message='\n'+lang['scanning']+'...', fg='blue', nl=True)

    # Scanning Item
    @staticmethod
    def scanningItem(verbose, settings, lang, item):
        if verbose:
            click.secho(message=str(u'{0:<70}').format('\033[92m'+lang['title']+': \033[0m'+unicodedata.normalize('NFC', item['title']))+
                                str('{0:<25}').format('\033[92m'+lang['year']+': \033[0m'+(item['year'] if item['year'] else '?'))+
                                str('{0:<25}').format('\033[92m'+lang['missing']+': \033[0m'+str(item['missing']))+
                                str('{}').format('\033[92m'+lang['destination']+': \033[0m'+item['destination'].split('/')[-1]), nl=True)

    # Searching
    @staticmethod
    def searching(verbose, settings, lang):
        if verbose:
            click.secho(message='\n'+lang['searching']+'...', fg='blue', nl=True)

    # Searching Item
    @staticmethod
    def searchingItem(verbose, settings, lang, item):
        if verbose:
            click.secho(message='\033[92m'+lang['searching']+': '+'\033[0m'+item['title'], nl=True)

    # Downloading
    @staticmethod
    def downloading(verbose, settings, lang):
        if verbose:
            click.secho(message='\n'+lang['downloading']+'...', fg='blue', nl=True)

    # Downloading Item
    @staticmethod
    def downloadingItem(verbose, settings, lang, item):
        if verbose:
            click.secho(message='\033[92m'+lang['downloading']+': '+'\033[0m'+item['url'], nl=True)

    # Time
    @staticmethod
    def time(verbose, settings, lang, seconds):
        if verbose:
            click.secho(message='\033[94m'+lang['time']+': '+'\033[0m'+'{:.2f}'.format(seconds)+' seconds', nl=True)

    # Missing
    @staticmethod
    def missing(verbose, settings, lang, total):
        if verbose:
            click.secho(message='\033[94m'+lang['missing']+': '+'\033[0m'+str(total), nl=True)

    # Found
    @staticmethod
    def found(verbose, settings, lang, total):
        if verbose:
            click.secho(message='\033[94m'+lang['found']+': '+'\033[0m'+str(total), nl=True)

    # Downloaded
    @staticmethod
    def downloaded(verbose, settings, lang, total):
        if verbose:
            click.secho(message='\033[94m'+lang['downloaded']+': '+'\033[0m'+str(total), nl=True)

    # No Settings
    @staticmethod
    def noSettings(verbose, settings, lang):
        if verbose:
            print('\033[91mNo settings.json file found. Please see the documentation.\033[0m')
            sys.exit()

    # Invalid Settings
    @staticmethod
    def invalidSettings(verbose, settings, lang):
        if verbose:
            print('\033[91mInvalid settings.json file found. Please see the documentation.\033[0m')
            sys.exit()

    # Missing Settings Key
    @staticmethod
    def missingSettingsKey(verbose, settings, lang, key):
        if verbose:
            print('\033[91mMissing option in settings.json file ('+key+'). Please see the documentation.\033[0m')
            sys.exit()

    # Missing Settings SubKey
    @staticmethod
    def missingSettingsSubKey(verbose, settings, lang, key, subkey):
        if verbose:
            print('\033[91mMissing option in '+key+' section of settings.json file ('+subkey+'). Please see the documentation.\033[0m')
            sys.exit()

    # No Language
    @staticmethod
    def noLanguage(verbose, settings, lang, choice):
        if verbose:
            print('\033[91mThe language file for the lanugage specified in the settings.json file does not exist. Please see the documentation. ('+choice+')\033[0m')
            sys.exit()

    # Missing Module
    @staticmethod
    def incorrectPythonVersion(verbose, settings, lang, version):
        if verbose:
            print('\033[91m'+lang['incorrect_python_version']+' ('+version+')\033[0m')
            sys.exit()

    # Missing Module
    @staticmethod
    def missingModule(verbose, settings, lang, module):
        if verbose:
            print('\033[91m'+lang['module_not_found']+' ('+module+')\033[0m')
            sys.exit()

    # No Directory
    @staticmethod
    def noDirectory(verbose, settings, lang):
        if verbose:
            click.secho(message=lang['directory_does_not_exist'], fg='red', nl=True, err=True)
            sys.exit()

    # Missing Radarr Variables
    @staticmethod
    def missingRadarrVars(verbose, settings, lang):
        if verbose:
            click.secho(message=lang['missing_radarr_environment_variables'], fg='red', nl=True, err=True)
            sys.exit()

    # Invalid TMDB API Key
    @staticmethod
    def invalidTmdbApiKey(verbose, settings, lang):
        if verbose:
            click.secho(message=lang['invalid_tmdb_api_key'], fg='red', nl=True, err=True)
            sys.exit()

    # Invalid TMDB API Key
    @staticmethod
    def scraperNotFound(verbose, settings, lang, scraper):
        if verbose:
            click.secho(message=lang['scraper_not_found']+" ("+scraper+")", fg='red', nl=True, err=True)
            sys.exit()