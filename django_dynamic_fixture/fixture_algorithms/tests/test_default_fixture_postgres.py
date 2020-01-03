# -*- coding: utf-8 -*-
from datetime import datetime
import six

from django.db import models
from django.test import TestCase

from django_dynamic_fixture.fixture_algorithms.default_fixture import PostgresFixtureMixin
from django_dynamic_fixture.fixture_algorithms.sequential_fixture import SequentialDataFixture, StaticSequentialDataFixture
from django_dynamic_fixture.fixture_algorithms.random_fixture import RandomDataFixture
from django_dynamic_fixture.fixture_algorithms.unique_random_fixture import UniqueRandomDataFixture

try:
    import psycopg2
    from django.contrib.postgres.fields import ArrayField

    class PostgresDataFixtureTestMixin(object):
        def test_arrayfield_integer_config(self):
            data = self.fixture.generate_data(ArrayField(models.IntegerField()))
            assert isinstance(data, list)
            assert isinstance(data[0], int)

        def test_arrayfield_char_config(self):
            data = self.fixture.generate_data(ArrayField(models.CharField()))
            assert isinstance(data, list)
            assert isinstance(data[0], six.text_type)

        def test_arrayfield_datetime_config(self):
            data = self.fixture.generate_data(ArrayField(models.DateTimeField()))
            assert isinstance(data, list)
            assert isinstance(data[0], datetime)

        def test_arrayfield_email_config(self):
            data = self.fixture.generate_data(ArrayField(models.EmailField(max_length=100)))
            assert isinstance(data, list)
            assert isinstance(data[0], six.text_type)


    class PostgresSequentialDataFixtureTestCase(TestCase, PostgresDataFixtureTestMixin):
        def setUp(self):
            class CustomFixture(SequentialDataFixture, PostgresFixtureMixin):
                pass
            self.fixture = CustomFixture()

    class PostgresStaticSequentialDataFixtureTestCase(TestCase, PostgresDataFixtureTestMixin):
        def setUp(self):
            class CustomFixture(StaticSequentialDataFixture, PostgresFixtureMixin):
                pass
            self.fixture = CustomFixture()

    class PostgresRandomDataFixtureTestCase(TestCase, PostgresDataFixtureTestMixin):
        def setUp(self):
            class CustomFixture(RandomDataFixture, PostgresFixtureMixin):
                pass
            self.fixture = CustomFixture()

    class PostgresUniqueRandomDataFixtureTestCase(TestCase, PostgresDataFixtureTestMixin):
        def setUp(self):
            class CustomFixture(UniqueRandomDataFixture, PostgresFixtureMixin):
                pass
            self.fixture = CustomFixture()

except (ImportError, ModuleNotFoundError):
    print('Skipping Postgres tests because psycopg2 has not been installed.')
