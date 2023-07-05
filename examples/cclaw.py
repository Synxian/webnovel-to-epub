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
    for i in content.find_all('p'):
        if re.search(r'(discord.gg|discord)', i.get_text(), re.IGNORECASE):
            i.decompose()

def remove_patreon(content):
    for i in content.find_all('p'):
        if re.search(r'(patreon)', i.get_text(), re.IGNORECASE):
            i.decompose()


def next_chapter(soup):
    return soup.find("div", class_='nav-next').find('a', href=True)['href']


args = {
    'title': 'some title',
    'starting_chapter_link': 'link',
    'starting_chapter_number': 1,
    'ending_chapter_number': 2,
    'file_name': 'some file name',
    'content_class': ['entry-content'],
    'chapter_title_function': chapter_title,
    'sanitizing_function': sanitize_content,
    'cover_link': 'link',
    'language': 'en',
    'add_images': True,
    'extra_funcs': [remove_discord, remove_patreon],
    'next_chapter_function': next_chapter
}

EpubScrapper(**args)
