# -*- coding: utf-8 -*-
from django.conf import settings

from django.test import TestCase
import pytest

from django_dynamic_fixture.models_test import *
from django_dynamic_fixture.ddf import *
from django_dynamic_fixture.decorators import only_for_database, POSTGRES
from django_dynamic_fixture.fixture_algorithms.sequential_fixture import SequentialDataFixture

data_fixture = SequentialDataFixture()


class DDFTestCase(TestCase):
    def setUp(self):
        self.ddf = DynamicFixture(data_fixture)


class CustomFieldsTest(DDFTestCase):
    def test_new_field_that_extends_django_field_must_be_supported(self):
        instance = self.ddf.new(ModelWithCustomFields)
        assert instance.x == 1

    def test_new_field_that_extends_django_field_must_be_supported_with_custom_value(self):
        instance = self.ddf.new(ModelWithCustomFields, x=6)
        assert instance.x == 6

    def test_unsupported_field_is_filled_with_null_if_it_is_possible(self):
        instance = self.ddf.new(ModelWithCustomFields)
        assert instance.y is None

    def test_unsupported_field_raise_an_error_if_it_does_not_accept_null_value(self):
        DDFLibrary.get_instance().clear()
        with pytest.raises(UnsupportedFieldError):
            self.ddf.new(ModelWithUnsupportedField)

    def test_new_field_that_double_inherits_django_field_must_be_supported(self):
        instance = self.ddf.new(ModelWithCustomFieldsMultipleInheritance)
        assert instance.x == 1

    def test_new_field_that_double_inherits_django_field_must_be_supported_with_custom_value(self):
        instance = self.ddf.new(ModelWithCustomFieldsMultipleInheritance, x=5)
        assert instance.x == 5


class NewFullFillAttributesUsingPluginsTest(DDFTestCase):
    def test_custom_field_not_registered_must_raise_an_unsupported_field_exception(self):
        DDFLibrary.get_instance().clear()
        with pytest.raises(UnsupportedFieldError):
            self.ddf.get(ModelWithUnsupportedField)

    def test_new_fill_field_with_data_generated_by_plugins_with_dict(self):
        data_fixture.plugins = settings.DDF_FIELD_FIXTURES
        try:
            instance = self.ddf.get(ModelForFieldPlugins)
            # assert instance.aaa == 123456789
            # assert instance.bbb == 123456789
            assert instance.custom_field_custom_fixture == 123456789
        finally:
            data_fixture.plugins = {}

    def test_new_fill_field_with_data_generated_by_plugins_with_direct_fuction(self):
        data_fixture.plugins = settings.DDF_FIELD_FIXTURES
        try:
            instance = self.ddf.get(ModelForFieldPlugins)
            assert instance.custom_field_custom_fixture2 == 987654321
        finally:
            data_fixture.plugins = {}

    # Real Custom Field
    def test_json_field_not_registered_must_raise_an_unsupported_field_exception(self):
        # jsonfield requires Django 1.4+
        try:
            from jsonfield import JSONCharField, JSONField
            instance = self.ddf.new(ModelForPlugins1)
            assert False, 'JSON fields must not be supported by default'
        except ImportError:
            pass
        except UnsupportedFieldError as e:
            pass

    def test_new_fill_json_field_with_data_generated_by_plugins(self):
        # jsonfield requires Django 1.4+
        try:
            import json
            from jsonfield import JSONCharField, JSONField
            data_fixture.plugins = settings.DDF_FIELD_FIXTURES
            try:
                instance = self.ddf.new(ModelForPlugins1)
                assert isinstance(instance.json_field1, str), type(instance.json_field1)
                assert isinstance(instance.json_field2, str), type(instance.json_field2)
                assert isinstance(json.loads(instance.json_field1), dict)
                assert isinstance(json.loads(instance.json_field2), list)
                assert instance.json_field1 == '{"some random value": "c"}'
                assert instance.json_field2 == '[1, 2, 3]'
            finally:
                data_fixture.plugins = {}
        except ImportError:
            pass


class PostgresCustomFieldsTest(DDFTestCase):
    @only_for_database(POSTGRES)
    def test_json_field(self):
        instance = self.ddf.get(ModelForPostgresFields)
        assert instance.nullable_json_field == {}
        assert instance.json_field == {}

    @only_for_database(POSTGRES)
    def test_json_field_as_null(self):
        instance = self.ddf.get(ModelForPostgresFields, nullable_json_field=None)
        assert instance.nullable_json_field is None

    @only_for_database(POSTGRES)
    def test_json_field_as_dicts(self):
        instance = self.ddf.get(ModelForPostgresFields, json_field={'a': 1})
        assert instance.json_field == {'a': 1}

    @only_for_database(POSTGRES)
    def test_json_field_as_lists(self):
        instance = self.ddf.get(ModelForPostgresFields, json_field=['str1', 2, {'c': 3}])
        assert instance.json_field == ['str1', 2, {'c': 3}]

    @only_for_database(POSTGRES)
    def test_json_field_as_strings(self):
        instance = self.ddf.get(ModelForPostgresFields, json_field='str')
        assert instance.json_field == 'str'
