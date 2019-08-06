import sys
sys.dont_write_bytecode = True
from setuptools import setup, find_namespace_packages

setup(
  name='trailerdl',
  version='2.0',
  author='David Engel',
  license='GNU General Public License v3.0',
  platforms='Python 3.6',
  description='Simple python package for downloading extras for movies and series.',
  long_description='Download trailers, teasers, scenes, featurettes, behind the scenes, and bloopers for your movies and series.',
  long_description_content_type='text/markdown',
  url='https://github.com/airship-david/Trailer-Downloader',
  classifiers=[
    "Programming Language :: Python :: 3.6",
    "License :: OSI Approved :: GNU General Public License v3.0",
    "Operating System :: OS Independent"
  ],
  package_dir={'': 'src'},
  packages=find_namespace_packages(where='src'),
  include_package_data=True,
  install_requires=[
    'bs4',
    'click',
    'tmdbsimple',
    'unidecode',
    'youtube_dl'
  ],
  entry_points={
    'console_scripts': [
      'trailerdl=trailerdl.cli:cli'
    ]
  }
)