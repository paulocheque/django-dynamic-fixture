Django Dynamic Fixture
======================

[![Docs Status](https://readthedocs.org/projects/django-dynamic-fixture/badge/?version=latest)](http://django-dynamic-fixture.readthedocs.org/en/latest/index.html)
[![PyPI version](https://badge.fury.io/py/django-dynamic-fixture.svg)](https://badge.fury.io/py/django-dynamic-fixture)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-dynamic-fixture)
![PyPI - Downloads](https://img.shields.io/pypi/dm/django-dynamic-fixture)

**Latest version: 4.0.1 (Sep 2023)**

Django Dynamic Fixture (DDF) is a complete and simple library to create dynamic model instances for testing purposes.

It lets you focus on your tests, instead of focusing on generating some dummy data which is boring and polutes the test source code.

* [Basic Examples](#basic-examples)
* [Cheat Sheet](#cheat-sheet)
* <a href="http://django-dynamic-fixture.readthedocs.org/en/latest/index.html" target="_blank">Full Documentation</a>


Basic Examples
--------------

> Customize only the important details of the test:

```python
    from ddf import G
    from my_library import Author, Book

    def test_search_book_by_author():
        author1 = G(Author)
        author2 = G(Author)
        book1 = G(Book, authors=[author1])
        book2 = G(Book, authors=[author2])
        books = Book.objects.search_by_author(author1.name)
        assert book1 in books
        assert book2 not in books
```

> Using some goodies to keep the test code smaller:

```python
    from ddf import G

    def test_search_book_by_author():
        author1, author2 = G('my_library.Author', n=2)
        book1 = G('my_library.Book', authors=[author1])
        book2 = G('my_library.Book', authors=[author2])
        books = Book.objects.search_by_author(author1.name)
        assert book1 in books
        assert book2 not in books
```

> Configuring data from relationship fields:

```python
    from ddf import G

    def test_search_book_by_author():
        book1 = G(Book, main_author__name='Eistein')
        book2 = G(Book)
        books = Book.objects.search_by_author(book1.main_author.name)
        assert book1 in books
        assert book2 not in books
        assert book1.main_author.name == 'Eistein'
```

Cheat Sheet
--------------

```python
# Import the main DDF features
from ddf import N, G, F, M, C, P, teach # meaning: New, Get, ForeignKey, Mask, Copier, Print, teach
```

```python
# `N` creates an instance of model without saving it to DB
instance = N(Book)
```

```python
# `G` creates an instance of model and save it into the DB
instance = G(Book)
```

```python
# `F` customize relationship objects
instance = G(Book, author=F(name='Eistein'))
# Same as `F`
instance = G(Book, author__name='Eistein')
```

```python
# `M` receives a data mask and create a random string using it
# Known symbols: `_`, `#` or `-`
# To escape known symbols: `!`
instance = N(Book, address=M('Street ___, ### !- --'))
assert instance.address == 'Street TPA, 632 - BR'
```

```python
# `C` copies data from one field to another
instance = N(Book, address_formatted=C('address'), address=M('Street ___, ### \- --'))
assert instance.address_formatted == 'Street TPA, 632 - BR'
```

```python
# `teach` teaches DDF in how to build an instance
teach(Book, address=M('Street ___, ### !- --'))
instance = G(Book)
assert instance.address == 'Street TPA, 632 - BR'
```

```python
# `P` print instance values for debugging
P(instance)
```

```python
import ddf
ddf.__version__
```

```python
from ddf import ddf_check_models
succeeded, errors = ddf_check_models()
succeeded, errors = ddf_check_models(print_csv=True)
succeeded, errors = ddf_check_models(csv_filename='ddf_compatibility_report.csv')
```
