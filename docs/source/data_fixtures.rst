.. _data_fixtures:

Data Fixtures
*******************************************************************************

This configuration defines the algorithm of data generation that will be used to populate fields with dynamic data. Do NOT mix data fixtures in the same test suite because the generated data may conflict and it will produce erratic tests.

In settings.py::

    DDF_DEFAULT_DATA_FIXTURE = 'sequential' # or 'static_sequential' or 'random' or 'path.to.your.DataFixtureClass'

Overriding global data fixture
===============================================================================

This algorithm will be used just for the current model generation.

In the test file or shell::

    G(MyModel, data_fixture='sequential')
    G(MyModel, data_fixture='random')
    G(MyModel, data_fixture=MyCustomDataFixture())

Sequential Data Fixture
===============================================================================

Useful to use in test suites. Sequential Data Fixture stores an independent counter for each model field that is incremented every time this field has to be populated. If for some reason the field has some restriction (*max_length*, *max_digits* etc), the counter restarts. This counter is used to populate fields of numbers (*Integer*, *BigDecimal* etc) and strings (*CharField*, *TextField* etc). For *BooleanFields*, it will always return False. For *NullBooleanFields*, it will always return None. For date and time fields, it will always return Today minus 'counter' days or Now minus 'counter' seconds, respectively.

In settings.py::

    DDF_DEFAULT_DATA_FIXTURE = 'sequential'

In the test file::

    instance = G(MyModel)
    assert instance.integerfield_a == 1
    assert instance.integerfield_b == 1
    assert instance.charfield_b == 1
    assert instance.booleanfield == False
    assert instance.nullbooleanfield is None

    instance = G(MyModel)
    assert instance.integerfield_a == 2
    assert instance.integerfield_b == 2
    assert instance.charfield_b == 2
    assert instance.booleanfield == False
    assert instance.nullbooleanfield is None

    instance = G(MyOtherModel)
    assert instance.integerfield_a == 1

    # ...

Static Sequential Data Fixture
===============================================================================

Useful to use in test suites. Static Sequential Data Fixture is the same as Sequential Data Fixture, except it will increase the counter only if the field has *unique=True*.

In settings.py::

    DDF_DEFAULT_DATA_FIXTURE = 'static_sequential'

In the test file::

    instance = G(MyModel)
    assert instance.integerfield_unique == 1
    assert instance.integerfield_notunique == 2

    instance = G(MyModel)
    assert instance.integerfield_unique == 2
    assert instance.integerfield_notunique == 2
    # ...

Random Data Fixture
===============================================================================

Useful to use in python shells. In shell you may want to do some manual tests, and DDF may help you to generate models too. If you are using shell with a not-in-memory database, you may have problems with *SequentialDataFixture* because the sequence will be reset every time you close the shell, but the data already generated is persisted.

It is dangerous to use this data fixture in a test suite because it can produce erratic tests. For example, depending on the quantity of tests and *max_length* of a *CharField*, there is a high probability to generate an identical value which will result in invalid data for fields with *unique=True*.

In settings.py::

    DDF_DEFAULT_DATA_FIXTURE = 'random'

In the test file::

    instance = G(MyModel)
    assert instance.integerfield_a is not None
    assert instance.charfield_b is not None
    assert instance.booleanfield in [False, True]
    assert instance.nullbooleanfield in [None, False, True]
    # ...

Custom Data Fixture
===============================================================================

In settings.py::

    DDF_DEFAULT_DATA_FIXTURE = 'path.to.your.DataFixtureClass'

In the path/to/your.py file::

    from django_dynamic_fixture.ddf import DataFixture
    class DataFixtureClass(DataFixture): # it can inherit of SequentialDataFixture, RandomDataFixture etc.
        def integerfield_config(self, field, key): # method name must have the format: FIELDNAME_config
            return 1000 # it will always return 1000 for all IntegerField

In the test file::

    instance = G(MyModel)
    assert instance.integerfield_a == 1000
    assert instance.integerfield_b == 1000
    # ...


Custom Field Fixture
===============================================================================

You can also override a field default fixture or even create a fixture for a new field using the **DDF_FIELD_FIXTURES** settings in ``settings.py``::

    # https://github.com/bradjasper/django-jsonfield
    import json
    DDF_FIELD_FIXTURES = {
        'jsonfield.fields.JSONCharField': {'ddf_fixture': lambda: json.dumps({'some random value': 'c'})},
        'jsonfield.fields.JSONField': {'ddf_fixture': lambda: json.dumps([1, 2, 3])},
    }
