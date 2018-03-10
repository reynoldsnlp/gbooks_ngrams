"""Extract URLs from Google Books N-gram dataset for Russian."""

import os

from bs4 import BeautifulSoup
import requests

if not os.path.isfile('urls_gbooks_ngrams.html'):
    print('Downloading n-gram dataset webpage with links...', end='')
    url = 'http://storage.googleapis.com/books/ngrams/books/datasetsv2.html'
    response = requests.get(url)
    with open('urls_gbooks_ngrams.html', 'w') as f:
        f.write(response.text)
    print('done!')
else:
    print('urls_gbooks_ngrams.html found!')

print('Parsing the html file to extract urls...')
with open('urls_gbooks_ngrams.html') as f:
    soup = BeautifulSoup(f, 'html5lib')
print('    ...search for <a> tags')
with open('urls_totalcounts.txt', 'w') as utot, \
     open('urls_1gram.txt', 'w') as u1, \
     open('urls_2gram.txt', 'w') as u2, \
     open('urls_3gram.txt', 'w') as u3, \
     open('urls_4gram.txt', 'w') as u4, \
     open('urls_5gram.txt', 'w') as u5, \
     open('urls_dependency.txt', 'w') as d:
    for link in soup.find_all('a'):
        href = link.get('href')
        if '-rus-' in href and '20120701' in href:
            print(f'...processing {href}')
            if 'totalcounts' in href:
                print(href, file=utot)
            elif '-1gram-' in href:
                print(href, file=u1)
            elif '-2gram-' in href:
                print(href, file=u2)
            elif '-3gram-' in href:
                print(href, file=u3)
            elif '-4gram-' in href:
                print(href, file=u4)
            elif '-5gram-' in href:
                print(href, file=u5)
            elif '-0gram-' in href:
                print(href, file=d)
            else:
                print(f'...IGNORED: {href}')
