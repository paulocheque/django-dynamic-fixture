# -*- coding: utf-8 -*-

from django.test import TestCase

from django_dynamic_fixture.fixture_algorithms.tests.abstract_test_generic_fixture import DataFixtureTestCase
from django_dynamic_fixture.fixture_algorithms.random_fixture import RandomDataFixture


class RandomDataFixtureTestCase(TestCase, DataFixtureTestCase):
    def setUp(self):
        self.fixture = RandomDataFixture()
