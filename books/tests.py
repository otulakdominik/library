from django.test import TestCase
from django.urls import reverse

from .models import (
    Book,
    Author,
    IndustryIdentifiers,
)

import datetime


class BookTest(TestCase):

    def setUp(self):
        self.author1 = Author.objects.create(
            name='Gustaw',
        )
        self.identifier1 = IndustryIdentifiers.objects.create(
            type='IG',
            identifier='421321',
        )

        self.book1 = Book.objects.create(
            name='Hobbit',
            released=datetime.date(1994, 6, 23),
            pageCount=234,
            language='pl',
            imageLink='https://hobbit',
            authors=author1,
            identifiers=identifier1
        )

        self.book2 = Book.objects.create(
            name='Wladca',
            released=date(2001, 2, 21),
            pageCount=134,
            language='an',
            imageLink='https://wladca',
            authors=author1,
            identifiers=identifier1
        )

        def test_view_url_exists(self):
            response = self.client.get('/book/list/')
            self.assertEqual(response.status_code, 200)

        def test_view_url_accessible_by_name(self):
            response = self.client.get(reverse('books:list'))
            self.assertEqual(response.status_code, 200)

        def test_view_uses_correct_template(self):
            response = self.client.get(reverse('authors'))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'books/list.html')