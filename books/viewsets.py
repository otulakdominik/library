import django_filters.rest_framework
from rest_framework.filters import OrderingFilter
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import BookSerializer, BookSearchSerializer
from .models import Book
from .filters import BookFilter
from .utils import fetch_book


class BookViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, OrderingFilter,]
    filterset_class = BookFilter
    ordering_fields = ('publishedDate',)

    def post(self, request, *args, **kwargs):
        serializer = BookSearchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        book_data = fetch_book(serializer.data.get('title'))
        return Response(book_data)
