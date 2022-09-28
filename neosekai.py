from bs4 import BeautifulSoup
CONTENT= ['reading-content', 'text-left']

def new_chapter(soup):
    return soup.title.string[soup.title.string.find('Chapter'):soup.title.string.find('NeoSekai')-3]

def next_chapter(soup):
    soup.find("div", class_='nav-next').find('a', href=True)['href']