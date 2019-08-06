import io
import json
import os
import sys
from trailerdl.lib.utilities.logging import Logging

class Config:
    # Settings
    @staticmethod
    def settings():
        response = {
            'name': 'Trailer Downloader',
            'version': '2.0',
            'context': dict(
                help_option_names=['-h', '--help']
            )
        }
        if os.path.exists(os.path.split(os.path.abspath(__file__))[0]+'/../../settings.json'):
            with io.open(os.path.split(os.path.abspath(__file__))[0]+'/../../settings.json', mode='r', encoding='utf8') as file:
                try:
                    response = {**response, **json.load(file)}
                except:
                    Logging.invalidSettings(True, [], [])

                return Config.validateSettings(response)
        else:
            Logging.noSettings(True, [], [])

    # Language
    @staticmethod
    def language(lang):
        if os.path.exists(os.path.split(os.path.abspath(__file__))[0]+'/../languages/'+lang+'.json'):
            with io.open(os.path.split(os.path.abspath(__file__))[0]+'/../languages/'+lang+'.json', mode='r', encoding='utf8') as file:
                return json.load(file)
        else:
            Logging.noLanguage(True, [], [], lang)

    # Validate
    @staticmethod
    def validateSettings(settings):
        required_keys = [
            "tmdb_api_key",
            "region",
            "language",
            "min_resolution",
            "max_resolution",
            "scrapers",
            "limits",
            "subfolders",
            "formatting"
        ]

        has_subkeys = [
            "limits",
            "subfolders",
            "formatting"
        ]

        required_subkeys = [
            "Trailers",
            "Teasers",
            "Scenes",
            "Featurettes",
            "Behind The Scenes",
            "Bloopers"
        ]

        for key in required_keys:
            if key not in settings:
                Logging.missingSettingsKey(True, settings, [], key)

        for subkey in required_subkeys:
            for key in has_subkeys:
                if subkey not in settings[key]:
                    Logging.missingSettingsSubKey(True, settings, [], key, subkey)

        return settings

    # Validate Requirements
    @staticmethod
    def validateRequirements(settings, lang):
        if sys.version_info[0] < 3:
            Logging.incorrectPythonVersion(True, settings, lang, str(sys.version_info[0])+"."+str(sys.version_info[1])+"."+str(sys.version_info[2]))
            sys.exit()
        try:
            import click
        except:
            Logging.missingModule(True, settings, lang, 'click')
            sys.exit()
        try:
            from bs4 import BeautifulSoup, SoupStrainer
        except:
            Logging.missingModule(True, settings, lang, 'beautifulsoup')
            sys.exit()
        try:
            import tmdbsimple as tmdb
        except:
            Logging.missingModule(True, settings, lang, 'tmdbsimple')
            sys.exit()
        try:
            from unidecode import unidecode
        except:
            Logging.missingModule(True, settings, lang, 'unidecode')
            sys.exit()
        try:
            import youtube_dl
        except:
            Logging.missingModule(True, settings, lang, 'youtube_dl')
            sys.exit()