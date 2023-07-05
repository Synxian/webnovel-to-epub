import sys
import re
sys.path.append('..')

from epub_scrapper import EpubScrapper #pylint: disable=c0413

def sanitize_content(content):
    for i in content.find_all('div'):
        if i.find('img') and i.find('img').get('src')[0:4] == 'epub':
            i.replace_with(i.find('img'))
        else:
            i.decompose()
    for i in content.find_all('span'):
        i.decompose()

def chapter_title(soup):
    return soup.title.string[soup.title.string.find('Chapter'):soup.title.string.find('CClaw')-3]

def remove_discord(content):
    if 'Join the discord server' in content.p.get_text():
        content.p.decompose()


args = {
    'title': 'some title',
    'starting_chapter_link': 'link',
    'starting_chapter_number': 0,
    'ending_chapter_number': 0,
    'file_name': 'some file name',
    'content_class': ['entry-content'],
    'chapter_title_function': chapter_title,
    'sanitizing_function': sanitize_content,
    'language': 'en',
    'add_images': 'Bool',
    'cover_link': 'link',
    'extra_funcs': [remove_discord]
}

EpubScrapper(**args)
