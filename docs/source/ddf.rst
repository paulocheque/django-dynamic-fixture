.. _ddf:

Core DDF features
*******************************************************************************

.. contents::
   :local:

Get: G
===============================================================================

The ``G`` function (shortcut for the ``get`` function) is the main feature of DDF. It is useful for integration tests, for the model logic and queries to the database.

It receives a model class and it will return a **valid and persisted instance** filled with dynamically generated data::


    from ddf import G # or from ddf import get
    author = G(Author)
    assert author.id is not None # indicating the instance was saved
    assert author.name is not None # indicating a name was generated for you
    assert len(author.name) > 0


This facilitates writing tests and it hides all dummy data that pollutes the source code. But all **important data of the test may be explicitly defined**. This is even a good practice, because it let the test very clear and cohesive::


    book = G(Book, name='The Lord of the Rings', publish_date=date(1954, 07, 29))
    assert book.name == 'The Lord of the Rings'
    assert book.publish_date == date(1954, 07, 29)


Important details:

* The **id** (AutoField) is auto filled, unless you set a value to it.
* if a field has **default value**, it is used by default. Unless you override it.
* if a field has **choices**, the first option is selected by default. Unless you override it.


New: N
===============================================================================

This function ``N`` (shortcut to ``new``) is similar to ``G``, except it will NOT save the generated instance. This is good for **unit tests**, without touching the database::

    from ddf import N
    not_saved_book = N(Book)
    assert not_saved_book.id is None # indicating the instance was NOT saved
    assert not_saved_book.name is not None # indicating a name was generated for you

It can also be usefuf to **manipulate the instance before saving it**. Usually, we need that to deal with custom fields, custom validations etc. For these cases, we can use the ``persist_dependencies=True`` parameter to save internal dependencies of ``ForeignKey`` and ``OneToOneField`` fields::

    book = N(Book, persist_dependencies=True)
    assert book.id is None # the Book was not persisted
    assert book.publisher.id is not None # internal dependency was persisted

ps: Since the instance does not have an ID, it can NOT insert instances in ``ManyToManyField`` fields. So, be aware to use the ``G`` function for these cases.

Fixture: F
===============================================================================

DDF also allows you **customise recursively through relationship fields** ``ForeignKey``, ``OneToOneField`` and ``ManyToManyField``) using the ``F`` function (shortcut for ``fixture``).

ForeignKey and OneToOneField
-------------------------------------------------------------------------------

To customise relationships, you can use the ``F`` function or the Django look up syntax::

    from ddf import G, F
    book = G(Book, author=F(name='Eistein'))
    # or, even simpler, using the Django loop up syntax:
    book = G(Book, author__name='Eistein')
    assert book.author.name == 'Eistein'

This is the equivalent to::

    author = G(Author, name='Eistein')
    book = G(Book, author=author)
    assert book.author.name == 'Eistein'

``F`` function is recursible::

    book = G(Book, author=F(address=F(zipcode='123456789')))
    # or, even simpler, using the Django loop up syntax:
    book = G(Book, author__address__zipcode='123456789')
    assert book.author.address.zipcode == '123456789'

``F`` can be used to customize instances of a ``ManyToManyField`` too::

    book = G(Book, authors=[F(name='Eistein'), F(name='Tesla')])
    assert book.authors.all()[0].name == 'Eistein'
    assert book.authors.all()[1].name == 'Tesla'


Django Look Up fields syntax (New in 1.6.1) (Fixed in 3.0.0)
-------------------------------------------------------------------------------

This is an alias to ``F`` function, and it follows the Django pattern of filters that use two underlines to access internal fields of foreign keys. You can **combine** multiple parameters to create a complete customisable instance.

ps: Just be careful because DDF does NOT interpret **related names** yet. It has also some limitation for many to many fields.


Many to Many fields
-------------------------------------------------------------------------------

DDF can add instances in ``ManyToManyFields``, but only if the instance has been persisted to the database (Django requirement). DDF handles ``ManyToManyFields`` with ``through`` table as well.

It is possible to define **how many instances** will be created dynamically::

    book = G(Book, authors=5)
    assert book.authors.all().count() == 5

It is possible to customize each instance of the ``ManyToManyField``::

    book = G(Book, authors=[F(name='Eistein'), F(address__zipcode='123456789')])
    assert book.authors.all().count() == 2
    assert instance.authors.all()[0].name == 'Eistein'
    assert instance.authors.all()[1].address.zipcode == '123456789'

It is possible to pass already created instances too::

    author1 = G(Author)
    author2 = G(Author)

    book = G(Book, authors=[author1, author2])
    assert book.authors.all().count() == 2

Or even mixed them up::

    book = G(Book, authors=[F(), author1, F(), author2])
    assert book.authors.all().count() == 4


Mask: M (New in 3.1.0)
===============================================================================

``M`` (shortcut for ``Mask``) is a feature that tell DDF to generate a random string using a custom mask.

The mask symbols are:

- ``#``: represents a number: 0-9
- ``-``: represents a upper case char: A-Z
- ``_``: represents a lower case char: a-z
- ``!``: escape mask symbols, inclusive itself

Examples::

    from ddf import G, M
    instance = G(Publisher, address=M(r'St. -______, ### !- -- --'))
    assert instance.address == 'St. Imaiden, 164 - SP BR'


Copier: C (New in 1.6.0)
===============================================================================

``C`` (shortcut for ``Copier``) is a feature to copy the data of a field to another one. It is necessary to avoid cycles in the copier expression. If a cycle is found, DDF will alert the programmer the expression is invalid::

    from ddf import G, C
    user = G(User, first_name=C('username'))
    assert instance.first_name == instance.username

    instance = G(MyModel, first_name=C('username'), username='eistein')
    assert instance.first_name == 'eistein'

It is possible to copy values of internal relationships, but only in the **bottom-up way**::

    person = G(Person, phone=C('parent.phone'))
    assert person.phone == person.parent.phone


Teaching DDF with Lessons (shelve in 2.1.0) (New in 3.0.0)
===============================================================================

Sometimes DDF can not generate a valid and persisted instance because it contains custom fields or custom validations (field or model validation). In these cases, it is possible to **teach DDF how to build a valid instance**. It is necessary to create a valid configuration and save it in an internal and global DDF library of configurations. All future instances of that model will use the saved lesson as base.

In the **PyTest** **conftest.py** file or another global module that will be loaded before the test suite::

    from ddf import teach
    teach(Author, name='Eistein')
    # After this command, all authors will have the name Eistein, unless it was overrided.

In the test files::

    from ddf import G
    author = G(Author)
    assert author.name == 'Eistein'


It is possible to **override** the lessons though::

    author = G(Author, name='Tesla')
    assert author.name == 'Tesla'

It is possible to store **custom functions** of data fixtures for fields too::

    zip_code_data_fixture = lambda field: 'MN {}'.format(random.randint())
    teach(Address, zip_code=zip_code_data_fixture)

    address = G(Address)
    assert address.zip_code == 'MN 55416'

It is possible to store **Copiers** too::

    teach(Author, first_name=C('username'))

    author = G(Author, username='eistein')
    assert instance.username == 'eistein'
    assert instance.first_name == 'eistein'

It is also possible to save custom lessons that will override the default one. But avoid having too many of them, since this will became the test suite very complex.

You can have **many custom lessons** too, giving names to them::

    from ddf import teach
    teach(Model, field_x=77)
    teach(Model, field_x=88, ddf_lesson='my custom lesson 1')
    teach(Model, field_x=99, ddf_lesson='my custom lesson 2')

    instance = G(Model)
    assert instance.field_x == 77

    instance = G(Model, ddf_lesson='my custom lesson 1')
    assert instance.field_x == 88

    instance = G(Model, ddf_lesson='my custom lesson 2')
    assert instance.field_x == 99

ps: Just be aware that overriding lessons is an anti-pattern and may let your test suite very hard to understand.
