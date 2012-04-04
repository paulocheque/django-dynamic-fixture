# -*- coding: utf-8 -*-
from django.db import models

from django.test import TestCase

from django_dynamic_fixture.fixture_algorithms.tests.abstract_test_generic_fixture import DataFixtureTestCase
from django_dynamic_fixture.fixture_algorithms.sequential_fixture import SequentialDataFixture, StaticSequentialDataFixture


class SequentialDataFixtureTestCase(TestCase, DataFixtureTestCase):
    def setUp(self):
        self.fixture = SequentialDataFixture()

    def test_it_must_fill_integer_fields_sequencially_by_attribute(self):
        self.assertEquals(1, self.fixture.generate_data(models.IntegerField()))
        field = models.IntegerField()
        field.name = 'x'
        self.assertEquals(1, self.fixture.generate_data(field))
        self.assertEquals(2, self.fixture.generate_data(field))

    def test_it_must_fill_string_with_sequences_of_numbers_by_attribute(self):
        self.assertEquals('1', self.fixture.generate_data(models.CharField(max_length=1)))
        field = models.CharField(max_length=1)
        field.name = 'x'
        self.assertEquals('1', self.fixture.generate_data(field))
        self.assertEquals('2', self.fixture.generate_data(field))


class StaticSequentialDataFixtureTestCase(TestCase, DataFixtureTestCase):
    def setUp(self):
        self.fixture = StaticSequentialDataFixture()

    def test_it_must_fill_fields_sequencially_by_attribute_if_field_is_unique(self):
        field = models.IntegerField(unique=True)
        field.name = 'x'
        self.assertEquals(1, self.fixture.generate_data(field))
        self.assertEquals(2, self.fixture.generate_data(field))

    def test_it_must_fill_fields_with_static_value_by_attribute_if_field_is_not_unique(self):
        field = models.IntegerField(unique=False)
        field.name = 'x'
        self.assertEquals(1, self.fixture.generate_data(field))
        self.assertEquals(1, self.fixture.generate_data(field))

