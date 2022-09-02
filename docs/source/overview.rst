.. _overview:


Getting Started
*******************************************************************************

.. contents::
   :local:

Basic Example of Usage
===============================================================================

Models sample (`models.py`)::

    from django.db import models

    class Author(models.Model):
        name = models.CharField(max_length=255)

    class Book(models.Model):
        name = models.CharField(max_length=255)
        authors = models.ManyToManyField(Author)

        @staticmethod
        def search_by_author(author_name):
            return Book.objects.filter(authors__name=author_name)


**PyTest** example (`tests/test_books.py`)::

    from ddf import G

    def test_search_book_by_author():
        author1 = G(Author)
        author2 = G(Author)
        book1 = G(Book, authors=[author1])
        book2 = G(Book, authors=[author2])
        books = Book.objects.search_by_author(author1.name)
        assert book1 in books
        assert book2 not in books

**Django TestCase** example (`tests/test_books.py`)::

    from django.test import TestCase
    from ddf import G

    class SearchingBooks(TestCase):
        def test_search_book_by_author(self):
            author1 = G(Author)
            author2 = G(Author)
            book1 = G(Book, authors=[author1])
            book2 = G(Book, authors=[author2])
            books = Book.objects.search_by_author(author1.name)
            self.assertTrue(book1 in books)
            self.assertTrue(book2 not in books)


Installation
===============================================================================

::

    pip install django-dynamic-fixture

or::

    1. Download zip file
    2. Extract it
    3. Execute in the extracted directory: python setup.py install

Development version
-------------------------------------------------------------------------------

::

    pip install -e git+git@github.com:paulocheque/django-dynamic-fixture.git#egg=django-dynamic-fixture


requirements.txt
-------------------------------------------------------------------------------

::

    django-dynamic-fixture==<VERSION>
    # or use the development version
    git+git://github.com/paulocheque/django-dynamic-fixture.git#egg=django-dynamic-fixture


Upgrade
-------------------------------------------------------------------------------

::

    pip install django-dynamic-fixture --upgrade --no-deps


Support and Compatibility
===============================================================================

+---------------------------------------------------------+
| DDF current support                                     |
+================+=================+======================+
| Python 3.8     | Django 3.x.x    | DDF 3.*.* - Jan 2020 |
+----------------+-----------------+----------------------+
| Python 3.7     | Django 3.x.x    | DDF 3.*.* - Jan 2020 |
+----------------+-----------------+----------------------+
| Python 3.6     | Django 3.x.x    | DDF 3.*.* - Jan 2020 |
+----------------+-----------------+----------------------+
| Python > 3.5   | Django 2.x.x    | DDF 3.*.* - Jan 2020 |
+----------------+-----------------+----------------------+
| Python 2.7     | Django 1.11.x   | DDF 3.*.* - Jan 2020 |
+----------------+-----------------+----------------------+

+---------------------------------------------------------+
| DDF old support                                         |
+================+=================+======================+
| Python 3.3     | Django < 1.11.x | DDF 2.0.* - Dec 2017 |
+----------------+-----------------+----------------------+
| Python <= 2.7  | Django < 1.11.x | DDF 2.0.* - Dec 2017 |
+----------------+-----------------+----------------------+


List of features
===============================================================================

  * Highly customizable: you can **customize fields recursively**
  * Deals with **unique=True**
  * Deals with **cyclic dependencies** (including self references)
  * Deals with **many to many relationship** (common M2M or M2M with additional data, i.e. **through='table'**)
  * Deals with **custom fields** (especially if the custom field inherits from a django field)
  * Support for **parallel tests**
  * Deals with **auto calculated** attributes
  * It is **easy to debug errors**

Motivation
===============================================================================

  * It is a terrible practice to use **static data** in tests (yml/json/sql files).
  * It is very hard to maintain lots of **Factory objects**.
  * Creating fixtures for each model is boring and it produces a lot of **replicated code**.
  * It is a bad idea to use uncontrolled data in tests, like bizarre random data.

Comparison with other tools
===============================================================================

The DDF was created in a context of a project with a **very complex design** with many **cyclic dependencies**. In that context, no available tool was satisfactory. Or we stumbled in some **infinite loop** or some bug caused by a **custom field**. For these reasons, the tests started to fail and it was very hard to understand why.

Another thing, the DDF was planned to have a **lean and clean syntax**. We believe that automated tests must be developed quickly with the **minimum overhead**. For that reason we are in favor of **less verbose approach**, except in the documentation ;)

Also, DDF is flexible, since it is possible to customize the entire data generation or by field.

  * Either they are incomplete, or bugged or it produces erratic tests, because they use random and uncontrolled data.
  * The syntax of others tools is too verbose, which pollutes the tests.
  * Complete, lean and practice documentation.
  * It is hard to debug tests with another tools.
  * List of other tools: <https://www.djangopackages.com/grids/g/testing/> or <http://djangopackages.com/grids/g/fixtures>
  * The core of the tool is the algorithm, it is not the data generation as all other tools. This means you can change the data generation logic.

Plus:

  * **PyTest** compatible
  * **Nose plugin** that enables a setup for the entire suite (unittest2 includes only setups for class and module)
  * **Nose plugin** to count how many queries are executed by test
  * **Command** to count how many queries are executed to save any kind of model instance
  * **FileSystemDjangoTestCase** that facilitates to create tests for features that use filesystem.
