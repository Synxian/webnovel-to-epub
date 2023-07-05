import re
import requests
from bs4 import BeautifulSoup
from ebooklib import epub
from constants import DEFAULT_STYLE

class EpubScrapper:
    def __init__(self, title, starting_chapter_link, starting_chapter_number:int,
                  ending_chapter_number:int, file_name, content_class:list,
                  chapter_title_function, sanitizing_function, language=None, author:list=None,
                  cover_link=None, style=DEFAULT_STYLE, add_images=False, extra_funcs:list=None):
        self.title = title
        self.starting_chapter_number = starting_chapter_number
        self.ending_chapter_number = ending_chapter_number
        self.file_name = f'{file_name}.epub'
        self.content_class = content_class
        self.table_of_contents = []
        self.chapters = {}
        self.language = language
        self.author = author
        self.cover_link = cover_link
        self.chapter_title_function = chapter_title_function
        self.sanitizing_function = sanitizing_function
        self.add_images = add_images
        self.extra_funcs = extra_funcs
        self.book = epub.EpubBook()

        self.initialize_epub()
        self.scrap(starting_chapter_link)


        nav_css = epub.EpubItem(
            uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style,
        )

        # add CSS file
        self.book.add_item(nav_css)

        spine = ['nav']
        for i in self.chapters.values():
            spine.append(i)

        # basic spine
        self.book.spine = spine
        self.book.toc = tuple(self.table_of_contents)

        # add default NCX and Nav file
        self.book.add_item(epub.EpubNcx())
        self.book.add_item(epub.EpubNav())
        epub.write_epub(self.file_name, self.book, {})

    def initialize_epub(self):
        self.book.set_title(self.title)
        self.book.set_identifier(
            f'{self.title}{self.starting_chapter_number}to{self.ending_chapter_number}'
        )
        if self.language:
            self.book.set_language(self.language)
        if self.author:
            for i in self.author:
                self.book.add_author(i)
        if self.cover_link:
            self.add_cover(self.cover_link)

    def add_cover(self, link):
        cover = None
        self.book.set_cover('cover.jpg', cover)

    def scrap(self, chapter):
        for i in range(self.starting_chapter_number, self.ending_chapter_number+1):
            response = requests.get(chapter, timeout=5)
            soup = BeautifulSoup(response.content, "html.parser")
            chapter_content = self.get_chapter_content(soup)
            next_chapter = self.next_chapter(chapter_content)
            self.sanitize_content(chapter_content)
            chapter_title = self.get_chapter_title(soup)
            if self.extra_funcs:
                for func in self.extra_funcs:
                    func(chapter_content)
            title_html = "<h1>"+chapter_title+"</h1>"
            chapter_content = chapter_content.renderContents()
            self.chapters[f"c{i}"] = epub.EpubHtml(
                title=chapter_title, file_name=f'chapter_{i}.xhtml', lang='hr'
            )
            self.chapters[f"c{i}"].content = bytes(title_html, "utf-8")+chapter_content
            self.book.add_item(self.chapters[f"c{i}"])
            toc_entry = epub.Link(
                self.chapters[f"c{i}"].file_name, chapter_title, self.chapters[f"c{i}"].id
            )
            self.table_of_contents.append(toc_entry)
            print(f'chapter {i} ready')
            chapter = next_chapter

    def get_chapter_content(self, soup):
        content = soup
        for i in self.content_class:
            content = content.find('div', i)
        return content

    def get_chapter_title(self, soup):
        return self.chapter_title_function(soup)

    def next_chapter(self, content):
        for i in content.find_all('a'):
            if re.search(r'(next|Next)', i.get_text()):
                return i['href']

    def sanitize_content(self, soup):
        self.sanitizing_function(soup)
