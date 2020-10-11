from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views import View
from django.db.models import Q
from .models import (
    Book,
    Author,
    IndustryIdentifiers,
)
from .forms import (
    BookForm,
    AuthorForm,
    IdentifiersForm,
    SearchBookForm,
)

import re
import requests
import datetime


class BookListView(ListView):
    model = Book
    template_name = 'books/list.html'
    context_object_name = 'books'
    paginate_by = 10


class BookCreateView(CreateView):
    model = Book
    template_name = 'books/create.html'
    form_class = BookForm
    success_url = 'list'


class BookUpdateView(UpdateView):
    model = Book
    template_name = 'books/edit.html'
    fields = [
        'title',
        'released',
        'pageCount',
        'language',
        'imageLink',
        'authors',
        'identifiers',
    ]

    def get_success_url(self):
        return reverse('books:list')


class BookDeleteView(DeleteView):
    model = Book
    success_url = 'list'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('books:list')


class AuthorCreateView(CreateView):
    model = Author
    template_name = 'books/author.html'
    form_class = AuthorForm
    success_url = 'create'


class IdentifiersCreateView(CreateView):
    model = IndustryIdentifiers
    template_name = 'books/identifiers.html'
    form_class = IdentifiersForm
    success_url = 'create'


class SearchResultsView(ListView):
    model = Book
    template_name = 'books/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Book.objects.filter(
            Q(title__icontains=query) | Q(language__icontains=query) | Q(authors__name__icontains=query)
        )

        return object_list


class DataSearchResultsView(ListView):
    model = Book
    template_name = 'books/search_results.html'

    def get_queryset(self):
        start = self.request.GET.get('s')
        end = self.request.GET.get('e')
        object_list = Book.objects.filter(released__range=[start, end])

        return object_list


class BookSearchApiGoogle(View):
    form_class = SearchBookForm
    template_name = 'books/search_api.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def search(self, value):
        params = {'q': value}
        google_books = requests.get(url="https://www.googleapis.com/books/v1/volumes", params=params)
        books_json = google_books.json()
        bookshelf = books_json['items']
        return bookshelf

    def add_book_to_library(self, bookshelf):

        for book in bookshelf:
            if 'imageLinks' in  book['volumeInfo']:
                links = book['volumeInfo']['imageLinks']
            else:
                links['thumbnail'] = 'http://none'

            if 'publishedDate' in book['volumeInfo']:
                date = book['volumeInfo']['publishedDate']

                m = re.match(r'(\d\d\d\d)(?:-(\d\d)-(\d\d))?', date)
                m = m.groups('1')
                fulldate = datetime.date(int(m[0]), int(m[1]), int(m[2]))
            else:
                fulldate = '01-01-01'
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
            if author_ex==True:
                book.authors.set(id_authors)
            book.identifiers.set(id_identifiers)
            book.save()

    def post(self, request, *args, **kwargs):
        form = self.form_class(self.request.POST)
        if form.is_valid():
            keyword = form.cleaned_data['keyword']
            books = self.search(keyword)
            self.add_book_to_library(books)
            return HttpResponseRedirect(reverse_lazy('books:list'))

        return reverse_lazy('search_api')