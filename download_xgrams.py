"""Download data using links in urls/"""

import errno
from glob import glob
import os
import sys

import requests

try:
    n = sys.argv[1]  # what size of n-gram?
except IndexError:
    n = input('What size ngrams do you want to download? (1/2/3/4/5)  ')
try:
    os.mkdir(f'{n}grams')
except OSError as e:
    if e.errno != errno.EEXIST:
        raise
try:
    force_all = sys.argv[2]:
except IndexError:
    force_all = False
if force_all in {'None', 'none'}:
    force_all = None
    print('Existing files will NOT be replaced by downloading them again.')
elif force_all:
    force_all = True
    print('Existing files WILL be replaced by downloading them again.')


def download(url, path):
    print(f'Downloading {url}...')
    r =  requests.get(url, stream=True)
    with open(path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)


with open(f'urls/urls_{n}gram.txt') as url_file:
    for url in url_file:
        url = url.strip()
        path = f'{n}grams/' + url.split('/')[-1]
        if os.path.exists(path):
            if force_all:
                download(url, path)
            elif force_all is None:
                continue
            else:
                force = input(f'{path} already exists.\n\t'
                              'Download again? (yes/yes-all/NO/no-all) ')
                if force in {'Y', 'y', 'yes', 'Yes'}:
                    download(url, path)
                elif force in {'yes-all', 'Yes-all', 'yesall', 'Yesall'}:
                    force_all = True
                    download(url, path)
                elif force in {'N', 'n', 'no', 'No', 'NO', ''}:
                    continue
                elif force in {'no-all', 'No-all', 'noall', 'Noall'}:
                    force_all = None
                    continue
                else:
                    print('\tUnrecognized response. Skipping...')
        else:
            download(url, path)

