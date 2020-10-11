from django import forms
import datetime
from .models import Book, Author, IndustryIdentifiers


class BookForm(forms.ModelForm):
    title = forms.CharField(max_length=200, label='title')
    authors = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=Author.objects.all(),
        required=True
    )
    cur_year = datetime.datetime.today().year
    year_range = tuple([i for i in range(cur_year, 0, -1)])
    released = forms.DateField(widget=forms.SelectDateWidget(years=year_range), label='release date')
    pageCount = forms.IntegerField(label='page count')
    language = forms.CharField(max_length=100, label='language')
    identifiers = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=IndustryIdentifiers.objects.all(),
        required=True
    )
    imageLink = forms.URLField(label='Image Link', initial='http://')

    class Meta:
        model = Book
        fields = ('title', 'authors', 'released', 'pageCount', 'language', 'identifiers', 'imageLink',)


class AuthorForm(forms.ModelForm):
    name = forms.CharField(max_length=200, label='name', required=True)

    class Meta:
        model = Author
        fields = ('name',)


class IdentifiersForm(forms.ModelForm):
    type = forms.CharField(max_length=200, label='type', required=True)
    identifier = forms.CharField(max_length=200, label='identifier', required=True)

    class Meta:
        model = IndustryIdentifiers
        fields = ('type', 'identifier',)


class SearchBookForm(forms.Form):
    keyword = forms.CharField()
