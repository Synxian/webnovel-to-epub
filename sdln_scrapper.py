import requests
from bs4 import BeautifulSoup
from ebooklib import epub
import re
from constants import DEFAULT_STYLE
#============================================variables=============================================#
TITLE = 'I was said to be incompetent at home, but it seems that I was super-competent globally - volume 01' #book title
chapter = 'https://sdslntranslations.blogspot.com/2020/04/chapterstory-1-thus-i-left-home-yet.html' #first chapter link # pylint:disable=invalid-name
TOTAL_CHAPTERS = 3 #total chapters (use final chap+1)
FILE_TITLE = 'placeholder.epub' #title of the resulting epub
CONTENT_CLASS = ['post-body-container', 'post-body entry-content float-container'] #div where the reading content is at, if chapter title is included, remove the following lines # pylint:disable=line-too-long
TOC = []
#==================================================================================================#

def sanitize_content(content):
    for i in content.find_all('div', style='text-align: center;'):
        i.decompose()
    for i in content.find_all('span'):
        i.decompose()
    # import pdb; pdb.set_trace()

def next_chapter(content):
    for i in content.find_all('a'):
        if re.search(r'(next|Next)', i.get_text()):
            return i['href']
     
book = epub.EpubBook()

chapters={}

book.set_title(TITLE)

for i in range(1,TOTAL_CHAPTERS):
    response = requests.get(chapter)
    soup = BeautifulSoup(response.content, "html.parser")

    chapter_content = soup.find("div", class_=CONTENT_CLASS[0]).find("div", class_=CONTENT_CLASS[1]) #div where the reading content is at, if chapter title is included, remove the following lines # pylint:disable=line-too-long
    chapter = next_chapter(chapter_content) #function to find next chapter url
    # sanitize_content(chapter_content)
    chapter_title = soup.title.string #function to find chapter title
    title_html = "<h1>"+chapter_title+"</h1>"
    chapter_content = chapter_content.renderContents()
    chapters[f"c{i}"] = epub.EpubHtml(title=chapter_title, file_name=f'chap_{i}.xhtml', lang='hr')
    chapters[f"c{i}"].content = bytes(title_html, "utf-8")+chapter_content

    # add chapter
    book.add_item(chapters[f"c{i}"])
    toc_entry = epub.Link(chapters[f"c{i}"].file_name, chapter_title, chapters[f"c{i}"].id)
    TOC.append(toc_entry)
    print(f'chapter {i} ready')


# add default NCX and Nav file
book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())

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

epub.write_epub(FILE_TITLE, book, {})