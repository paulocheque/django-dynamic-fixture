# -*- coding: utf-8 -*-

from django import conf

from django.test import TestCase

from django_dynamic_fixture import global_settings
from django_dynamic_fixture.fixture_algorithms.sequential_fixture import SequentialDataFixture, \
    StaticSequentialDataFixture
from django_dynamic_fixture.fixture_algorithms.random_fixture import RandomDataFixture
from six.moves import reload_module


class AbstractGlobalSettingsTestCase(TestCase):
    def tearDown(self):
        if hasattr(conf.settings, 'DDF_DEFAULT_DATA_FIXTURE'): del conf.settings.DDF_DEFAULT_DATA_FIXTURE
        if hasattr(conf.settings, 'DDF_FILL_NULLABLE_FIELDS'): del conf.settings.DDF_FILL_NULLABLE_FIELDS
        if hasattr(conf.settings, 'DDF_IGNORE_FIELDS'): del conf.settings.DDF_IGNORE_FIELDS
        if hasattr(conf.settings, 'DDF_NUMBER_OF_LAPS'): del conf.settings.DDF_NUMBER_OF_LAPS
        if hasattr(conf.settings, 'DDF_VALIDATE_MODELS'): del conf.settings.DDF_VALIDATE_MODELS
        reload_module(conf)


class CustomDataFixture(object): pass

class DDF_DEFAULT_DATA_FIXTURE_TestCase(AbstractGlobalSettingsTestCase):
    def test_not_configured_must_load_default_value(self):
        reload_module(global_settings)
        self.assertEquals(SequentialDataFixture, type(global_settings.DDF_DEFAULT_DATA_FIXTURE))

    def test_may_be_an_internal_data_fixture_nick_name(self):
        conf.settings.DDF_DEFAULT_DATA_FIXTURE = 'sequential'
        reload_module(global_settings)
        self.assertEquals(SequentialDataFixture, type(global_settings.DDF_DEFAULT_DATA_FIXTURE))

        conf.settings.DDF_DEFAULT_DATA_FIXTURE = 'random'
        reload_module(global_settings)
        self.assertEquals(RandomDataFixture, type(global_settings.DDF_DEFAULT_DATA_FIXTURE))

        conf.settings.DDF_DEFAULT_DATA_FIXTURE = 'static_sequential'
        reload_module(global_settings)
        self.assertEquals(StaticSequentialDataFixture, type(global_settings.DDF_DEFAULT_DATA_FIXTURE))

    def test_may_be_a_path_to_a_custom_data_fixture(self):
        conf.settings.DDF_DEFAULT_DATA_FIXTURE = 'django_dynamic_fixture.tests.test_global_settings.CustomDataFixture'
        reload_module(global_settings)
        self.assertEquals(CustomDataFixture, type(global_settings.DDF_DEFAULT_DATA_FIXTURE))

    def test_if_path_can_not_be_found_it_will_raise_an_exception(self):
        conf.settings.DDF_DEFAULT_DATA_FIXTURE = 'unknown_path.CustomDataFixture'
        self.assertRaises(Exception, reload_module, global_settings)


class DDF_FILL_NULLABLE_FIELDS_TestCase(AbstractGlobalSettingsTestCase):
    def test_not_configured_must_load_default_value(self):
        reload_module(global_settings)
        self.assertEquals(True, global_settings.DDF_FILL_NULLABLE_FIELDS)

    def test_must_be_a_boolean(self):
        conf.settings.DDF_FILL_NULLABLE_FIELDS = False
        reload_module(global_settings)
        self.assertEquals(False, global_settings.DDF_FILL_NULLABLE_FIELDS)

    def test_must_raise_an_exception_if_it_is_not_a_boolean(self):
        conf.settings.DDF_FILL_NULLABLE_FIELDS = 'x'
        self.assertRaises(Exception, reload_module, global_settings)


class DDF_IGNORE_FIELDS_TestCase(AbstractGlobalSettingsTestCase):
    def test_not_configured_must_load_default_value(self):
        reload_module(global_settings)
        self.assertEquals([], global_settings.DDF_IGNORE_FIELDS)

    def test_must_be_a_list_of_strings(self):
        conf.settings.DDF_IGNORE_FIELDS = ['x']
        reload_module(global_settings)
        self.assertEquals(['x'], global_settings.DDF_IGNORE_FIELDS)

    def test_must_raise_an_exception_if_it_is_not_an_list_of_strings(self):
        conf.settings.DDF_IGNORE_FIELDS = None
        self.assertRaises(Exception, reload_module, global_settings)


class DDF_NUMBER_OF_LAPS_TestCase(AbstractGlobalSettingsTestCase):
    def test_not_configured_must_load_default_value(self):
        reload_module(global_settings)
        self.assertEquals(1, global_settings.DDF_NUMBER_OF_LAPS)

    def test_must_be_an_integer(self):
        conf.settings.DDF_NUMBER_OF_LAPS = 2
        reload_module(global_settings)
        self.assertEquals(2, global_settings.DDF_NUMBER_OF_LAPS)

    def test_must_raise_an_exception_if_it_is_not_an_integer(self):
        conf.settings.DDF_NUMBER_OF_LAPS = None
        self.assertRaises(Exception, reload_module, global_settings)


class DDF_VALIDATE_MODELS_TestCase(AbstractGlobalSettingsTestCase):
    def test_not_configured_must_load_default_value(self):
        reload_module(global_settings)
        self.assertEquals(False, global_settings.DDF_VALIDATE_MODELS)

    def test_must_be_a_boolean(self):
        conf.settings.DDF_VALIDATE_MODELS = False
        reload_module(global_settings)
        self.assertEquals(False, global_settings.DDF_VALIDATE_MODELS)

    def test_must_raise_an_exception_if_it_is_not_a_boolean(self):
        conf.settings.DDF_VALIDATE_MODELS = 'x'
        self.assertRaises(Exception, reload_module, global_settings)


class DDF_USE_LIBRARY_TestCase(AbstractGlobalSettingsTestCase):
    def test_not_configured_must_load_default_value(self):
        reload_module(global_settings)
        self.assertEquals(False, global_settings.DDF_USE_LIBRARY)

    def test_must_be_a_boolean(self):
        conf.settings.DDF_USE_LIBRARY = False
        reload_module(global_settings)
        self.assertEquals(False, global_settings.DDF_USE_LIBRARY)

    def test_must_raise_an_exception_if_it_is_not_a_boolean(self):
        conf.settings.DDF_USE_LIBRARY = 'x'
        self.assertRaises(Exception, reload_module, global_settings)
