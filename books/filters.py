import django_filters
from django_filters import rest_framework as filters
from django_filters.widgets import RangeWidget

from .models import Book

class BookFilter(filters.FilterSet):
    title = filters.CharFilter()
    authors__name = filters.CharFilter()
    language = filters.CharFilter()
    date_between = django_filters.DateFromToRangeFilter(
        field_name='released',
        label='Date (Between)',
        widget=RangeWidget(attrs={'type': 'date'})
    )

    class Meta:
        model = Book
        fields = [
            'title',
            'authors__name',
            'language',
            'date_between',
        ]
