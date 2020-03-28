from django.db import models


class Publisher(models.Model):
    name = models.CharField(max_length=100, unique=True)

class Author(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    parent = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True)

class Book(models.Model):
    isb = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    main_author = models.ForeignKey(Author, related_name='books', on_delete=models.DO_NOTHING)
    authors = models.ManyToManyField('Author', related_name='m2m')
    categories = models.ManyToManyField('Category', related_name='m2m')
    from .fields import JSONField
    metadata = JSONField(null=True)

class BookPublisher(models.Model):
    book_edition = models.ForeignKey('BookEdition', on_delete=models.DO_NOTHING)
    publisher = models.ForeignKey('Publisher', on_delete=models.DO_NOTHING)
    comments = models.TextField(max_length=100)

class BookEdition(models.Model):
    book = models.ForeignKey(Book, related_name='editions', on_delete=models.DO_NOTHING)
    publishers = models.ManyToManyField('Publisher', related_name='edition_publishers', through=BookPublisher)
    year = models.IntegerField()
