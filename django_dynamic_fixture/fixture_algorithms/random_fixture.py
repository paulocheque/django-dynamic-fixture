# -*- coding: utf-8 -*-
from datetime import datetime, date, timedelta
from decimal import Decimal
import random
import string

import six
try:
    from django.utils.timezone import now
except ImportError:
    now = datetime.now

try:
    from django.contrib.gis.geos import *
except ImportError:
    pass # Django < 1.7

from django_dynamic_fixture.fixture_algorithms.default_fixture import BaseDataFixture, GeoDjangoDataFixture


class RandomDataFixture(BaseDataFixture, GeoDjangoDataFixture):
    def random_string(self, n):
        return six.text_type('').join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))

    # NUMBERS
    def integerfield_config(self, field, key, start=1, end=10 ** 6):
        return random.randint(start, end)

    def smallintegerfield_config(self, field, key):
        # Values from -32768 to 32767 are safe in all databases supported by Django.
        return self.integerfield_config(field, key, -2 ** 15, 2 ** 15 - 1)

    def positiveintegerfield_config(self, field, key):
        return self.integerfield_config(field, key)

    def positivesmallintegerfield_config(self, field, key):
        # Values up to 32767 are safe in all databases supported by Django.
        return self.integerfield_config(field, key, end=2 ** 15 - 1)

    def bigintegerfield_config(self, field, key):
        return self.integerfield_config(field, key)

    def floatfield_config(self, field, key):
        return float(self.integerfield_config(field, key))

    def decimalfield_config(self, field, key):
        data = self.integerfield_config(field, key)
        number_of_digits = field.max_digits - field.decimal_places
        max_value = 10 ** number_of_digits
        data = data % max_value
        return Decimal(str(data))

    # STRINGS
    def charfield_config(self, field, key):
        if field.max_length:
            length = field.max_length
        else:
            length = 10
        return self.random_string(length)

    def textfield_config(self, field, key):
        return self.charfield_config(field, key)

    def slugfield_config(self, field, key):
        return self.charfield_config(field, key)

    def commaseparatedintegerfield_config(self, field, key):
        return six.text_type(random.randint(1, field.max_length)) #FIXME:

    # BOOLEAN
    def booleanfield_config(self, field, key):
        return random.randint(0, 1) == 0

    def nullbooleanfield_config(self, field, key):
        values = {0: None, 1: False, 2: True}
        return values[random.randint(0, 2)]

    # DATE/TIME RELATED
    def datefield_config(self, field, key):
        return date.today() - timedelta(days=random.randint(1, 36500))

    def timefield_config(self, field, key):
        return now() - timedelta(seconds=random.randint(1, 36500))

    def datetimefield_config(self, field, key):
        return now() - timedelta(seconds=random.randint(1, 36500))

    # FORMATTED STRINGS
    def emailfield_config(self, field, key):
        return six.text_type('a%s@dynamicfixture.com') % self.random_string(10)

    def urlfield_config(self, field, key):
        return six.text_type('http://dynamicfixture%s.com') % self.random_string(10)

    # Deprecated in Django >= 1.7
    def ipaddressfield_config(self, field, key):
        a = random.randint(1, 255)
        b = random.randint(1, 255)
        c = random.randint(1, 255)
        d = random.randint(1, 255)
        return six.text_type('%s.%s.%s.%s') % (a, b, c, d)

    def xmlfield_config(self, field, key):
        return six.text_type('<a>%s</a>') % self.random_string(5)

    # FILES
    def filepathfield_config(self, field, key):
        return self.random_string(10)

    def filefield_config(self, field, key):
        return self.random_string(10)

    def imagefield_config(self, field, key):
        return self.random_string(10)
