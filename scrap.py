import urllib.request
from bs4 import BeautifulSoup
import sys
import re
import json
import time

def getSoup(url):
    return BeautifulSoup(urllib.request.urlopen(url).read(), 'html.parser')

index_page = getSoup("https://www.poesie-francaise.fr/poemes-auteurs/")
author_links = index_page.select('.menu-centrale a')
author_count = author_total = len(author_links)

db = {}

for i, author_link in enumerate(author_links):
    author_url = str(author_link.get('href')).replace('.fr/poemes-', '.fr/')
    try:
        if author_url == 'https://www.poesie-francaise.fr/':
            author_count -= 1
            continue

        author = author_url.split('/')[-2]
        author_page = getSoup(author_url)
        db[author] = []

        poem_links = author_page.select('article > .w3-panel > a')
        poem_count = poem_total = len(poem_links)

        for j, poem_link in enumerate(poem_links):
            poem_url = str(poem_link.get('href'))
            if not poem_url.startswith(author_url):
                poem_count -= 1
                continue
            try:
                poem_page = getSoup(poem_url)
                poem = poem_page.select('#content > article > .w3-content > p')
                title = poem_page.select('#content > article > .w3-content > h2')
                book = poem_page.select('#content > article > .w3-content > .w3-margin-bottom > a')
                if len(poem) == 0:
                    continue
                else:
                    poem = poem[0]

                if len(title) == 0:
                    title = 'Sans Titre'
                else:
                    title = title[0].getText()

                if len(book) == 0:
                    book = '.'
                else:
                    book = book[0].getText()

                db[author].append({
                    'titre': title,
                    'recueil': book,
                    'content': poem.get_text(separator='\n'),
                })
                print(f'({i-(author_total-author_count)+1:4d}:{author_count:4d}){author}: [{j-(poem_total-poem_count)+1:4d}/{poem_count:4d}]', end='\r')
            except:
                print(f'Error {poem_url}')
            # time.sleep(1)
        print()
    except:
        print(f'Error {author_url}')

with open('poemes.json', 'w') as jfile:
    jfile.write(json.dumps(db))
