import re
import requests
from bs4 import BeautifulSoup
from ebooklib import epub
from constants import DEFAULT_STYLE
#============================================variables=============================================#
TITLE = 'The girl who betrayed me reigns in the top caste at my high school - vol 03' #book title
chapter = 'https://soafp.com/soafps/the-girl-who-betrayed-me/chapter-16-orders-and-sly-requests/' #first chapter link # pylint:disable=invalid-name
STARTING_CHAP = 1
TOTAL_CHAPTERS = 1
FILE_TITLE = 'placeholder'+'.epub' #title of the resulting epub
CONTENT_CLASS = ['entry-content'] #div where the reading content is at, if chapter title is included, remove the following lines # pylint:disable=line-too-long
TOC = []
#==================================================================================================#

def sanitize_content(content):
    for l in content.find_all('div'):
        l.decompose()
    for l in content.find_all('span'):
        l.decompose()

def next_chapter(htm):
    return htm.find("div", class_='nav-next').find('a', href=True)['href']

def replace_hr(content):
    for l in content.find('hr'):
        aux = soup.new_tag('hr')
        l.insert_after(aux)
        l.unwrap()

def remove_translator(content):
    if 'Translator:' in content.p.string:
        content.p.decompose()

book = epub.EpubBook()

chapters={}
book.set_title(TITLE)

for i in range(STARTING_CHAP, TOTAL_CHAPTERS+1):
    response = requests.get(chapter)
    soup = BeautifulSoup(response.content, "html.parser")
    chapter_content = soup.find('div', CONTENT_CLASS[0]) #div where the reading content is at, if chapter title is included, remove the following lines # pylint:disable=line-too-long
    chapter = next_chapter(soup) #function to find next chapter url
    remove_translator(chapter_content)
    sanitize_content(chapter_content)
    chapter_title = soup.find('header', 'entry-header').find(class_='entry-title').string #function to find chapter title # pylint:disable=line-too-long
    title_html = "<h1>"+chapter_title+"</h1>"
    chapter_content = chapter_content.renderContents()
    chapters[f"c{i}"] = epub.EpubHtml(title=title_html, file_name=f'chap_{i}.xhtml', lang='hr')
    chapters[f"c{i}"].content = bytes(title_html, "utf-8") + chapter_content

    # add chapter
    book.add_item(chapters[f"c{i}"])
    toc_entry = epub.Link(chapters[f"c{i}"].file_name, chapter_title, chapters[f"c{i}"].id)
    TOC.append(toc_entry)
    print(f'chapter {i} ready')


# define CSS style
style = DEFAULT_STYLE # pylint:disable=invalid-name
nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style) # pylint:disable=line-too-long

# add CSS file
book.add_item(nav_css)

spine = ['nav']
for i in chapters.values():
    spine.append(i)

# basic spine
book.spine = spine
book.toc = tuple(TOC)

# add default NCX and Nav file
book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())

epub.write_epub(FILE_TITLE, book, {})