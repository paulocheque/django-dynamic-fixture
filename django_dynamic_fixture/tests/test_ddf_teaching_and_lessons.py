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
        DDFLibrary.get_instance().clear()


class TeachAndLessonsTest(DDFTestCase):
    def test_teach_a_default_lesson_for_a_model(self):
        self.ddf.teach(ModelForLibrary, integer=1000)
        instance = self.ddf.get(ModelForLibrary)
        assert instance.integer == 1000

    def test_default_lesson_may_be_overrided_although_it_is_an_anti_pattern(self):
        self.ddf.teach(ModelForLibrary, integer=1000)
        instance = self.ddf.get(ModelForLibrary)
        assert instance.integer == 1000
        self.ddf.teach(ModelForLibrary, integer=1001)
        instance = self.ddf.get(ModelForLibrary)
        assert instance.integer == 1001

    def test_it_must_NOT_raise_an_error_if_user_try_to_use_a_not_saved_default_configuration(self):
        self.ddf.get(ModelForLibrary)

    def test_it_must_raise_an_error_if_try_to_set_a_static_value_to_a_field_with_unicity(self):
        with pytest.raises(InvalidConfigurationError):
            self.ddf.teach(ModelForLibrary, integer_unique=1000)

    def test_it_must_accept_dynamic_values_for_fields_with_unicity(self):
        self.ddf.teach(ModelForLibrary, integer_unique=lambda field: 1000)

    def test_it_must_NOT_propagate_lessons_for_internal_dependencies(self):
        self.ddf.teach(ModelForLibrary, foreignkey=DynamicFixture(data_fixture, integer=1000))
        instance = self.ddf.get(ModelForLibrary)
        assert instance.integer != 1000
        assert instance.foreignkey.integer == 1000

    def test_it_must_use_lessons_for_internal_dependencies(self):
        # ModelForLibrary.foreignkey is a `ModelForLibrary2`
        self.ddf.teach(ModelForLibrary, integer=1000)
        self.ddf.teach(ModelForLibrary2, integer=1001)
        instance = self.ddf.get(ModelForLibrary, foreignkey=DynamicFixture(data_fixture))
        assert instance.integer == 1000
        assert instance.foreignkey.integer == 1001

    # Not implemented yet
    # def test_teaching_must_store_ddf_configs_too(self):
    #     self.ddf.teach(ModelForLibrary, fill_nullable_fields=False)
    #     instance = self.ddf.get(ModelForLibrary)
    #     assert instance.integer is None

    #     DDFLibrary.get_instance().clear()
    #     self.ddf.teach(ModelForLibrary, fill_nullable_fields=True)
    #     instance = self.ddf.get(ModelForLibrary)
    #     assert instance.integer is not None

    # Not implemented yet
    # def test_teaching_ddf_configs_must_NOT_be_propagated_to_another_models(self):
    #     self.ddf.teach(ModelForLibrary, fill_nullable_fields=False)
    #     instance = self.ddf.get(ModelForLibrary)
    #     assert instance.integer is None
    #     assert instance.foreignkey.integer is None

    #     DDFLibrary.get_instance().clear()
    #     self.ddf.teach(ModelForLibrary, fill_nullable_fields=True)
    #     instance = self.ddf.get(ModelForLibrary)
    #     assert instance.integer is not None
    #     assert instance.foreignkey.integer is None # not populated


class TeachingAndCustomLessonsTest(DDFTestCase):
    def test_a_model_can_have_custom_lessons(self):
        self.ddf.teach(ModelForLibrary, integer=1000, ddf_lesson=None)
        self.ddf.teach(ModelForLibrary, integer=1001, ddf_lesson='a name')
        instance = self.ddf.get(ModelForLibrary)
        assert instance.integer == 1000
        instance = self.ddf.get(ModelForLibrary, ddf_lesson='a name')
        assert instance.integer == 1001

    def test_custom_lessons_must_not_be_used_if_not_explicity_specified(self):
        self.ddf.teach(ModelForLibrary, integer=1000, ddf_lesson='a name')
        instance = self.ddf.get(ModelForLibrary)
        assert instance.integer != 1000

    def test_a_model_can_have_many_custom_lessons(self):
        self.ddf.teach(ModelForLibrary, integer=1000, ddf_lesson='a name')
        self.ddf.teach(ModelForLibrary, integer=1001, ddf_lesson='a name 2')

        instance = self.ddf.get(ModelForLibrary, ddf_lesson='a name')
        assert instance.integer == 1000

        instance = self.ddf.get(ModelForLibrary, ddf_lesson='a name 2')
        assert instance.integer == 1001

    def test_it_must_raise_an_error_if_user_try_to_use_a_not_saved_configuration(self):
        with pytest.raises(InvalidConfigurationError):
            self.ddf.get(ModelForLibrary, ddf_lesson='a not teached lesson')

    def test_default_lesson_and_custom_lesson_must_work_together(self):
        # regression test
        self.ddf.teach(ModelForLibrary, integer=1000, ddf_lesson='a name')
        self.ddf.teach(ModelForLibrary, integer=1001, ddf_lesson=True)
        self.ddf.teach(ModelForLibrary, integer=1002, ddf_lesson='a name2')
        instance = self.ddf.get(ModelForLibrary, ddf_lesson='a name')
        assert instance.integer == 1000
        instance = self.ddf.get(ModelForLibrary)
        assert instance.integer == 1001
        instance = self.ddf.get(ModelForLibrary, ddf_lesson='a name2')
        assert instance.integer == 1002

    def test_default_lesson_and_custom_lesson_must_work_together_for_different_models(self):
        # regression test
        self.ddf.teach(ModelForLibrary, integer=1000, ddf_lesson='a name')
        self.ddf.teach(ModelForLibrary, integer=1001, ddf_lesson=True)
        self.ddf.teach(ModelForLibrary, integer=1002, ddf_lesson='a name2')
        self.ddf.teach(ModelForLibrary2, integer=2000, ddf_lesson='a name')
        self.ddf.teach(ModelForLibrary2, integer=2001, ddf_lesson=True)
        self.ddf.teach(ModelForLibrary2, integer=2002, ddf_lesson='a name2')

        instance = self.ddf.get(ModelForLibrary, ddf_lesson='a name')
        assert instance.integer == 1000
        instance = self.ddf.get(ModelForLibrary)
        assert instance.integer == 1001
        instance = self.ddf.get(ModelForLibrary, ddf_lesson='a name2')
        assert instance.integer == 1002

        instance = self.ddf.get(ModelForLibrary2, ddf_lesson='a name')
        assert instance.integer == 2000
        instance = self.ddf.get(ModelForLibrary2)
        assert instance.integer == 2001
        instance = self.ddf.get(ModelForLibrary2, ddf_lesson='a name2')
        assert instance.integer == 2002


class DDFLibraryTest(TestCase):
    def setUp(self):
        self.lib = DDFLibrary()

    def test_add_and_get_configuration_without_string_name(self):
        self.lib.add_configuration(ModelForLibrary, {'a': 1})
        assert self.lib.get_configuration(ModelForLibrary) == {'a': 1}
        assert self.lib.get_configuration(ModelForLibrary, name=DDFLibrary.DEFAULT_KEY) == {'a': 1}
        assert self.lib.get_configuration(ModelForLibrary, name=None) == {'a': 1}

        self.lib.clear()
        self.lib.add_configuration(ModelForLibrary, {'a': 2}, name=None)
        assert self.lib.get_configuration(ModelForLibrary) == {'a': 2}
        assert self.lib.get_configuration(ModelForLibrary, name=DDFLibrary.DEFAULT_KEY) == {'a': 2}
        assert self.lib.get_configuration(ModelForLibrary, name=None) == {'a': 2}

        self.lib.clear()
        self.lib.add_configuration(ModelForLibrary, {'a': 3}, name=True)
        assert self.lib.get_configuration(ModelForLibrary) == {'a': 3}
        assert self.lib.get_configuration(ModelForLibrary, name=DDFLibrary.DEFAULT_KEY) == {'a': 3}
        assert self.lib.get_configuration(ModelForLibrary, name=None) == {'a': 3}

    def test_add_and_get_configuration_with_name(self):
        self.lib.add_configuration(ModelForLibrary, {'a': 1}, name='x')
        assert self.lib.get_configuration(ModelForLibrary, name='x') == {'a': 1}

    def test_clear_config(self):
        self.lib.clear_configuration(ModelForLibrary) # run ok if empty
        self.lib.add_configuration(ModelForLibrary, {'a': 1})
        self.lib.add_configuration(ModelForLibrary, {'a': 2}, name='x')
        self.lib.add_configuration(ModelForLibrary2, {'a': 3})
        self.lib.clear_configuration(ModelForLibrary)
        assert self.lib.get_configuration(ModelForLibrary) == {}
        with pytest.raises(Exception):
            self.lib.get_configuration(ModelForLibrary, name='x')
        assert self.lib.get_configuration(ModelForLibrary2) == {'a': 3}

    def test_clear(self):
        self.lib.add_configuration(ModelForLibrary, {'a': 1})
        self.lib.add_configuration(ModelForLibrary, {'a': 2}, name='x')
        self.lib.add_configuration(ModelForLibrary2, {'a': 3})
        self.lib.add_configuration(ModelForLibrary2, {'a': 4}, name='x')
        self.lib.clear()
        assert self.lib.get_configuration(ModelForLibrary) == {}
        with pytest.raises(Exception):
            self.lib.get_configuration(ModelForLibrary, name='x')
        assert self.lib.get_configuration(ModelForLibrary2) == {}
        with pytest.raises(Exception):
            self.lib.get_configuration(ModelForLibrary2, name='x')
