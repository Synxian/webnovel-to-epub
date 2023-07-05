import sys
sys.path.append('..')

from epub_scrapper import EpubScrapper #pylint: disable=c0413

def sanitize_content(content):
    for i in content.find_all('div', style='text-align: center;'):
        if i.find('img') and i.find('img').get('src')[0:4] == 'epub':
            i.replace_with(i.find('img'))
        else:
            i.decompose()
    for i in content.find_all('span'):
        i.decompose()

def chapter_title(soup):
    return soup.title.string[soup.title.string.find('Chapter'):soup.title.string.find('NeoSekai')-3]

def next_chapter(soup):
    return soup.find("div", class_='nav-next').find('a', href=True)['href']

args = {
    'title': 'some title',
    'starting_chapter_link': 'link',
    'starting_chapter_number': 1,
    'ending_chapter_number': 2,
    'file_name': 'some file name',
    'content_class': ['reading-content', 'text-left'],
    'chapter_title_function': chapter_title,
    'sanitizing_function': sanitize_content,
    'language': 'en',
    'next_chapter_function': next_chapter
}

EpubScrapper(**args)