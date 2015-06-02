# -*- coding: utf-8 -*-
from datetime import datetime, date, timedelta
from decimal import Decimal
from itertools import chain
import random
import socket
import string
import struct
from warnings import warn

import six
from six.moves import xrange
try:
    from django.utils.timezone import now
except ImportError:
    now = datetime.now
try:
    from django.contrib.gis.geos import *
except ImportError:
    pass # Django < 1.7

from django_dynamic_fixture.fixture_algorithms.sequential_fixture import AutoDataFiller
from django_dynamic_fixture.fixture_algorithms.default_fixture import BaseDataFixture, GeoDjangoDataFixture


class UniqueRandomDataFixture(BaseDataFixture, GeoDjangoDataFixture):
    DEFAULT_LENGTH = 10
    OBJECT_COUNT = 512
    WARNING_MESSAGE_TMPL = (
        'Maximum number of objects (%d) is exceeded in '
        'unique_random_fixture. Uniqueness is not guaranteed.'
    )

    def __init__(self):
        super(UniqueRandomDataFixture, self).__init__()
        self.filler = AutoDataFiller()

    def get_counter(self, field, key):
        result = self.filler.next(key)
        if result > self.OBJECT_COUNT:
            warn(self.WARNING_MESSAGE_TMPL % self.OBJECT_COUNT, RuntimeWarning)
        return result

    def random_string(self, field, key, n=None):
        counter = six.text_type(self.get_counter(field, key))
        length = n or self.DEFAULT_LENGTH
        result = counter
        result += six.text_type('').join(
            random.choice(string.ascii_letters)
            for _ in xrange(length - len(counter))
        )
        return result

    def random_integer(self, field, key, signed=True):
        counter = self.get_counter(field, key) - 1
        counter %= self.OBJECT_COUNT
        if not signed:
            MAX_INT = 2 ** 16
            multiplier = MAX_INT // self.OBJECT_COUNT
            return random.randrange(
                multiplier * counter + 1, multiplier * (counter + 1)
            )

        MAX_SIGNED_INT = 2 ** 15
        multiplier = MAX_SIGNED_INT // self.OBJECT_COUNT
        positive_range = range(
            multiplier * counter + 1, multiplier * (counter + 1)
        )
        negative_range = range(
            (-multiplier) * (counter + 1), (-multiplier) * counter
        )
        return random.choice(list(chain(positive_range, negative_range)))

    # NUMBERS
    def integerfield_config(self, field, key):
        return self.random_integer(field, key)

    def smallintegerfield_config(self, field, key):
        return self.random_integer(field, key)

    def bigintegerfield_config(self, field, key):
        return self.random_integer(field, key)

    def positiveintegerfield_config(self, field, key):
        return self.random_integer(field, key, signed=False)

    def positivesmallintegerfield_config(self, field, key):
        return self.random_integer(field, key, signed=False)

    def floatfield_config(self, field, key):
        return float(self.random_integer(field, key)) + random.random()

    def decimalfield_config(self, field, key):
        number_of_digits = field.max_digits - field.decimal_places
        max_value = 10 ** number_of_digits
        value = self.random_integer(field, key) % max_value
        value = float(value) + random.random()
        return Decimal(str(value))

    # STRINGS
    def charfield_config(self, field, key):
        return self.random_string(field, key, field.max_length)

    def textfield_config(self, field, key):
        return self.charfield_config(field, key)

    def slugfield_config(self, field, key):
        return self.charfield_config(field, key)

    def commaseparatedintegerfield_config(self, field, key):
        return self.charfield_config(field, key)

    # BOOLEAN
    def booleanfield_config(self, field, key):
        counter = self.get_counter(field, key)
        if counter == 1:
            return True
        elif counter == 2:
            return False
        return random.choice((True, False))

    def nullbooleanfield_config(self, field, key):
        counter = self.get_counter(field, key)
        if counter == 1:
            return None
        elif counter == 2:
            return True
        elif counter == 3:
            return False
        return random.choice((None, True, False))

    # DATE/TIME RELATED
    def datefield_config(self, field, key):
        integer = self.random_integer(field, key, signed=False)
        return date.today() - timedelta(days=integer)

    def timefield_config(self, field, key):
        integer = self.random_integer(field, key, signed=False)
        return now() - timedelta(seconds=integer)

    def datetimefield_config(self, field, key):
        integer = self.random_integer(field, key, signed=False)
        return now() - timedelta(seconds=integer)

    # FORMATTED STRINGS
    def emailfield_config(self, field, key):
        return six.text_type('a%s@dynamicfixture.com') % self.random_string(field, key)

    def urlfield_config(self, field, key):
        return six.text_type('http://dynamicfixture%s.com') % self.random_string(field, key)

    # Deprecated in Django >= 1.7
    def ipaddressfield_config(self, field, key):
        MAX_IP = 2 ** 32 - 1

        integer = self.random_integer(field, key, signed=False)
        integer %= MAX_IP
        return six.text_type(socket.inet_ntoa(struct.pack('!L', integer)))

    def xmlfield_config(self, field, key):
        return six.text_type('<a>%s</a>') % self.random_string(field, key)

    # FILES
    def filepathfield_config(self, field, key):
        return self.random_string(field, key)

    def filefield_config(self, field, key):
        return self.random_string(field, key)

    def imagefield_config(self, field, key):
        return self.random_string(field, key)
