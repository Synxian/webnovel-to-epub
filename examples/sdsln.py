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
    return soup.title.string

args = {
    'title': 'some title',
    'starting_chapter_link': 'link',
    'starting_chapter_number': 1,
    'ending_chapter_number': 1,
    'file_name': 'some file name',
    'content_class': ['post-body-container', 'post-body entry-content float-container'],
    'chapter_title_function': chapter_title,
    'sanitizing_function': sanitize_content,
    'language': 'en',
}

EpubScrapper(**args)
