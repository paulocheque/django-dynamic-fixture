# -*- coding: utf-8 -*-
import re

from django.test import TestCase
import pytest

from django_dynamic_fixture.models_test import *
from django_dynamic_fixture.ddf import *
from django_dynamic_fixture.fixture_algorithms.sequential_fixture import SequentialDataFixture


class DDFTestCase(TestCase):
    def setUp(self):
        self.ddf = DynamicFixture(SequentialDataFixture())


class MaskTests(DDFTestCase):
    def test_it_must_generate_random_numbers(self):
        instance = self.ddf.get(ModelWithStrings, string=Mask('###'))
        assert re.match(r'\d{3}', instance.string)

    def test_it_must_generate_lower_ascii_chars(self):
        instance = self.ddf.get(ModelWithStrings, string=Mask('___'))
        assert re.match(r'[a-z]{3}', instance.string)

    def test_it_must_generate_upper_ascii_chars(self):
        instance = self.ddf.get(ModelWithStrings, string=Mask('---'))
        assert re.match(r'[A-Z]{3}', instance.string)

    def test_it_must_accept_pure_chars(self):
        instance = self.ddf.get(ModelWithStrings, string=Mask('ABC123'))
        assert re.match(r'ABC123', instance.string)

    def test_it_must_be_able_to_escape_symbols(self):
        instance = self.ddf.get(ModelWithStrings, string=Mask(r'!# !_ !-'))
        assert '# _ -' == instance.string

    def test_phone_mask(self):
        instance = self.ddf.get(ModelWithStrings, string=Mask(r'+## (##) #####!-#####'))
        assert re.match(r'\+\d{2} \(\d{2}\) \d{5}-\d{5}', instance.string)

    def test_address_mask(self):
        instance = self.ddf.get(ModelWithStrings, string=Mask(r'St. -______, ### !- -- --'))
        assert re.match(r'St\. [A-Z]{1}[a-z]{6}, \d{3} - [A-Z]{2} [A-Z]{2}', instance.string)
