# -*- coding: utf-8 -*-

from django.db import models

from datetime import datetime, date
from decimal import Decimal


class DataFixtureTestCase(object):
    def setUp(self):
        self.fixture = None

    def test_numbers(self):
        self.assertTrue(isinstance(self.fixture.generate_data(models.IntegerField()), int))
        self.assertTrue(isinstance(self.fixture.generate_data(models.SmallIntegerField()), int))
        self.assertTrue(isinstance(self.fixture.generate_data(models.PositiveIntegerField()), int))
        self.assertTrue(isinstance(self.fixture.generate_data(models.PositiveSmallIntegerField()), int))
        self.assertTrue(isinstance(self.fixture.generate_data(models.BigIntegerField()), int))
        self.assertTrue(isinstance(self.fixture.generate_data(models.FloatField()), float))
        self.assertTrue(isinstance(self.fixture.generate_data(models.DecimalField(max_digits=1, decimal_places=1)), Decimal))

    def test_it_must_deal_with_decimal_max_digits(self):
        # value 10 must be a problem, need to restart the counter: 10.0 has 3 digits
        for _ in xrange(11):
            self.assertTrue(isinstance(self.fixture.generate_data(models.DecimalField(max_digits=1, decimal_places=1)), Decimal))
            self.assertTrue(isinstance(self.fixture.generate_data(models.DecimalField(max_digits=2, decimal_places=1)), Decimal))

    def test_strings(self):
        self.assertTrue(isinstance(self.fixture.generate_data(models.CharField(max_length=1)), unicode))
        self.assertTrue(isinstance(self.fixture.generate_data(models.TextField()), unicode))
        self.assertTrue(isinstance(self.fixture.generate_data(models.SlugField(max_length=1)), unicode))
        self.assertTrue(isinstance(self.fixture.generate_data(models.CommaSeparatedIntegerField(max_length=1)), unicode))

    def test_new_truncate_strings_to_max_length(self):
        for _ in range(12): # truncate start after the 10 object
            self.assertTrue(isinstance(self.fixture.generate_data(models.CharField(max_length=1)), unicode))

    def test_boolean(self):
        self.assertTrue(isinstance(self.fixture.generate_data(models.BooleanField()), bool))
        value = self.fixture.generate_data(models.NullBooleanField())
        self.assertTrue(isinstance(value, bool) or value == None)

    def test_date_time_related(self):
        self.assertTrue(isinstance(self.fixture.generate_data(models.DateField()), date))
        self.assertTrue(isinstance(self.fixture.generate_data(models.TimeField()), datetime))
        self.assertTrue(isinstance(self.fixture.generate_data(models.DateTimeField()), datetime))

    def test_formatted_strings(self):
        self.assertTrue(isinstance(self.fixture.generate_data(models.EmailField(max_length=100)), unicode))
        self.assertTrue(isinstance(self.fixture.generate_data(models.URLField(max_length=100)), unicode))
        self.assertTrue(isinstance(self.fixture.generate_data(models.IPAddressField(max_length=100)), unicode))

    def test_files(self):
        self.assertTrue(isinstance(self.fixture.generate_data(models.FilePathField(max_length=100)), unicode))
        self.assertTrue(isinstance(self.fixture.generate_data(models.FileField()), unicode))
        try:
            import pil
            # just test it if the PIL package is installed
            self.assertTrue(isinstance(self.fixture.generate_data(models.ImageField(max_length=100)), unicode))
        except ImportError:
            pass

