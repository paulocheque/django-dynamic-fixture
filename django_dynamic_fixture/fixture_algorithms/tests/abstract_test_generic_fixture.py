# -*- coding: utf-8 -*-

from django.db import models

from datetime import datetime, date
from decimal import Decimal
import six


class DataFixtureTestCase(object):
    def setUp(self):
        self.fixture = None

    def test_numbers(self):
        assert isinstance(self.fixture.generate_data(models.IntegerField()), int)
        assert isinstance(self.fixture.generate_data(models.SmallIntegerField()), int)
        assert isinstance(self.fixture.generate_data(models.PositiveIntegerField()), int)
        assert isinstance(self.fixture.generate_data(models.PositiveSmallIntegerField()), int)
        assert isinstance(self.fixture.generate_data(models.BigIntegerField()), int)
        assert isinstance(self.fixture.generate_data(models.FloatField()), float)
        assert isinstance(self.fixture.generate_data(models.DecimalField(max_digits=1, decimal_places=1)), Decimal)

    def test_it_must_deal_with_decimal_max_digits(self):
        # value 10 must be a problem, need to restart the counter: 10.0 has 3 digits
        for _ in range(11):
            assert isinstance(self.fixture.generate_data(models.DecimalField(max_digits=1, decimal_places=1)), Decimal)
            assert isinstance(self.fixture.generate_data(models.DecimalField(max_digits=2, decimal_places=1)), Decimal)

    def test_strings(self):
        assert isinstance(self.fixture.generate_data(models.CharField(max_length=1)), six.text_type)
        assert isinstance(self.fixture.generate_data(models.TextField()), six.text_type)
        assert isinstance(self.fixture.generate_data(models.SlugField(max_length=1)), six.text_type)
        assert isinstance(self.fixture.generate_data(models.CommaSeparatedIntegerField(max_length=1)), six.text_type)

    def test_new_truncate_strings_to_max_length(self):
        for _ in range(12): # truncate start after the 10 object
            assert isinstance(self.fixture.generate_data(models.CharField(max_length=1)), six.text_type)

    def test_boolean(self):
        assert isinstance(self.fixture.generate_data(models.BooleanField()), bool)
        value = self.fixture.generate_data(models.NullBooleanField())
        assert isinstance(value, bool) or value == None

    def test_date_time_related(self):
        assert isinstance(self.fixture.generate_data(models.DateField()), date)
        assert isinstance(self.fixture.generate_data(models.TimeField()), datetime)
        assert isinstance(self.fixture.generate_data(models.DateTimeField()), datetime)

    def test_formatted_strings(self):
        assert isinstance(self.fixture.generate_data(models.EmailField(max_length=100)), six.text_type)
        assert isinstance(self.fixture.generate_data(models.URLField(max_length=100)), six.text_type)
        assert isinstance(self.fixture.generate_data(models.IPAddressField(max_length=100)), six.text_type)
        assert isinstance(self.fixture.generate_data(models.GenericIPAddressField(max_length=100)), six.text_type)

    def test_files(self):
        assert isinstance(self.fixture.generate_data(models.FilePathField(max_length=100)), six.text_type)
        assert isinstance(self.fixture.generate_data(models.FileField()), six.text_type)
        try:
            import pil
            # just test it if the PIL package is installed
            assert isinstance(self.fixture.generate_data(models.ImageField(max_length=100)), six.text_type)
        except ImportError:
            pass

