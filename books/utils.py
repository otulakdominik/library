from typing import Union

from .models import (
    Book,
    Author,
    IndustryIdentifiers,
)

import re
import requests
import datetime



def fetch_book(title: str) -> Union[None, dict]:
    google_books = requests.get(url='https://www.googleapis.com/books/v1/volumes?q={title}'.format(title=title,))
    books_json = google_books.json()
    bookshelf = books_json['items']

    for book in bookshelf:
        if 'imageLinks' in book['volumeInfo']:
            links = book['volumeInfo']['imageLinks']
        else:
            links['thumbnail'] = 'http://none'

        if 'publishedDate' in book['volumeInfo']:
            date = book['volumeInfo']['publishedDate']

            m = re.match(r'(\d\d\d\d)(?:-(\d\d)-(\d\d))?', date)
            m = m.groups('1')
            fulldate = datetime.date(int(m[0]), int(m[1]), int(m[2]))
        else:
            fulldate = '1111-01-01'
        author_ex = True
        id_authors = []
        if 'authors' in book['volumeInfo']:
            for author in book['volumeInfo']['authors']:
                obj, _ = Author.objects.get_or_create(
                    name=author
                )
                id_authors.append(obj)
        else:
            author_ex = False

        id_identifiers = []

        for identifiers in book['volumeInfo']['industryIdentifiers']:
            obj, _ = IndustryIdentifiers.objects.get_or_create(
                type=identifiers['type'],
                identifier=identifiers['identifier'],
            )
            id_identifiers.append(obj)

        if 'pageCount' not in book['volumeInfo']:
            book['volumeInfo']['pageCount'] = 0

        if 'language' not in book['volumeInfo']:
            book['volumeInfo']['language'] = 'none'

        book, _ = Book.objects.get_or_create(
            title=book['volumeInfo']['title'],
            released=fulldate,
            language=book['volumeInfo']['language'],
            pageCount=book['volumeInfo']['pageCount'],
            imageLink=links['thumbnail']
        )
        if author_ex == True:
            book.authors.set(id_authors)
        book.identifiers.set(id_identifiers)
        book.save()


