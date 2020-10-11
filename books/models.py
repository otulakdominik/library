from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


class Author(models.Model):
    name = models.CharField(
        _('author'),
        max_length=300,
    )

    class Meta:
        verbose_name = _('author')
        verbose_name_plural = _('authors')

    def __str__(self):
        return self.name


class IndustryIdentifiers(models.Model):
    type = models.CharField(
        _('type'),
        max_length=200,
    )

    identifier = models.CharField(
        _('identifier'),
        max_length=200,
    )

    class Meta:
        verbose_name = _('identifier')
        verbose_name_plural = _('indetifiers')

    def __str__(self):
        return self.type + ' ' + self.identifier


class Book(models.Model):
    title = models.CharField(
        _('title'),
        max_length=200,
    )

    released = models.DateField(
        _('release date'),
    )

    pageCount = models.SmallIntegerField(
        _('page count'),
        blank=True,
    )

    language = models.CharField(
        _('language'),
        max_length=100,
        blank=True,
    )

    imageLink = models.URLField(
        _('image link'),
        max_length=300,
        blank=True,
    )

    authors = models.ManyToManyField(Author)
    identifiers = models.ManyToManyField(IndustryIdentifiers)

    class Meta:
        verbose_name = _('book')
        verbose_name_plural = _('books')

    def get_absolute_url(self):
        return reverse('book-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title
