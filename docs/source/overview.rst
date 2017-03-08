.. _overview:

Getting Started
*******************************************************************************

Basic Example of Usage
===============================================================================

Models sample::

    from django.db import models

    class Author(models.Model):
        name = models.CharField(max_length=255)

    class Book(models.Model):
        name = models.CharField(max_length=255)
        authors = models.ManyToManyField(Author)

Test sample::

    from django.test import TestCase
    from django_dynamic_fixture import G

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


Compatibility
===============================================================================

* Legacy: Django 1.2, 1.3 - Python: 2.7

* Django 1.4 with Python 2.7
* Django 1.5 with Python 2.7
* Django 1.6 with Python 2.7 or 3.3

* Not tested with Django 1.7 yet

List of features
===============================================================================

  * Highly customizable: you can customize fields recursively
  * Deals with unique=True
  * Deals with cyclic dependencies (including self references)
  * Deals with many to many relationship (common M2M or M2M with additional data, i.e. through='table')
  * Deals with custom fields (especially if the custom field inherits from a django field)
  * Support for parallel tests
  * Deals with auto calculated attributes
  * It is easy to debug errors

Motivation
===============================================================================

  * It is a terrible practice to use static data in tests.
  * Creating dynamic fixture for each model is boring and it produces a lot of replicated code.
  * It is a bad idea to use uncontrolled data in tests, like bizarre random data.

Comparison with other tools
===============================================================================

The DDF was created in a context of a project with a very complex design with many cyclic dependencies. In that context, no available tool was satisfactory. Or we stumbled in some infinite loop or some bug caused by a custom field. For these reasons, the tests started to fail and it was very hard to understand why.

Another thing, the DDF was planned to have a lean and clean syntax. We believe that automated tests must be developed quickly with the minimum overhead. For that reason we are in favor of less verbose approach, except in the documentation ;)

Also, DDF is flexible, since it is possible to customize the entire data generation or by field.

  * Either they are incomplete, or bugged or it produces erratic tests, because they use random and uncontrolled data.
  * The syntax of others tools is too verbose, which polutes the tests.
  * Complete, lean and practice documentation.
  * It is hard to debug tests with another tools.
  * List of other tools: <https://www.djangopackages.com/grids/g/testing/> or <http://djangopackages.com/grids/g/fixtures>
  * The core of the tool is the algorithm, it is not the data generation as all other tools. This means you can change the data generation logic.

Plus:

  * Nose plugin that enables a setup for the entire suite (unittest2 includes only setups for class and module)
  * Nose plugin to count how many queries are executed by test
  * Command to count how many queries are executed to save any kind of model instance
  * FileSystemDjangoTestCase that facilitates to create tests for features that use filesystem.

External references
===============================================================================

  * http://stackoverflow.com/search?q=django+dynamic+fixture
  * http://stackoverflow.com/questions/12487337/optimizing-setup-and-teardown-for-sample-django-model-using-django-nose-and-djan
  * http://stackoverflow.com/questions/4400609/initial-data-fixture-management-in-django