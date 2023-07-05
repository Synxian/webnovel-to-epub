# Class

## parameters

1. title: The title of the book
1. starting_chapter_link: The link to the first chapter to scrap
1. starting_chapter_number: The number of the first chapter in the epub, not necessarilly 1
1. ending_chapter_number: The last chapter of the epub (ending_chapter >= starting_chapter)
1. file_title: The file name (please don't add .epub)
1. content_class: A list with the html tag/tags where the text is contained. Mostly you'll find nested tags to reach the content, in this cases the parents come before the child nodes in the list.
1. chapter_title_function: A function to obtain the title of the chapter, ideally soup.
1. sanitizing_function: A function to clean extra content from the main body, like the link to the next chapter, patreon image, etc.
1. language: The language of the book, completely optional, just use 'en' if you feel like it.
1. author: List with the author or authors of the text.
1. cover_link: Link to the desired cover image.
1. style: the css for the epub, default css from the yumemiru danshi epubs by PT Scans
1. add_images: Bool (default False), set to True if you want to add paragraph embeded images
1. extra_funcs: List with additional (in_place) functions for content cleansing
1. next_chapter_function: Function with the method to obtain the next chapter link, almost always is the same (refer to any example but sdsln) -almost-

For more information about language parameter refer to: http://www.ietf.org/rfc/rfc4646.txt

# Usage

You'll have to inspect the page to find the html tags, the rest is pretty straight forward, just define sanitize, get_title and next_chapter_function.
In the examples folder you'll find some ready-to-use scrappers for a few famous pages