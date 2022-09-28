import requests
from bs4 import BeautifulSoup
from ebooklib import epub

#============================================variables=============================================#
TITLE = 'placeholder' #book title
chapter = 'placeholder' #first chapter link # pylint:disable=invalid-name
TOTAL_CHAPTERS = 111 #total chapters
FILE_TITLE = 'placeholder' #title of the resulting epub
CONTENT_CLASS = 'placeholder' #div where the reading content is at, if chapter title is included, remove the following lines # pylint:disable=line-too-long
#==================================================================================================#


book = epub.EpubBook()

chapters={}

book.set_title(TITLE)

for i in range(1,TOTAL_CHAPTERS):
    response = requests.get(chapter)
    soup = BeautifulSoup(response.content, "html.parser")

    chapter_content = soup.find("div", class_=CONTENT_CLASS) #div where the reading content is at, if chapter title is included, remove the following lines # pylint:disable=line-too-long
    chapter_title = '' #function to find chapter title
    chapter_title = "<h1>"+chapter_title+"</h1>"
    chapter_content = chapter_content.renderContents()
    chapters[f"c{i}"] = epub.EpubHtml(title=chapter_title, file_name=f'chap_{i}.xhtml', lang='hr')
    chapters[f"c{i}"].content = bytes(chapter_title, "utf-8")+chapter_content

    # add chapter
    book.add_item(chapters[f"c{i}"])
    chapter = '' #function to find next chapter url
    print(f'chapter {i} ready')


# add default NCX and Nav file
book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())

# define CSS style
style = 'BODY {color: white;}' # pylint:disable=invalid-name
nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style) # pylint:disable=line-too-long

# add CSS file
book.add_item(nav_css)

spine = ['nav']
for i in chapters.items():
    spine.append(i)

# basic spine
book.spine = spine

epub.write_epub(FILE_TITLE, book, {})