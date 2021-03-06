# Generated by Django 3.1 on 2020-10-10 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, verbose_name='author')),
            ],
            options={
                'verbose_name': 'author',
                'verbose_name_plural': 'authors',
            },
        ),
        migrations.CreateModel(
            name='IndustryIdentifiers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=200, verbose_name='type')),
                ('identifier', models.CharField(max_length=200, verbose_name='identifier')),
            ],
            options={
                'verbose_name': 'identifier',
                'verbose_name_plural': 'indetifiers',
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='title')),
                ('released', models.DateField(verbose_name='release date')),
                ('pageCount', models.SmallIntegerField(blank=True, verbose_name='page count')),
                ('language', models.CharField(blank=True, max_length=100, verbose_name='language')),
                ('imageLink', models.URLField(blank=True, max_length=300, verbose_name='image link')),
                ('authors', models.ManyToManyField(to='books.Author')),
                ('identifiers', models.ManyToManyField(to='books.IndustryIdentifiers')),
            ],
            options={
                'verbose_name': 'book',
                'verbose_name_plural': 'books',
            },
        ),
    ]
