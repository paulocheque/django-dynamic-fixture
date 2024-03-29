from django.db import models

from django.test import TestCase

from django_dynamic_fixture.fixture_algorithms.tests.abstract_test_generic_fixture import DataFixtureTestCase
from django_dynamic_fixture.fixture_algorithms.sequential_fixture import SequentialDataFixture, StaticSequentialDataFixture


class SequentialDataFixtureTestCase(TestCase, DataFixtureTestCase):
    def setUp(self):
        self.fixture = SequentialDataFixture()

    def test_it_must_fill_integer_fields_sequencially_by_attribute(self):
        assert self.fixture.generate_data(models.IntegerField()) == 1
        field = models.IntegerField()
        field.name = 'x'
        assert self.fixture.generate_data(field) == 1
        assert self.fixture.generate_data(field) == 2

    def test_it_must_fill_string_with_sequences_of_numbers_by_attribute(self):
        assert self.fixture.generate_data(models.CharField(max_length=1)) == '1'
        field = models.CharField(max_length=1)
        field.name = 'x'
        assert self.fixture.generate_data(field) == '1'
        assert self.fixture.generate_data(field) == '2'


class StaticSequentialDataFixtureTestCase(TestCase, DataFixtureTestCase):
    def setUp(self):
        self.fixture = StaticSequentialDataFixture()

    def test_it_must_fill_fields_sequencially_by_attribute_if_field_is_unique(self):
        field = models.IntegerField(unique=True)
        field.name = 'x'
        assert self.fixture.generate_data(field) == 1
        assert self.fixture.generate_data(field) == 2

    def test_it_must_fill_fields_with_static_value_by_attribute_if_field_is_not_unique(self):
        field = models.IntegerField(unique=False)
        field.name = 'x'
        assert self.fixture.generate_data(field) == 1
        assert self.fixture.generate_data(field) == 1

