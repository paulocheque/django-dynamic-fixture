# -*- coding: utf-8 -*-
from datetime import datetime, date, timedelta
from decimal import Decimal
import threading

from django_dynamic_fixture.ddf import DataFixture
from django_dynamic_fixture.django_helper import field_is_unique

try:
    from django.utils.timezone import now
except ImportError:
    now = datetime.now


class AutoDataFiller(object):
    """
    Responsibility: generate a unique and sequential value for each key.
    """

    def __init__(self):
        self.__data_controller_map = {} # key => counter
        self.__locks = {} # key => lock

    # synchronized by key
    def next(self, key):
        if key not in self.__data_controller_map:
            self.__data_controller_map[key] = 0
            self.__locks[key] = threading.RLock()
        self.__locks[key].acquire()
        self.__data_controller_map[key] += 1
        value = self.__data_controller_map[key]
        self.__locks[key].release()
        return value

    def current(self, key):
        if key not in self.__data_controller_map:
            self.next(key)
        return self.__data_controller_map[key]


class SequentialDataFixture(DataFixture):

    def __init__(self):
        self.filler = AutoDataFiller()

    def get_value(self, field, key):
        return self.filler.next(key)

    # NUMBERS
    def integerfield_config(self, field, key):
        return self.get_value(field, key)

    def smallintegerfield_config(self, field, key):
        return self.integerfield_config(field, key)

    def positiveintegerfield_config(self, field, key):
        return self.integerfield_config(field, key)

    def positivesmallintegerfield_config(self, field, key):
        return self.integerfield_config(field, key)

    def bigintegerfield_config(self, field, key):
        return self.integerfield_config(field, key)

    def floatfield_config(self, field, key):
        return float(self.get_value(field, key))

    def decimalfield_config(self, field, key):
        data = self.get_value(field, key)
        number_of_digits = field.max_digits - field.decimal_places
        max_value = 10 ** number_of_digits
        data = data % max_value
        return Decimal(str(data))

    # STRINGS
    def charfield_config(self, field, key):
        data = self.get_value(field, key)
        if field.max_length:
            max_value = (10 ** field.max_length) - 1
            data = unicode(data % max_value)
            data = data[:field.max_length]
        else:
            data = unicode(data)
        return data

    def textfield_config(self, field, key):
        return self.charfield_config(field, key)

    def slugfield_config(self, field, key):
        return self.charfield_config(field, key)

    def commaseparatedintegerfield_config(self, field, key):
        return self.charfield_config(field, key)

    # BOOLEAN
    def booleanfield_config(self, field, key):
        return False

    def nullbooleanfield_config(self, field, key):
        return None

    # DATE/TIME RELATED
    def datefield_config(self, field, key):
        data = self.get_value(field, key)
        return date.today() - timedelta(days=data)

    def timefield_config(self, field, key):
        data = self.get_value(field, key)
        return now() - timedelta(seconds=data)

    def datetimefield_config(self, field, key):
        data = self.get_value(field, key)
        return now() - timedelta(seconds=data)

    # FORMATTED STRINGS
    def emailfield_config(self, field, key):
        return u'a%s@dynamicfixture.com' % self.get_value(field, key)

    def urlfield_config(self, field, key):
        return u'http://dynamicfixture%s.com' % self.get_value(field, key)

    def ipaddressfield_config(self, field, key):
        # TODO: better workaround (this suppose ip field is not unique)
        data = self.get_value(field, key)
        a = '1'
        b = '1'
        c = '1'
        d = data % 256
        return u'%s.%s.%s.%s' % (a, b, c, str(d))

    def xmlfield_config(self, field, key):
        return u'<a>%s</a>' % self.get_value(field, key)

    # FILES
    def filepathfield_config(self, field, key):
        return unicode(self.get_value(field, key))

    def filefield_config(self, field, key):
        return unicode(self.get_value(field, key))

    def imagefield_config(self, field, key):
        return unicode(self.get_value(field, key))


class GlobalSequentialDataFixture(SequentialDataFixture):
    def get_value(self, field, key):
        return self.filler.next('ddf-global-key')


class StaticSequentialDataFixture(SequentialDataFixture):
    def get_value(self, field, key):
        if field_is_unique(field):
            return self.filler.next(key)
        else:
            return self.filler.current(key)
