# -*- coding: utf-8 -*-
from datetime import datetime, date
from decimal import Decimal
import uuid

import django
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


try:
    from django.contrib.gis.geos import *
except ImproperlyConfigured:
    pass  # enviroment without geo libs

try:
    from django.contrib.gis.db import models as geomodel
except ImproperlyConfigured:
    pass  # enviroment without geo libs

from django.test import TestCase
import pytest

from django_dynamic_fixture.models_test import *
from django_dynamic_fixture.ddf import *
from django_dynamic_fixture.ddf import _PRE_SAVE, _POST_SAVE
from django_dynamic_fixture.fixture_algorithms.sequential_fixture import SequentialDataFixture


data_fixture = SequentialDataFixture()


class DDFTestCase(TestCase):
    def setUp(self):
        self.ddf = DynamicFixture(data_fixture)
        DDFLibrary.get_instance().clear()
        _PRE_SAVE.clear()
        _POST_SAVE.clear()


class NewCreateAModelInstanceTest(DDFTestCase):
    def test_new_create_a_non_saved_instance_of_the_model(self):
        instance = self.ddf.new(EmptyModel)
        assert isinstance(instance, EmptyModel)
        assert instance.id is None


class GetDealWithPrimaryKeyTest(DDFTestCase):
    def test_get_use_database_id_by_default(self):
        instance = self.ddf.get(EmptyModel)
        assert instance.id is not None
        assert instance.pk is not None

    def test_get_use_given_id(self):
        instance = self.ddf.new(EmptyModel, id=99998)
        assert instance.id == 99998
        assert instance.pk == 99998

    def test_get_use_given_named_id(self):
        instance = self.ddf.get(ModelWithNamedPrimaryKey, named_pk=99998)
        assert instance.named_pk == 99998
        assert instance.pk == 99998


class NewFullFillAttributesWithAutoDataTest(DDFTestCase):
    def test_new_fill_number_fields_with_numbers(self):
        instance = self.ddf.new(ModelWithNumbers)
        assert isinstance(instance.integer, int)
        assert isinstance(instance.smallinteger, int)
        assert isinstance(instance.positiveinteger, int)
        assert isinstance(instance.positivesmallinteger, int)
        assert isinstance(instance.biginteger, int)
        assert isinstance(instance.float, float)

    def test_new_fill_string_fields_with_text_type_strings(self):
        instance = self.ddf.new(ModelWithStrings)
        assert isinstance(instance.string, six.text_type)
        assert isinstance(instance.text, six.text_type)
        assert isinstance(instance.slug, six.text_type)
        assert isinstance(instance.commaseparated, six.text_type)

    def test_new_fill_boolean_fields_with_False_and_None(self):
        instance = self.ddf.new(ModelWithBooleans)
        assert instance.boolean == False
        assert instance.nullboolean is None

    def test_new_fill_time_related_fields_with_current_values(self):
        instance = self.ddf.new(ModelWithDateTimes)
        assert date.today() >= instance.date
        assert datetime.now() >= instance.time
        assert datetime.now() >= instance.datetime

    def test_new_fill_formatted_strings_fields_with_basic_values(self):
        instance = self.ddf.new(ModelWithFieldsWithCustomValidation)
        assert isinstance(instance.email, six.text_type)
        assert isinstance(instance.url, six.text_type)
        assert isinstance(instance.ip, six.text_type)
        assert isinstance(instance.ipv6, six.text_type)

    def test_new_fill_file_fields_with_basic_strings(self):
        instance = self.ddf.new(ModelWithFileFields)
        assert isinstance(instance.filepath, six.text_type)
        assert isinstance(instance.file.path, six.text_type)
        try:
            import pil
            # just test it if the PIL package is installed
            assert isinstance(instance.image, str)
        except ImportError:
            pass

    def test_new_fill_binary_fields_with_basic_data(self):
        value = b'\x00\x46\xFE'
        instance = self.ddf.new(ModelWithBinary, binary=value)
        assert bytes(instance.binary) == bytes(value)

        instance = self.ddf.get(ModelWithBinary)
        if six.PY3:
            assert isinstance(instance.binary, six.binary_type), type(instance.binary)
        else:
            assert isinstance(instance.binary, (six.binary_type, str, unicode)), type(instance.binary)


class NewFullFillAttributesWithDefaultDataTest(DDFTestCase):
    def test_fill_field_with_default_data(self):
        instance = self.ddf.new(ModelWithDefaultValues)
        assert instance.integer_with_default == 3

    def test_fill_field_with_possible_choices(self):
        instance = self.ddf.new(ModelWithDefaultValues)
        assert instance.string_with_choices == 'a'

    def test_fill_field_with_default_value_even_if_field_is_foreign_key(self):
        instance = self.ddf.new(ModelWithDefaultValues)
        assert instance.foreign_key_with_default is None

    def test_fill_field_with_default_data_and_choices_must_consider_default_data_instead_choices(self):
        instance = self.ddf.new(ModelWithDefaultValues)
        assert instance.string_with_choices_and_default == 'b'

    def test_fill_field_with_possible_optgroup_choices(self):
        instance = self.ddf.new(ModelWithDefaultValues)
        assert instance.string_with_optgroup_choices == 'a'


class NewFullFillAttributesWithCustomDataTest(DDFTestCase):
    def test_fields_are_filled_with_custom_attributes(self):
        assert self.ddf.new(ModelWithNumbers, integer=9).integer == 9
        assert self.ddf.new(ModelWithStrings, string='7').string == '7'
        assert self.ddf.new(ModelWithBooleans, boolean=True).boolean

    def test_decimal_can_be_filled_by_an_string(self):
        self.ddf.get(ModelWithNumbers, decimal='9.5')
        assert ModelWithNumbers.objects.latest('id').decimal == Decimal('9.5')

    def test_fields_can_be_filled_by_functions(self):
        instance = self.ddf.new(ModelWithStrings, string=lambda field: field.name)
        assert instance.string == 'string'

    def test_invalid_configuration_raise_an_error(self):
        with pytest.raises(InvalidConfigurationError):
            self.ddf.new(ModelWithNumbers, integer=lambda x: ''.invalidmethod())

    def test_bad_data_raise_an_error(self):
        self.ddf.get(ModelWithNumbers, integer=50000)
        with pytest.raises(BadDataError):
            self.ddf.get(ModelWithNumbers, integer=50000)


class NewFullFillAttributesUsingPluginsTest(DDFTestCase):
    def test_custom_field_not_registered_must_raise_an_unsupported_field_exception(self):
        with pytest.raises(UnsupportedFieldError):
            self.ddf.new(ModelWithUnsupportedField)

    def test_new_fill_field_with_data_generated_by_plugins_with_dict(self):
        data_fixture.plugins = django.conf.settings.DDF_FIELD_FIXTURES
        try:
            instance = self.ddf.get(ModelForFieldPlugins)
            # assert instance.aaa == 123456789
            # assert instance.bbb == 123456789
            assert instance.custom_field_custom_fixture == 123456789
        finally:
            data_fixture.plugins = {}

    def test_new_fill_field_with_data_generated_by_plugins_with_direct_fuction(self):
        data_fixture.plugins = django.conf.settings.DDF_FIELD_FIXTURES
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
            data_fixture.plugins = django.conf.settings.DDF_FIELD_FIXTURES
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


class NewIgnoringNullableFieldsTest(DDFTestCase):
    def test_new_do_not_fill_nullable_fields_if_we_do_not_want_to(self):
        self.ddf = DynamicFixture(data_fixture, fill_nullable_fields=False)
        instance = self.ddf.new(ModelForNullable)
        assert instance.not_nullable is not None
        assert instance.nullable is None


class NewIgnoreFieldsInIgnoreListTest(DDFTestCase):
    def test_new_do_not_fill_ignored_fields(self):
        self.ddf = DynamicFixture(data_fixture, ignore_fields=['not_required', 'not_required_with_default'])
        instance = self.ddf.new(ModelForIgnoreList)
        assert instance.not_required is None
        assert instance.not_required_with_default is not None
        # not ignored fields
        assert instance.required is not None
        assert instance.required_with_default is not None

    def test_get_raise_an_error_if_a_required_field_is_in_ignore_list(self):
        self.ddf = DynamicFixture(data_fixture, ignore_fields=['required', 'required_with_default'])
        with pytest.raises(BadDataError):
            self.ddf.get(ModelForIgnoreList)

    def test_ignore_fields_are_propagated_to_self_references(self):
        self.ddf = DynamicFixture(data_fixture, ignore_fields=['not_required', 'nullable'])
        instance = self.ddf.new(ModelForIgnoreList)
        assert instance.not_required is None
        assert instance.self_reference.not_required is None

    def test_ignore_fields_are_not_propagated_to_different_references(self):
        self.ddf = DynamicFixture(data_fixture, ignore_fields=['not_required', 'nullable'])
        instance = self.ddf.new(ModelForIgnoreList)
        assert instance.different_reference.nullable is not None

    def test_ignore_fields_are_not_ignored_if_explicitely_given(self):
        self.ddf = DynamicFixture(data_fixture, not_required=3, ignore_fields=['not_required', 'nullable'])
        instance = self.ddf.new(ModelForIgnoreList)
        assert instance.not_required == 3


class NewAlsoCreatesRelatedObjectsTest(DDFTestCase):
    def test_new_fill_foreignkey_fields(self):
        instance = self.ddf.new(ModelWithRelationships)
        assert isinstance(instance.foreignkey, ModelRelated)

    def test_new_fill_onetoone_fields(self):
        instance = self.ddf.new(ModelWithRelationships)
        assert isinstance(instance.onetoone, ModelRelated)

    def test_new_deal_with_default_values(self):
        instance = self.ddf.new(ModelWithRelationships)
        assert isinstance(instance.foreignkey_with_default, ModelRelated), str(type(instance.foreignkey_with_default))

    def test_new_deal_with_id_default_values(self):
        instance = self.ddf.new(ModelWithRelationships)
        assert isinstance(instance.foreignkey_with_id_default, ModelRelated), str(type(instance.foreignkey_with_default))

#        TODO
#    def test_new_fill_genericrelations_fields(self):
#        instance = self.ddf.new(ModelWithRelationships)
#        assert isinstance(instance.foreignkey, ModelRelated)


class NewCanCreatesCustomizedRelatedObjectsTest(DDFTestCase):
    def test_customizing_nullable_fields_for_related_objects(self):
        instance = self.ddf.new(ModelWithRelationships, selfforeignkey=DynamicFixture(data_fixture, fill_nullable_fields=False))
        assert isinstance(instance.integer, int)
        assert instance.selfforeignkey.integer is None


class NewDealWithSelfReferencesTest(DDFTestCase):
    def test_new_create_by_default_only_1_lap_in_cycle(self):
        instance = self.ddf.new(ModelWithRelationships)
        assert instance.selfforeignkey is not None # 1 cycle
        assert instance.selfforeignkey.selfforeignkey is None # 2 cycles

    def test_new_create_n_laps_in_cycle(self):
        self.ddf = DynamicFixture(data_fixture, number_of_laps=2)
        instance = self.ddf.new(ModelWithRelationships)
        assert instance.selfforeignkey is not None # 1 cycle
        assert instance.selfforeignkey.selfforeignkey is not None # 2 cycles
        instance.selfforeignkey.selfforeignkey.selfforeignkey is None # 3 cycles


class GetFullFilledModelInstanceAndPersistTest(DDFTestCase):
    def test_get_create_and_save_a_full_filled_instance_of_the_model(self):
        instance = self.ddf.get(ModelWithRelationships)
        assert isinstance(instance, ModelWithRelationships)
        assert instance.id is not None
        # checking unique problems
        another_instance = self.ddf.get(ModelWithRelationships)
        assert isinstance(another_instance, ModelWithRelationships)
        assert another_instance.id is not None

    def test_get_create_and_save_related_fields(self):
        instance = self.ddf.get(ModelWithRelationships)
        assert instance.selfforeignkey is not None
        assert instance.foreignkey is not None
        assert instance.onetoone is not None


class ManyToManyRelationshipTest(DDFTestCase):
    def test_new_ignore_many_to_many_configuratios(self):
        instance = self.ddf.new(ModelWithRelationships, manytomany=3)
        instance.save()
        assert instance.manytomany.all().count() == 0

    def test_get_ignore_many_to_many_configuratios(self):
        instance = self.ddf.get(ModelWithRelationships, manytomany=3)
        assert instance.manytomany.all().count() == 3

    def test_many_to_many_configuratios_accept_list_of_dynamic_filters(self):
        instance = self.ddf.get(ModelWithRelationships, manytomany=[DynamicFixture(data_fixture, integer=1000), DynamicFixture(data_fixture, integer=1001)])
        assert instance.manytomany.all().count() == 2
        assert instance.manytomany.all()[0].integer == 1000
        assert instance.manytomany.all()[1].integer == 1001

    def test_many_to_many_configuratios_accept_list_of_instances(self):
        b1 = self.ddf.get(ModelRelated, integer=1000)
        b2 = self.ddf.get(ModelRelated, integer=1001)
        instance = self.ddf.get(ModelWithRelationships, manytomany=[b1, b2])
        assert instance.manytomany.all().count() == 2
        objs = instance.manytomany.all().order_by('integer')
        assert objs[0].integer == 1000
        assert objs[1].integer == 1001

    def test_invalid_many_to_many_configuration(self):
        with pytest.raises(InvalidManyToManyConfigurationError):
            self.ddf.get(ModelWithRelationships, manytomany='a')

    def test_many_to_many_through(self):
        b1 = self.ddf.get(ModelRelated, integer=1000)
        b2 = self.ddf.get(ModelRelated, integer=1001)
        instance = self.ddf.get(ModelWithRelationships, manytomany_through=[b1, b2])
        objs = instance.manytomany_through.all().order_by('integer')
        assert objs.count() == 2
        assert objs[0].integer == 1000
        assert objs[1].integer == 1001


class NewDealWithCyclicDependenciesTest(DDFTestCase):
    def test_new_create_by_default_only_1_lap_in_cycle(self):
        c = self.ddf.new(ModelWithCyclicDependency)
        assert c.d is not None # 1 cycle
        assert c.d.c is None # 2 cycles

    def test_new_create_n_laps_in_cycle(self):
        self.ddf = DynamicFixture(data_fixture, number_of_laps=2)
        c = self.ddf.new(ModelWithCyclicDependency)
        assert c.d is not None
        assert c.d.c is not None # 1 cycle
        assert c.d.c.d is not None # 2 cycles
        assert c.d.c.d.c is None # 3 cycles


class NewDealWithInheritanceTest(DDFTestCase):
    def test_new_must_not_raise_an_error_if_model_is_abstract(self):
        self.ddf.new(ModelAbstract) # it does not raise an exceptions

    def test_get_must_raise_an_error_if_model_is_abstract(self):
        with pytest.raises(InvalidModelError):
            self.ddf.get(ModelAbstract)

    def test_get_must_fill_parent_fields_too(self):
        instance = self.ddf.get(ModelParent)
        assert isinstance(instance.integer, int)
        assert ModelParent.objects.count() == 1

    def test_get_must_fill_grandparent_fields_too(self):
        instance = self.ddf.get(ModelChild)
        assert isinstance(instance.integer, int)
        assert ModelParent.objects.count() == 1
        assert ModelChild.objects.count() == 1

    def test_get_must_ignore_parent_link_attributes_but_the_parent_object_must_be_created(self):
        instance = self.ddf.get(ModelChildWithCustomParentLink)
        assert isinstance(instance.integer, int)
        assert ModelParent.objects.count() == 1
        assert ModelChildWithCustomParentLink.objects.count() == 1
        assert instance.my_custom_ref.id is not None
        assert instance.my_custom_ref.my_custom_ref_x.id is not None

    # TODO: need to check these tests. Here we are trying to simulate a bug with parent_link attribute
    def test_get_0(self):
        instance = self.ddf.get(ModelWithRefToParent)
        assert ModelWithRefToParent.objects.count() == 1
        assert ModelParent.objects.count() == 1
        assert isinstance(instance.parent, ModelParent)

    def test_get_1(self):
        instance = self.ddf.get(ModelWithRefToParent, parent=self.ddf.get(ModelChild))
        assert ModelWithRefToParent.objects.count() == 1
        assert ModelParent.objects.count() == 1
        assert ModelChild.objects.count() == 1
        assert isinstance(instance.parent, ModelChild)

    def test_get_2(self):
        instance = self.ddf.get(ModelWithRefToParent, parent=self.ddf.get(ModelChildWithCustomParentLink))
        assert ModelWithRefToParent.objects.count() == 1
        assert ModelParent.objects.count() == 1
        assert ModelChildWithCustomParentLink.objects.count() == 1
        assert isinstance(instance.parent, ModelChildWithCustomParentLink)


class CustomFieldsTest(DDFTestCase):
    def test_new_field_that_extends_django_field_must_be_supported(self):
        instance = self.ddf.new(ModelWithCustomFields)
        assert instance.x == 1

    def test_unsupported_field_is_filled_with_null_if_it_is_possible(self):
        instance = self.ddf.new(ModelWithCustomFields)
        assert instance.y is None

    def test_unsupported_field_raise_an_error_if_it_does_not_accept_null_value(self):
        with pytest.raises(UnsupportedFieldError):
            self.ddf.new(ModelWithUnsupportedField)

    def test_new_field_that_double_inherits_django_field_must_be_supported(self):
        instance = self.ddf.new(ModelWithCustomFieldsMultipleInheritance)
        assert instance.x == 1


class ComplexFieldsTest(DDFTestCase):
    def test_x(self):
        instance = self.ddf.new(ModelForUUID)
        assert isinstance(instance.uuid, uuid.UUID)


if (hasattr(settings, 'DDF_TEST_GEODJANGO') and settings.DDF_TEST_GEODJANGO):
    class GeoDjangoFieldsTest(DDFTestCase):
        def test_geodjango_fields(self):
            instance = self.ddf.new(ModelForGeoDjango)
            assert isinstance(instance.geometry, GEOSGeometry), str(type(instance.geometry))
            assert isinstance(instance.point, Point)
            assert isinstance(instance.line_string, LineString)
            assert isinstance(instance.polygon, Polygon)
            assert isinstance(instance.multi_point, MultiPoint)
            assert isinstance(instance.multi_line_string, MultiLineString)
            assert isinstance(instance.multi_polygon, MultiPolygon)
            assert isinstance(instance.geometry_collection, GeometryCollection)


class ModelValidatorsTest(DDFTestCase):
    def test_it_must_create_if_validation_is_disabled(self):
        instance = self.ddf.get(ModelWithValidators, field_validator='nok', clean_validator='nok')
        self.ddf.validate_models = False
        assert instance.field_validator == 'nok'
        assert instance.clean_validator == 'nok'

    def test_it_must_create_if_there_is_no_validation_errors(self):
        instance = self.ddf.get(ModelWithValidators, field_validator='ok', clean_validator='ok')
        self.ddf.validate_models = True
        assert instance.field_validator == 'ok'
        assert instance.clean_validator == 'ok'

    def test_it_must_raise_a_bad_data_error_if_data_is_not_valid(self):
        self.ddf.validate_models = True
        self.ddf.get(ModelWithValidators, field_validator='nok', clean_validator='ok')
        with pytest.raises(BadDataError):
            self.ddf.get(ModelWithValidators, field_validator='ok', clean_validator='nok')


class ConfigurationValidatorTest(DDFTestCase):
    def test_it_must_raise_a_bad_data_error_if_data_is_not_valid(self):
        self.ddf.validate_args = True
        with pytest.raises(InvalidConfigurationError):
            self.ddf.get(EmptyModel, unexistent_field='x')


class DisableAutoGeneratedDateTimesTest(DDFTestCase):
    def test_auto_generated_datetimes_must_be_respected_if_nothing_is_specified(self):
        instance = self.ddf.get(ModelWithAutoDateTimes)
        assert datetime.today().date() == instance.auto_now_add
        assert datetime.today().date() == instance.auto_now

    def test_it_must_ignore_auto_generated_datetime_if_a_custom_value_is_provided(self):
        instance = self.ddf.get(ModelWithAutoDateTimes, auto_now_add=date(2000, 12, 31))
        assert instance.auto_now_add == date(2000, 12, 31)

        instance = self.ddf.get(ModelWithAutoDateTimes, auto_now=date(2000, 12, 31))
        assert instance.auto_now == date(2000, 12, 31)

    def test_checking_if_implementation_works_for_m2m_fields_too(self):
        instance = self.ddf.get(ModelWithAutoDateTimes, manytomany=[DynamicFixture(data_fixture, auto_now_add=date(2000, 12, 31))])
        assert instance.manytomany.all()[0].auto_now_add == date(2000, 12, 31)

        instance = self.ddf.get(ModelWithAutoDateTimes, manytomany=[DynamicFixture(data_fixture, auto_now=date(2000, 12, 31))])
        assert instance.manytomany.all()[0].auto_now == date(2000, 12, 31)



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


class TeachAndLessonsTest(DDFTestCase):
    def test_teach_a_default_lesson_for_a_model(self):
        self.ddf.teach(ModelForLibrary, integer=1000)
        instance = self.ddf.get(ModelForLibrary)
        assert instance.integer == 1000

    def test_default_lesson_must_NOT_be_overrided(self):
        self.ddf.teach(ModelForLibrary, integer=1000)
        with pytest.raises(CantOverrideLesson):
            self.ddf.teach(ModelForLibrary, integer=1001)

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
        instance = self.ddf.get(ModelForLibrary)
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
        self.ddf.teach(ModelForLibrary, integer=1000, lesson=None)
        self.ddf.teach(ModelForLibrary, integer=1001, lesson='a name')
        instance = self.ddf.get(ModelForLibrary)
        assert instance.integer == 1000
        instance = self.ddf.get(ModelForLibrary, lesson='a name')
        assert instance.integer == 1001

    def test_custom_lessons_must_not_be_used_if_not_explicity_specified(self):
        self.ddf.teach(ModelForLibrary, integer=1000, lesson='a name')
        instance = self.ddf.get(ModelForLibrary)
        assert instance.integer != 1000

    def test_a_model_can_have_many_custom_lessons(self):
        self.ddf.teach(ModelForLibrary, integer=1000, lesson='a name')
        self.ddf.teach(ModelForLibrary, integer=1001, lesson='a name 2')

        instance = self.ddf.get(ModelForLibrary, lesson='a name')
        assert instance.integer == 1000

        instance = self.ddf.get(ModelForLibrary, lesson='a name 2')
        assert instance.integer == 1001

    def test_it_must_raise_an_error_if_user_try_to_use_a_not_saved_configuration(self):
        with pytest.raises(InvalidConfigurationError):
            self.ddf.get(ModelForLibrary, lesson='a not teached lesson')

    def test_default_lesson_and_custom_lesson_must_work_together(self):
        # regression test
        self.ddf.teach(ModelForLibrary, integer=1000, lesson='a name')
        self.ddf.teach(ModelForLibrary, integer=1001, lesson=True)
        self.ddf.teach(ModelForLibrary, integer=1002, lesson='a name2')
        instance = self.ddf.get(ModelForLibrary, lesson='a name')
        assert instance.integer == 1000
        instance = self.ddf.get(ModelForLibrary)
        assert instance.integer == 1001
        instance = self.ddf.get(ModelForLibrary, lesson='a name2')
        assert instance.integer == 1002

    def test_default_lesson_and_custom_lesson_must_work_together_for_different_models(self):
        # regression test
        self.ddf.teach(ModelForLibrary, integer=1000, lesson='a name')
        self.ddf.teach(ModelForLibrary, integer=1001, lesson=True)
        self.ddf.teach(ModelForLibrary, integer=1002, lesson='a name2')
        self.ddf.teach(ModelForLibrary2, integer=2000, lesson='a name')
        self.ddf.teach(ModelForLibrary2, integer=2001, lesson=True)
        self.ddf.teach(ModelForLibrary2, integer=2002, lesson='a name2')

        instance = self.ddf.get(ModelForLibrary, lesson='a name')
        assert instance.integer == 1000
        instance = self.ddf.get(ModelForLibrary)
        assert instance.integer == 1001
        instance = self.ddf.get(ModelForLibrary, lesson='a name2')
        assert instance.integer == 1002

        instance = self.ddf.get(ModelForLibrary2, lesson='a name')
        assert instance.integer == 2000
        instance = self.ddf.get(ModelForLibrary2)
        assert instance.integer == 2001
        instance = self.ddf.get(ModelForLibrary2, lesson='a name2')
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


class ModelWithCustomValidationTest(DDFTestCase):
    def test_ddf_can_not_create_instance_of_models_with_custom_validations(self):
        self.ddf.validate_models = True
        with pytest.raises(BadDataError):
            self.ddf.get(ModelWithClean)
        self.ddf.get(ModelWithClean, integer=9999) # this does not raise an exception


class PreSaveTest(DDFTestCase):
    def test_set_pre_save_receiver(self):
        def callback_function(instance):
            pass
        set_pre_save_receiver(ModelForSignals, callback_function)
        callback_function = lambda x: x
        set_pre_save_receiver(ModelForSignals, callback_function)

    def test_pre_save_receiver_must_raise_an_error_if_first_parameter_is_not_a_model_class(self):
        callback_function = lambda x: x
        with pytest.raises(InvalidReceiverError):
            set_pre_save_receiver(str, callback_function)

    def test_pre_save_receiver_must_raise_an_error_if_it_is_not_a_function(self):
        with pytest.raises(InvalidReceiverError):
            set_pre_save_receiver(ModelForSignals, '')

    def test_pre_save_receiver_must_raise_an_error_if_it_is_not_an_only_one_argument_function(self):
        callback_function = lambda x, y: x
        with pytest.raises(InvalidReceiverError):
            set_pre_save_receiver(ModelForSignals, callback_function)

    def test_pre_save_receiver_must_be_executed_before_saving(self):
        def callback_function(instance):
            if instance.id is not None:
                raise Exception('ops, instance already saved')
            self.ddf.get(ModelForSignals2)
        set_pre_save_receiver(ModelForSignals, callback_function)
        self.ddf.get(ModelForSignals)
        assert ModelForSignals2.objects.count() == 1

    def test_bugged_pre_save_receiver_must_raise_an_error(self):
        def callback_function(instance):
            raise Exception('ops')
        set_pre_save_receiver(ModelForSignals, callback_function)
        with pytest.raises(BadDataError):
            self.ddf.get(ModelForSignals)


class PostSaveTest(DDFTestCase):
    def test_set_post_save_receiver(self):
        def callback_function(instance):
            pass
        set_post_save_receiver(ModelForSignals, callback_function)
        callback_function = lambda x: x
        set_post_save_receiver(ModelForSignals, callback_function)

    def test_post_save_receiver_must_raise_an_error_if_first_parameter_is_not_a_model_class(self):
        callback_function = lambda x: x
        with pytest.raises(InvalidReceiverError):
            set_post_save_receiver(str, callback_function)

    def test_post_save_receiver_must_raise_an_error_if_it_is_not_a_function(self):
        with pytest.raises(InvalidReceiverError):
            set_post_save_receiver(ModelForSignals, '')

    def test_post_save_receiver_must_raise_an_error_if_it_is_not_an_only_one_argument_function(self):
        callback_function = lambda x, y: x
        with pytest.raises(InvalidReceiverError):
            set_post_save_receiver(ModelForSignals, callback_function)

    def test_pre_save_receiver_must_be_executed_before_saving(self):
        def callback_function(instance):
            if instance.id is None:
                raise Exception('ops, instance not saved')
            self.ddf.get(ModelForSignals2)
        set_post_save_receiver(ModelForSignals, callback_function)
        self.ddf.get(ModelForSignals)
        assert ModelForSignals2.objects.count() == 1

    def test_bugged_post_save_receiver_must_raise_an_error(self):
        def callback_function(instance):
            raise Exception('ops')
        set_post_save_receiver(ModelForSignals, callback_function)
        with pytest.raises(BadDataError):
            self.ddf.get(ModelForSignals)


class ExceptionsLayoutMessagesTest(DDFTestCase):
    def test_UnsupportedFieldError(self):
        try:
            self.ddf.new(ModelWithUnsupportedField)
            self.fail()
        except UnsupportedFieldError as e:
            assert """django_dynamic_fixture.models_test.ModelWithUnsupportedField.z""" in str(e)

    def test_BadDataError(self):
        self.ddf = DynamicFixture(data_fixture, ignore_fields=['required', 'required_with_default'])
        try:
            self.ddf.get(ModelForIgnoreList)
            self.fail()
        except BadDataError as e:
            assert 'IntegrityError' in str(e), str(e)
            assert 'NULL' in str(e).upper(), str(e)

    def test_InvalidConfigurationError(self):
        try:
            self.ddf.new(ModelWithNumbers, integer=lambda x: ''.invalidmethod())
            self.fail()
        except InvalidConfigurationError as e:
            assert 'django_dynamic_fixture.models_test.ModelWithNumbers.integer' in str(e)
            assert 'AttributeError' in str(e)
            assert 'invalidmethod' in str(e)

    def test_InvalidManyToManyConfigurationError(self):
        try:
            self.ddf.get(ModelWithRelationships, manytomany='a')
            self.fail()
        except InvalidManyToManyConfigurationError as e:
            assert """('Field: manytomany', 'a')""" == str(e)

    def test_InvalidModelError(self):
        try:
            self.ddf.get(ModelAbstract)
            self.fail()
        except InvalidModelError as e:
            assert """django_dynamic_fixture.models_test.ModelAbstract""" == str(e)

    def test_InvalidModelError_for_common_object(self):
        class MyClass(object): pass
        try:
            self.ddf.new(MyClass)
            self.fail()
        except InvalidModelError as e:
            assert """django_dynamic_fixture.tests.test_ddf.MyClass""" == str(e)


class SanityTest(DDFTestCase):
    def test_create_lots_of_models_to_verify_data_unicity_errors(self):
        for i in range(1000):
            self.ddf.get(ModelWithNumbers)


class AvoidNameCollisionTest(DDFTestCase):
    def test_avoid_common_name_instance(self):
        self.ddf = DynamicFixture(data_fixture, fill_nullable_fields=False)
        instance = self.ddf.new(ModelWithCommonNames)
        assert instance.instance != None

        instance = self.ddf.new(ModelWithCommonNames, instance=3)
        assert instance.instance == 3

        instance = self.ddf.get(ModelWithCommonNames)
        assert instance.instance != None

        instance = self.ddf.get(ModelWithCommonNames, instance=4)
        assert instance.instance == 4

    def test_avoid_common_name_field(self):
        self.ddf = DynamicFixture(data_fixture, fill_nullable_fields=False)
        instance = self.ddf.new(ModelWithCommonNames)
        assert instance.field != None

        instance = self.ddf.new(ModelWithCommonNames, field=5)
        assert instance.field == 5

        instance = self.ddf.get(ModelWithCommonNames)
        assert instance.field != None

        instance = self.ddf.get(ModelWithCommonNames, field=6)
        assert instance.field == 6
