from rest_framework import serializers
from .models import Book, Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'name')


class BookSearchSerializer(serializers.Serializer):
    title = serializers.CharField()


class BookSerializer(serializers.ModelSerializer):
    authors = serializers.StringRelatedField(many=True)
    identifiers = serializers.StringRelatedField(many=True)

    class Meta:
        model = Book
        fields = (
            'title',
            'authors',
            'released',
            'pageCount',
            'language',
            'identifiers',
            'imageLink',
        )
