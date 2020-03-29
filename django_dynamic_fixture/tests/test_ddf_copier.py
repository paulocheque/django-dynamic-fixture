# -*- coding: utf-8 -*-
from django.test import TestCase
import pytest

from django_dynamic_fixture.models_test import *
from django_dynamic_fixture.ddf import *
from django_dynamic_fixture.fixture_algorithms.sequential_fixture import SequentialDataFixture


data_fixture = SequentialDataFixture()


class DDFTestCase(TestCase):
    def setUp(self):
        self.ddf = DynamicFixture(data_fixture)


class CopyTest(DDFTestCase):
    def test_it_should_copy_from_model_fields(self):
        instance = self.ddf.get(ModelForCopy, int_a=Copier('int_b'), int_b=3)
        assert instance.int_a == 3

    def test_simple_scenario(self):
        instance = self.ddf.get(ModelForCopy, int_b=Copier('int_a'))
        assert instance.int_b == instance.int_a

    def test_order_of_attributes_must_be_superfluous(self):
        instance = self.ddf.get(ModelForCopy, int_a=Copier('int_b'))
        assert instance.int_a == instance.int_b

    def test_it_should_deal_with_multiple_copiers(self):
        instance = self.ddf.get(ModelForCopy, int_a=Copier('int_b'), int_c=Copier('int_d'))
        assert instance.int_a == instance.int_b
        assert instance.int_c == instance.int_d

    def test_multiple_copiers_can_depend_of_one_field(self):
        instance = self.ddf.get(ModelForCopy, int_a=Copier('int_c'), int_b=Copier('int_c'))
        assert instance.int_a == instance.int_c
        assert instance.int_b == instance.int_c

    def test_it_should_deal_with_dependent_copiers(self):
        instance = self.ddf.get(ModelForCopy, int_a=Copier('int_b'), int_b=Copier('int_c'))
        assert instance.int_a == instance.int_b
        assert instance.int_b == instance.int_c

    def test_it_should_deal_with_relationships(self):
        instance = self.ddf.get(ModelForCopy, int_a=Copier('e.int_e'))
        assert instance.int_a == instance.e.int_e

        instance = self.ddf.get(ModelForCopy, int_a=Copier('e.int_e'), e=DynamicFixture(data_fixture, int_e=5))
        assert instance.int_a == 5

    def test_it_should_raise_a_bad_data_error_if_value_is_invalid(self):
        with pytest.raises(BadDataError):
            self.ddf.get(ModelForCopy, int_a=Copier('int_b'), int_b=None)

    def test_it_should_raise_a_invalid_configuration_error_if_expression_is_bugged(self):
        with pytest.raises(InvalidConfigurationError):
            self.ddf.get(ModelForCopy, int_a=Copier('invalid_field'))
        with pytest.raises(InvalidConfigurationError):
            self.ddf.get(ModelForCopy, int_a=Copier('int_b.invalid_field'))

    def test_it_should_raise_a_invalid_configuration_error_if_copier_has_cyclic_dependency(self):
        with pytest.raises(InvalidConfigurationError):
            self.ddf.get(ModelForCopy, int_a=Copier('int_b'), int_b=Copier('int_a'))

    def test_it_must_copy_generated_data_mask_too(self):
        import re
        instance = self.ddf.get(ModelWithStrings, string=Mask('- _ #'), text=Copier('string'))
        assert re.match(r'[A-Z]{1} [a-z]{1} [0-9]{1}', instance.string)
        assert re.match(r'[A-Z]{1} [a-z]{1} [0-9]{1}', instance.text)
