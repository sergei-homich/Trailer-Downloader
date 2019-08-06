# Trailer-Downloader
Simple python package for downloading extras including trailers, teasers, scenes, featurettes, behind the scenes, and bloopers from Apple, YouTube Rentals, or from YouTube with help from TMDB. This is useful if you are running a media server like Plex and you would like to have local trailers for each of your movies and series. For automation purposes, this package can be integrated with Radarr, Sonarr, and Tautulli or you can just run it manually. Enjoy!

## Requirements
-[Python 3.6+](https://www.python.org/)

-[beautifulsoup](https://pypi.org/project/beautifulsoup4/)

-[click](https://github.com/pallets/click)

-[ffmpeg](https://github.com/FFmpeg/FFmpeg)

-[tmdbsimple](https://github.com/celiao/tmdbsimple)

-[unidecode](https://github.com/avian2/unidecode)

-[youtube_dl](https://github.com/ytdl-org/youtube-dl)

## Installation
```
pip3 install trailerdl
```

## Settings
Edit the **settings.json** file. Here you can setup your api key for TMDB, region, language, resolution settings, and scraper order as well as your file limits, subfolders, and formatting for each media type.

Guidelines on how extras must be formatted to work with Plex can be found [here](https://support.plex.tv/articles/200220677-local-media-assets-movies/).

## Usage

### Download Extras for a Specific Movie or Series

To download media items for a specific movie, use the command below. You will need to provide the movie title, year, and destination. Optionally you can provide the library type and media types to download. The verbose flag will display additional logging information.
```
trailerdl download --title "A Star Is Born" --year "2018" --destination "/path/to/movies/A Star Is Born (2018) --type "Movies" --extra "Trailers" --verbose
```

### Download Extras for All Movies or Series in a Directory

To download trailers for an entire library that already exists, use the command below. You will need to supply the directory that all of your movie folders are in. The script will iterate through all of your movie folders in the directory and it will automatically pull the title and year from the folder name. Trailers will be downloaded into the folder for each movie.
```
trailerdl download-library --directory "/path/to/movies"
```

### Automation

This script can also be fired by Radarr, Sonarr, or Tautulli to automatically download a trailer each time a new movie or series is added to your collection.

#### Radarr

#### Sonarr

#### Tautulli

### Notes

This package expects your movies and series to be in a very specific structure. If your structure does not match the format below, you **will not** be able to use this package.

-Movies  
---Movie Title 1 (2014)  
-----Movie Title 1 (2014).mp4  
---Movie Title 2 (2009)  
-----Movie Title 2 (2009).mkv  

-Series  
---Series Title 1 (2018)  
-----Season 1  
-----Season 2  
---Series Title 2 (2009)  
-----Season 1  
-----Season 2  

### Building

If you'd like to contribute to this project, please use the commands below to get it set up and running on your machine.
```
git clone https://github.com/airship-david/Trailer-Downloader.git
cd Trailer-Downloader
python3 -m venv env
source env/bin/activate
pip install --editable .
```

**Enjoy!**