from django.contrib import admin

from .models import(
    Book,
    Author,
    IndustryIdentifiers,
)


class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )


class IdustryIdentifiersAdmin(admin.ModelAdmin):
    list_display = (
        'type',
        'identifier',
    )


class BookAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'released',
        'pageCount',
        'language',
        'imageLink',
    )
    filter_horizontal = ('authors','identifiers',)


admin.site.register(Author, AuthorAdmin)
admin.site.register(IndustryIdentifiers, IdustryIdentifiersAdmin)
admin.site.register(Book, BookAdmin)
