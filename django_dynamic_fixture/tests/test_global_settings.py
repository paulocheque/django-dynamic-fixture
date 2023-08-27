import importlib

from django import conf

from django.test import TestCase
import pytest

from django_dynamic_fixture import global_settings
from django_dynamic_fixture.fixture_algorithms.sequential_fixture import SequentialDataFixture, \
    StaticSequentialDataFixture
from django_dynamic_fixture.fixture_algorithms.random_fixture import RandomDataFixture



class AbstractGlobalSettingsTestCase(TestCase):
    def tearDown(self):
        if hasattr(conf.settings, 'DDF_DEFAULT_DATA_FIXTURE'): del conf.settings.DDF_DEFAULT_DATA_FIXTURE
        if hasattr(conf.settings, 'DDF_FILL_NULLABLE_FIELDS'): del conf.settings.DDF_FILL_NULLABLE_FIELDS
        if hasattr(conf.settings, 'DDF_IGNORE_FIELDS'): del conf.settings.DDF_IGNORE_FIELDS
        if hasattr(conf.settings, 'DDF_NUMBER_OF_LAPS'): del conf.settings.DDF_NUMBER_OF_LAPS
        if hasattr(conf.settings, 'DDF_VALIDATE_MODELS'): del conf.settings.DDF_VALIDATE_MODELS
        importlib.reload(conf)


class CustomDataFixture: pass

class DDF_DEFAULT_DATA_FIXTURE_TestCase(AbstractGlobalSettingsTestCase):
    def test_not_configured_must_load_default_value(self):
        importlib.reload(global_settings)
        assert SequentialDataFixture == type(global_settings.DDF_DEFAULT_DATA_FIXTURE)

    def test_may_be_an_internal_data_fixture_nick_name(self):
        conf.settings.DDF_DEFAULT_DATA_FIXTURE = 'sequential'
        importlib.reload(global_settings)
        assert SequentialDataFixture == type(global_settings.DDF_DEFAULT_DATA_FIXTURE)

        conf.settings.DDF_DEFAULT_DATA_FIXTURE = 'random'
        importlib.reload(global_settings)
        assert RandomDataFixture == type(global_settings.DDF_DEFAULT_DATA_FIXTURE)

        conf.settings.DDF_DEFAULT_DATA_FIXTURE = 'static_sequential'
        importlib.reload(global_settings)
        assert StaticSequentialDataFixture == type(global_settings.DDF_DEFAULT_DATA_FIXTURE)

    def test_may_be_a_path_to_a_custom_data_fixture(self):
        conf.settings.DDF_DEFAULT_DATA_FIXTURE = 'django_dynamic_fixture.tests.test_global_settings.CustomDataFixture'
        importlib.reload(global_settings)
        assert CustomDataFixture == type(global_settings.DDF_DEFAULT_DATA_FIXTURE)

    def test_if_path_can_not_be_found_it_will_raise_an_exception(self):
        conf.settings.DDF_DEFAULT_DATA_FIXTURE = 'unknown_path.CustomDataFixture'
        with pytest.raises(Exception):
            importlib.reload(global_settings)


class DDF_FILL_NULLABLE_FIELDS_TestCase(AbstractGlobalSettingsTestCase):
    def test_not_configured_must_load_default_value(self):
        importlib.reload(global_settings)
        assert global_settings.DDF_FILL_NULLABLE_FIELDS is False

    def test_must_be_a_boolean(self):
        conf.settings.DDF_FILL_NULLABLE_FIELDS = True
        importlib.reload(global_settings)
        assert global_settings.DDF_FILL_NULLABLE_FIELDS

    def test_must_raise_an_exception_if_it_is_not_a_boolean(self):
        conf.settings.DDF_FILL_NULLABLE_FIELDS = 'x'
        with pytest.raises(Exception):
            importlib.reload(global_settings)


class DDF_IGNORE_FIELDS_TestCase(AbstractGlobalSettingsTestCase):
    def test_not_configured_must_load_default_value(self):
        importlib.reload(global_settings)
        assert global_settings.DDF_IGNORE_FIELDS == []

    def test_must_be_a_list_of_strings(self):
        conf.settings.DDF_IGNORE_FIELDS = ['x']
        importlib.reload(global_settings)
        assert global_settings.DDF_IGNORE_FIELDS == ['x']

    def test_must_raise_an_exception_if_it_is_not_an_list_of_strings(self):
        conf.settings.DDF_IGNORE_FIELDS = None
        with pytest.raises(Exception):
            importlib.reload(global_settings)


class DDF_FK_MIN_DEPTH_TestCase(AbstractGlobalSettingsTestCase):
    def test_not_configured_must_load_default_value(self):
        importlib.reload(global_settings)
        assert global_settings.DDF_FK_MIN_DEPTH == 0

    def test_must_be_an_integer(self):
        conf.settings.DDF_FK_MIN_DEPTH = 2
        importlib.reload(global_settings)
        assert global_settings.DDF_FK_MIN_DEPTH == 2

    def test_must_raise_an_exception_if_it_is_not_an_integer(self):
        conf.settings.DDF_FK_MIN_DEPTH = None
        with pytest.raises(Exception):
            importlib.reload(global_settings)


class DDF_VALIDATE_MODELS_TestCase(AbstractGlobalSettingsTestCase):
    def test_not_configured_must_load_default_value(self):
        importlib.reload(global_settings)
        assert global_settings.DDF_VALIDATE_MODELS is False

    def test_must_be_a_boolean(self):
        conf.settings.DDF_VALIDATE_MODELS = False
        importlib.reload(global_settings)
        assert global_settings.DDF_VALIDATE_MODELS is False

    def test_must_raise_an_exception_if_it_is_not_a_boolean(self):
        conf.settings.DDF_VALIDATE_MODELS = 'x'
        with pytest.raises(Exception):
            importlib.reload(global_settings)
