import sys
sys.dont_write_bytecode = True
import os
from trailerdl.lib.tools.download import Download
from trailerdl.lib.tools.scan import Scan
from trailerdl.lib.tools.search import Search
from trailerdl.lib.utilities.config import Config
from trailerdl.lib.utilities.logging import Logging

# Settings
settings = Config.settings()
lang = Config.language(settings['language'])

# Requirements
Config.validateRequirements(settings, lang)
import click

# CLI
@click.group(context_settings=settings['context'])
@click.version_option(
    prog_name=settings['name'],
    version=settings['version'],
    message='%(prog)s v%(version)s'
)
@click.pass_context
def cli(ctx):
    return

# Download
@cli.command(context_settings=settings['context'])
@click.version_option(
    prog_name=settings['name'],
    version=settings['version'],
    message='%(prog)s v%(version)s'
)
@click.option(
    '--'+lang['arguments']['title']['name'],
    help=lang['arguments']['title']['description'],
    metavar=lang['arguments']['title']['var'],
    required=True
)
@click.option(
    '--'+lang['arguments']['year']['name'],
    help=lang['arguments']['year']['description'],
    metavar=lang['arguments']['year']['var'],
    default=False
)
@click.option(
    '--'+lang['arguments']['destination']['name'],
    help=lang['arguments']['destination']['description'],
    metavar=lang['arguments']['destination']['var'],
    required=True
)
@click.option(
    '--'+lang['arguments']['type']['name'],
    help=lang['arguments']['type']['description'],
    type=click.Choice(lang['arguments']['type']['choices']),
    default=lang['arguments']['type']['default'],
    show_default=True
)
@click.option(
    '--'+lang['arguments']['extra']['name'],
    help=lang['arguments']['extra']['description'],
    type=click.Choice(lang['arguments']['extra']['choices']),
    default=lang['arguments']['extra']['default'],
    show_default=True,
    multiple=True
)
@click.option(
    '--'+lang['arguments']['verbose']['name'],
    help=lang['arguments']['verbose']['description'],
    is_flag=True
)
@click.pass_context
def download(ctx, title: str, year: str, destination: str, type: str, extra: tuple(), verbose: False):
    Logging.settings(verbose, settings, lang, destination, type, extra)

    scan = Scan(settings, lang, verbose)
    search = Search(settings, lang, verbose)
    download = Download(settings, lang, verbose)

    scan.add(title, year, destination, type, extra)

    for item in scan.run():
        search.add(item['title'], item['year'], item['destination'], item['type'], item['extras'], item['mapping'], item['missing'], item['needed_extras'])

    for item in search.run():
        download.add(item['title'], item['year'], item['type'], item['extra'], item['original_name'], item['scraper'], item['source'], item['url'], item['destination'], item['filename'])

    download.run()

# Download Library
@cli.command(context_settings=settings['context'])
@click.version_option(
    prog_name=settings['name'],
    version=settings['version'],
    message='%(prog)s v%(version)s'
)
@click.option(
    '--'+lang['arguments']['directory']['name'],
    help=lang['arguments']['directory']['description'],
    metavar=lang['arguments']['directory']['var'],
    required=True
)
@click.option(
    '--'+lang['arguments']['type']['name'],
    help=lang['arguments']['type']['description'],
    type=click.Choice(lang['arguments']['type']['choices']),
    default=lang['arguments']['type']['default'],
    show_default=True
)
@click.option(
    '--'+lang['arguments']['extra']['name'],
    help=lang['arguments']['extra']['description'],
    type=click.Choice(lang['arguments']['extra']['choices']),
    default=lang['arguments']['extra']['default'],
    show_default=True,
    multiple=True
)
@click.option(
    '--'+lang['arguments']['verbose']['name'],
    help=lang['arguments']['verbose']['description'],
    is_flag=True
)
@click.pass_context
def download_library(ctx, directory: str, type: str, extra: tuple(), verbose: False):
    Logging.settings(verbose, settings, lang, directory, type, extra)

    if os.path.exists(directory):
        scan = Scan(settings, lang, verbose)
        search = Search(settings, lang, verbose)
        download = Download(settings, lang, verbose)

        for item in sorted(os.listdir(directory)):
            if os.path.isdir(directory+'/'+item):
                try:
                    title = item[0:item.rfind('(')].strip()
                    year = item[item.rindex('(')+1:].split(')')[0].strip()
                except:
                    title = item.strip()
                    year = False
                destination = directory+'/'+item
                scan.add(title, year, destination, type, extra)

        for item in scan.run():
            search.add(item['title'], item['year'], item['destination'], item['type'], item['extras'], item['mapping'], item['missing'], item['needed_extras'])

        for item in search.run():
            download.add(item['title'], item['year'], item['type'], item['extra'], item['original_name'], item['scraper'], item['source'], item['url'], item['destination'], item['filename'])

        download.run()

    else:
        Logging.noDirectory(verbose, settings, lang)

# Radarr
@cli.command(context_settings=settings['context'])
@click.version_option(
    prog_name=settings['name'],
    version=settings['version'],
    message='%(prog)s v%(version)s'
)
@click.option(
    '--'+lang['arguments']['type']['name'],
    help=lang['arguments']['type']['description'],
    type=click.Choice(lang['arguments']['type']['choices']),
    default=lang['arguments']['type']['default'],
    show_default=True
)
@click.option(
    '--'+lang['arguments']['extra']['name'],
    help=lang['arguments']['extra']['description'],
    type=click.Choice(lang['arguments']['extra']['choices']),
    default=lang['arguments']['extra']['default'],
    show_default=True,
    multiple=True
)
@click.option(
    '--'+lang['arguments']['verbose']['name'],
    help=lang['arguments']['verbose']['description'],
    is_flag=True
)
@click.pass_context
def download_radarr(ctx, extra: tuple(), type: str, verbose: False):
    try:
        title = os.environ.get('radarr_movie_title')
        destination = os.environ.get('radarr_movie_path')
        try:
            year = destination[destination.rindex('(')+1:].split(')')[0].strip()
        except:
            year = False
    except:
        Logging.missingRadarrVars(verbose, settings, lang)

    Logging.settings(verbose, settings, lang, destination, type, extra)

    scan = Scan(settings, lang, verbose)
    search = Search(settings, lang, verbose)
    download = Download(settings, lang, verbose)

    scan.add(title, year, destination, type, extra)

    for item in scan.run():
        search.add(item['title'], item['year'], item['destination'], item['type'], item['extras'], item['mapping'], item['missing'], item['needed_extras'])

    for item in search.run():
        download.add(item['title'], item['year'], item['type'], item['extra'], item['original_name'], item['scraper'], item['source'], item['url'], item['destination'], item['filename'])

    download.run()

# Sonarr
@cli.command(context_settings=settings['context'])
@click.version_option(
    prog_name=settings['name'],
    version=settings['version'],
    message='%(prog)s v%(version)s'
)
@click.option(
    '--'+lang['arguments']['type']['name'],
    help=lang['arguments']['type']['description'],
    type=click.Choice(lang['arguments']['type']['choices']),
    default=lang['arguments']['type']['default'],
    show_default=True
)
@click.option(
    '--'+lang['arguments']['extra']['name'],
    help=lang['arguments']['extra']['description'],
    type=click.Choice(lang['arguments']['extra']['choices']),
    default=lang['arguments']['extra']['default'],
    show_default=True,
    multiple=True
)
@click.option(
    '--'+lang['arguments']['verbose']['name'],
    help=lang['arguments']['verbose']['description'],
    is_flag=True
)
@click.pass_context
def download_sonarr(ctx, extra: tuple(), type: str, verbose: False):
    try:
        title = os.environ.get('sonarr_series_title')
        destination = os.environ.get('sonarr_series_path')
        try:
            year = destination[destination.rindex('(')+1:].split(')')[0].strip()
        except:
            year = False
    except:
        Logging.missingRadarrVars(verbose, settings, lang)

    Logging.settings(verbose, settings, lang, destination, type, extra)

    scan = Scan(settings, lang, verbose)
    search = Search(settings, lang, verbose)
    download = Download(settings, lang, verbose)

    scan.add(title, year, destination, type, extra)

    for item in scan.run():
        search.add(item['title'], item['year'], item['destination'], item['type'], item['extras'], item['mapping'], item['missing'], item['needed_extras'])

    for item in search.run():
        download.add(item['title'], item['year'], item['type'], item['extra'], item['original_name'], item['scraper'], item['source'], item['url'], item['destination'], item['filename'])

    download.run()

# Tautulli
@cli.command(context_settings=settings['context'])
@click.version_option(
    prog_name=settings['name'],
    version=settings['version'],
    message='%(prog)s v%(version)s'
)
@click.option(
    '--'+lang['arguments']['title']['name'],
    help=lang['arguments']['title']['description'],
    metavar=lang['arguments']['title']['var'],
    required=True
)
@click.option(
    '--'+lang['arguments']['year']['name'],
    help=lang['arguments']['year']['description'],
    metavar=lang['arguments']['year']['var'],
    required=True
)
@click.option(
    '--'+lang['arguments']['file']['name'],
    help=lang['arguments']['file']['description'],
    metavar=lang['arguments']['file']['var'],
    required=True
)
@click.option(
    '--'+lang['arguments']['type']['name'],
    help=lang['arguments']['type']['description'],
    type=click.Choice(lang['arguments']['type']['choices']),
    default=lang['arguments']['type']['default'],
    show_default=True
)
@click.option(
    '--'+lang['arguments']['extra']['name'],
    help=lang['arguments']['extra']['description'],
    type=click.Choice(lang['arguments']['extra']['choices']),
    default=lang['arguments']['extra']['default'],
    show_default=True,
    multiple=True
)
@click.option(
    '--'+lang['arguments']['verbose']['name'],
    help=lang['arguments']['verbose']['description'],
    is_flag=True
)
@click.pass_context
def download_tautulli(ctx, title: str, year: str, file: str, type: str, extra: tuple(), verbose: False):
    destination = os.path.abspath(os.path.dirname(file))

    Logging.settings(verbose, settings, lang, destination, type, extra)

    scan = Scan(settings, lang, verbose)
    search = Search(settings, lang, verbose)
    download = Download(settings, lang, verbose)

    scan.add(title, year, destination, type, extra)

    for item in scan.run():
        search.add(item['title'], item['year'], item['destination'], item['type'], item['extras'], item['mapping'], item['missing'], item['needed_extras'])

    for item in search.run():
        download.add(item['title'], item['year'], item['type'], item['extra'], item['original_name'], item['scraper'], item['source'], item['url'], item['destination'], item['filename'])

    download.run()

# Main
if __name__ == '__main__':
    cli(obj={})