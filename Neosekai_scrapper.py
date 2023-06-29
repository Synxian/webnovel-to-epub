import requests
from bs4 import BeautifulSoup
from ebooklib import epub

book = epub.EpubBook()

chapters={}

title = "Since I’ve Entered the World of Romantic Comedy Manga, I’ll Do My Best to Make the Heroine Who Doesn’t Stick With the Hero Happy - chapter 1 to 73"
book.set_title(title)
chapter = "https://www.neosekaitranslations.com/novel/since-ive-entered-the-world-of-romantic-comedy-manga-ill-do-my-best-to-make-the-heroine-who-doesnt-stick-with-the-hero-happy/chapter-1-reincarnating-as-a-manga-character/"


for i in range(1,74):
    response = requests.get(chapter)
    soup = BeautifulSoup(response.content, "html.parser")

    chapter_content = soup.find("div", class_='reading-content').find("div", class_='text-left')
    chapter_title = soup.title.string[soup.title.string.find('Chapter'):soup.title.string.find('NeoSekai')-3]
    chapter_title = "<h1>"+chapter_title+"</h1>"
    chapter_content = chapter_content.renderContents()
    chapters["c{0}".format(i)] = epub.EpubHtml(title=chapter_title, file_name='chap_{0}.xhtml'.format(i), lang='hr')
    chapters["c{0}".format(i)].content = bytes(chapter_title, "utf-8")+chapter_content

    # add chapter
    book.add_item(chapters["c{0}".format(i)])
    chapter = soup.find("div", class_='nav-next').find('a', href=True)['href']
    print('chapter {0} ready'.format(i))


# add default NCX and Nav file
book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())
# define CSS style
style = 'BODY {color: white;}'
nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
# add CSS file
book.add_item(nav_css)

spine = ['nav']
for i in chapters:
    spine.append(chapters[i])

# basic spine
book.spine = spine

epub.write_epub('romcom manga isekai.epub', book, {})