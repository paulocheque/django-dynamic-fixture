# -*- coding: utf-8 -*-
from warnings import catch_warnings

from django.db import models
from django.test import TestCase

from django_dynamic_fixture.fixture_algorithms.tests.abstract_test_generic_fixture import DataFixtureTestCase
from django_dynamic_fixture.fixture_algorithms.unique_random_fixture import \
    UniqueRandomDataFixture


class RandomDataFixtureTestCase(TestCase, DataFixtureTestCase):
    def setUp(self):
        self.fixture = UniqueRandomDataFixture()

    def test_generated_strings_are_unique(self):
        results = set()
        for _ in range(self.fixture.OBJECT_COUNT):
            results.add(
                self.fixture.generate_data(models.CharField(max_length=10))
            )
        assert len(results) == self.fixture.OBJECT_COUNT

    def test_generated_signed_integers_are_unique(self):
        results = set()
        prev = 0
        for _ in range(self.fixture.OBJECT_COUNT):
            integer = self.fixture.generate_data(models.IntegerField())
            results.add(integer)
            assert abs(integer) > abs(prev)
            prev = integer
        assert len(results) == self.fixture.OBJECT_COUNT

    def test_generated_unsigned_integers_are_unique(self):
        results = set()
        prev = 0
        for _ in range(self.fixture.OBJECT_COUNT):
            integer = self.fixture.generate_data(models.PositiveIntegerField())
            results.add(integer)
            assert integer > prev
            prev = integer
        assert len(results) == self.fixture.OBJECT_COUNT

    def test_warning(self):
        with catch_warnings(record=True) as w:
            for _ in range(self.fixture.OBJECT_COUNT + 1):
                self.fixture.generate_data(models.CharField(max_length=10))
            warning = w[-1]
            assert issubclass(warning.category, RuntimeWarning)
            expected_message = (
                self.fixture.WARNING_MESSAGE_TMPL % self.fixture.OBJECT_COUNT
            )
            assert expected_message in str(warning.message)
