# -*- coding: utf-8 -*-
import uuid

from django.db import models

from django.test import TestCase

from django_dynamic_fixture.django_helper import django_greater_than
from django_dynamic_fixture.fixture_algorithms.default_fixture import BaseDataFixture


class BaseDataFixtureTestCase(TestCase):
    def setUp(self):
        self.fixture = BaseDataFixture()

    def test_uuid(self):
        if django_greater_than('1.8'):
            self.assertTrue(isinstance(self.fixture.generate_data(models.UUIDField()), uuid.UUID))

