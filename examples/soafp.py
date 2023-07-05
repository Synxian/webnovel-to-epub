import sys
sys.path.append('..')

from epub_scrapper import EpubScrapper #pylint: disable=c0413

def sanitize_content(content):
    for i in content.find_all('div'):
        i.decompose()
    for i in content.find_all('span'):
        i.decompose()

def chapter_title(soup):
    return soup.find('header', 'entry-header').find(class_='entry-title').string

def remove_translator(content):
    if 'Translator:' in content.p.string:
        content.p.decompose()

def next_chapter(content):
    return content.find("div", class_='nav-next').find('a', href=True)['href']

args = {
    'title': 'some title',
    'starting_chapter_link': 'link',
    'starting_chapter_number': 1,
    'ending_chapter_number': 2,
    'file_name': 'some file name',
    'content_class': ['entry-content'],
    'chapter_title_function': chapter_title,
    'sanitizing_function': sanitize_content,
    'language': 'en',
    'extra_funcs': [remove_translator],
    'next_chapter_function': next_chapter
}

EpubScrapper(**args)
