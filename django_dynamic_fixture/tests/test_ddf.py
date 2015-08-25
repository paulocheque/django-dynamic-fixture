# -*- coding: utf-8 -*-
from datetime import datetime, date
from decimal import Decimal
import uuid

import django
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


try:
    from django.contrib.gis.geos import *
except ImportError:
    pass  # Django < 1.7
except ImproperlyConfigured:
    pass  # enviroment without geo libs

try:
    from django.contrib.gis.db import models as geomodel
except ImportError:
    pass  # Django < 1.7
except ImproperlyConfigured:
    pass  # enviroment without geo libs


from django.test import TestCase

from django_dynamic_fixture.models_test import *
from django_dynamic_fixture.ddf import *
from django_dynamic_fixture.ddf import _PRE_SAVE, _POST_SAVE
from django_dynamic_fixture.fixture_algorithms.sequential_fixture import SequentialDataFixture
from django_dynamic_fixture.django_helper import django_greater_than


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
        self.assertTrue(isinstance(instance, EmptyModel))
        self.assertEquals(None, instance.id)


class GetDealWithPrimaryKeyTest(DDFTestCase):
    def test_get_use_database_id_by_default(self):
        instance = self.ddf.get(EmptyModel)
        self.assertNotEquals(None, instance.id)
        self.assertNotEquals(None, instance.pk)

    def test_get_use_given_id(self):
        instance = self.ddf.new(EmptyModel, id=99998)
        self.assertEquals(99998, instance.id)
        self.assertEquals(99998, instance.pk)


class NewFullFillAttributesWithAutoDataTest(DDFTestCase):
    def test_new_fill_number_fields_with_numbers(self):
        instance = self.ddf.new(ModelWithNumbers)
        self.assertTrue(isinstance(instance.integer, int))
        self.assertTrue(isinstance(instance.smallinteger, int))
        self.assertTrue(isinstance(instance.positiveinteger, int))
        self.assertTrue(isinstance(instance.positivesmallinteger, int))
        self.assertTrue(isinstance(instance.biginteger, int))
        self.assertTrue(isinstance(instance.float, float))

    def test_new_fill_string_fields_with_text_type_strings(self):
        instance = self.ddf.new(ModelWithStrings)
        self.assertTrue(isinstance(instance.string, six.text_type))
        self.assertTrue(isinstance(instance.text, six.text_type))
        self.assertTrue(isinstance(instance.slug, six.text_type))
        self.assertTrue(isinstance(instance.commaseparated, six.text_type))

    def test_new_fill_boolean_fields_with_False_and_None(self):
        instance = self.ddf.new(ModelWithBooleans)
        self.assertEquals(False, instance.boolean)
        self.assertEquals(None, instance.nullboolean)

    def test_new_fill_time_related_fields_with_current_values(self):
        instance = self.ddf.new(ModelWithDateTimes)
        self.assertTrue(date.today() >= instance.date)
        self.assertTrue(datetime.now() >= instance.time)
        self.assertTrue(datetime.now() >= instance.datetime)

    def test_new_fill_formatted_strings_fields_with_basic_values(self):
        instance = self.ddf.new(ModelWithFieldsWithCustomValidation)
        self.assertTrue(isinstance(instance.email, six.text_type))
        self.assertTrue(isinstance(instance.url, six.text_type))
        self.assertTrue(isinstance(instance.ip, six.text_type))
        if django_greater_than('1.4'):
            self.assertTrue(isinstance(instance.ipv6, six.text_type))

    def test_new_fill_file_fields_with_basic_strings(self):
        instance = self.ddf.new(ModelWithFileFields)
        self.assertTrue(isinstance(instance.filepath, six.text_type))
        self.assertTrue(isinstance(instance.file.path, six.text_type))
        try:
            import pil
            # just test it if the PIL package is installed
            self.assertTrue(isinstance(instance.image, str))
        except ImportError:
            pass

    def test_new_fill_binary_fields_with_basic_data(self):
        if django_greater_than('1.6'):
            value = b'\x00\x46\xFE'
            instance = self.ddf.new(ModelWithBinary, binary=value)
            self.assertEqual(bytes(instance.binary), bytes(value))

            instance = self.ddf.get(ModelWithBinary)
            if six.PY3:
                self.assertTrue(isinstance(instance.binary, six.binary_type), msg=type(instance.binary))
            else:
                self.assertTrue(isinstance(instance.binary, (six.binary_type, str, unicode)), msg=type(instance.binary))


class NewFullFillAttributesWithDefaultDataTest(DDFTestCase):
    def test_fill_field_with_default_data(self):
        instance = self.ddf.new(ModelWithDefaultValues)
        self.assertEquals(3, instance.integer_with_default)

    def test_fill_field_with_possible_choices(self):
        instance = self.ddf.new(ModelWithDefaultValues)
        self.assertEquals('a', instance.string_with_choices)

    def test_fill_field_with_default_value_even_if_field_is_foreign_key(self):
        instance = self.ddf.new(ModelWithDefaultValues)
        self.assertEquals(None, instance.foreign_key_with_default)

    def test_fill_field_with_default_data_and_choices_must_consider_default_data_instead_choices(self):
        instance = self.ddf.new(ModelWithDefaultValues)
        self.assertEquals('b', instance.string_with_choices_and_default)

    def test_fill_field_with_possible_optgroup_choices(self):
        instance = self.ddf.new(ModelWithDefaultValues)
        self.assertEquals('a', instance.string_with_optgroup_choices)


class NewFullFillAttributesWithCustomDataTest(DDFTestCase):
    def test_fields_are_filled_with_custom_attributes(self):
        self.assertEquals(9, self.ddf.new(ModelWithNumbers, integer=9).integer)
        self.assertEquals('7', self.ddf.new(ModelWithStrings, string='7').string)
        self.assertEquals(True, self.ddf.new(ModelWithBooleans, boolean=True).boolean)

    def test_decimal_can_be_filled_by_an_string(self):
        self.ddf.get(ModelWithNumbers, decimal='9.5')
        self.assertEquals(Decimal('9.5'), ModelWithNumbers.objects.latest('id').decimal)

    def test_fields_can_be_filled_by_functions(self):
        instance = self.ddf.new(ModelWithStrings, string=lambda field: field.name)
        self.assertEquals('string', instance.string)

    def test_invalid_configuration_raise_an_error(self):
        self.assertRaises(InvalidConfigurationError, self.ddf.new, ModelWithNumbers, integer=lambda x: ''.invalidmethod())

    def test_bad_data_raise_an_error(self):
        self.ddf.get(ModelWithNumbers, integer=50000)
        self.assertRaises(BadDataError, self.ddf.get, ModelWithNumbers, integer=50000)


class NewFullFillAttributesUsingPluginsTest(DDFTestCase):
    def test_custom_field_not_registered_must_raise_an_unsupported_field_exception(self):
        self.assertRaises(UnsupportedFieldError, self.ddf.new, ModelWithUnsupportedField)

    def test_new_fill_field_with_data_generated_by_plugins_with_dict(self):
        data_fixture.plugins = django.conf.settings.DDF_FIELD_FIXTURES
        try:
            instance = self.ddf.get(ModelForFieldPlugins)
            # self.assertEquals(123456789, instance.aaa)
            # self.assertEquals(123456789, instance.bbb)
            self.assertEquals(123456789, instance.custom_field_custom_fixture)
        finally:
            data_fixture.plugins = {}

    def test_new_fill_field_with_data_generated_by_plugins_with_direct_fuction(self):
        data_fixture.plugins = django.conf.settings.DDF_FIELD_FIXTURES
        try:
            instance = self.ddf.get(ModelForFieldPlugins)
            self.assertEquals(987654321, instance.custom_field_custom_fixture2)
        finally:
            data_fixture.plugins = {}

    # Real Custom Field
    def test_json_field_not_registered_must_raise_an_unsupported_field_exception(self):
        # jsonfield requires Django 1.4+
        if django_greater_than('1.4'):
            try:
                from jsonfield import JSONCharField, JSONField
                instance = self.ddf.new(ModelForPlugins1)
                self.assertEquals(True, False, msg='JSON fields must not be supported by default')
            except ImportError:
                pass
            except UnsupportedFieldError as e:
                pass

    def test_new_fill_json_field_with_data_generated_by_plugins(self):
        # jsonfield requires Django 1.4+
        if django_greater_than('1.4'):
            try:
                import json
                from jsonfield import JSONCharField, JSONField
                data_fixture.plugins = django.conf.settings.DDF_FIELD_FIXTURES
                try:
                    instance = self.ddf.new(ModelForPlugins1)
                    self.assertTrue(isinstance(instance.json_field1, str), msg=type(instance.json_field1))
                    self.assertTrue(isinstance(instance.json_field2, str), msg=type(instance.json_field2))
                    self.assertTrue(isinstance(json.loads(instance.json_field1), dict))
                    self.assertTrue(isinstance(json.loads(instance.json_field2), list))
                    self.assertEquals(instance.json_field1, '{"some random value": "c"}')
                    self.assertEquals(instance.json_field2, '[1, 2, 3]')
                finally:
                    data_fixture.plugins = {}
            except ImportError:
                pass


class NewIgnoringNullableFieldsTest(DDFTestCase):
    def test_new_do_not_fill_nullable_fields_if_we_do_not_want_to(self):
        self.ddf = DynamicFixture(data_fixture, fill_nullable_fields=False)
        instance = self.ddf.new(ModelForNullable)
        self.assertNotEquals(None, instance.not_nullable)
        self.assertEquals(None, instance.nullable)


class NewIgnoreFieldsInIgnoreListTest(DDFTestCase):
    def test_new_do_not_fill_ignored_fields(self):
        self.ddf = DynamicFixture(data_fixture, ignore_fields=['not_required', 'not_required_with_default'])
        instance = self.ddf.new(ModelForIgnoreList)
        self.assertEquals(None, instance.not_required)
        self.assertNotEquals(None, instance.not_required_with_default)
        # not ignored fields
        self.assertNotEquals(None, instance.required)
        self.assertNotEquals(None, instance.required_with_default)

    def test_get_raise_an_error_if_a_required_field_is_in_ignore_list(self):
        self.ddf = DynamicFixture(data_fixture, ignore_fields=['required', 'required_with_default'])
        self.assertRaises(BadDataError, self.ddf.get, ModelForIgnoreList)

    def test_ignore_fields_are_propagated_to_self_references(self):
        self.ddf = DynamicFixture(data_fixture, ignore_fields=['not_required', 'nullable'])
        instance = self.ddf.new(ModelForIgnoreList)
        self.assertEquals(None, instance.not_required)
        self.assertEquals(None, instance.self_reference.not_required)

    def test_ignore_fields_are_not_propagated_to_different_references(self):
        self.ddf = DynamicFixture(data_fixture, ignore_fields=['not_required', 'nullable'])
        instance = self.ddf.new(ModelForIgnoreList)
        self.assertNotEquals(None, instance.different_reference.nullable)

    def test_ignore_fields_are_not_ignored_if_explicitely_given(self):
        self.ddf = DynamicFixture(data_fixture, not_required=3, ignore_fields=['not_required', 'nullable'])
        instance = self.ddf.new(ModelForIgnoreList)
        self.assertEqual(3, instance.not_required)


class NewAlsoCreatesRelatedObjectsTest(DDFTestCase):
    def test_new_fill_foreignkey_fields(self):
        instance = self.ddf.new(ModelWithRelationships)
        self.assertTrue(isinstance(instance.foreignkey, ModelRelated))

    def test_new_fill_onetoone_fields(self):
        instance = self.ddf.new(ModelWithRelationships)
        self.assertTrue(isinstance(instance.onetoone, ModelRelated))

    def test_new_deal_with_default_values(self):
        instance = self.ddf.new(ModelWithRelationships)
        self.assertTrue(isinstance(instance.foreignkey_with_default, ModelRelated), msg=str(type(instance.foreignkey_with_default)))

    def test_new_deal_with_id_default_values(self):
        instance = self.ddf.new(ModelWithRelationships)
        self.assertTrue(isinstance(instance.foreignkey_with_id_default, ModelRelated), msg=str(type(instance.foreignkey_with_default)))

#        TODO
#    def test_new_fill_genericrelations_fields(self):
#        instance = self.ddf.new(ModelWithRelationships)
#        self.assertTrue(isinstance(instance.foreignkey, ModelRelated))


class NewCanCreatesCustomizedRelatedObjectsTest(DDFTestCase):
    def test_customizing_nullable_fields_for_related_objects(self):
        instance = self.ddf.new(ModelWithRelationships, selfforeignkey=DynamicFixture(data_fixture, fill_nullable_fields=False))
        self.assertTrue(isinstance(instance.integer, int))
        self.assertEquals(None, instance.selfforeignkey.integer)


class NewDealWithSelfReferencesTest(DDFTestCase):
    def test_new_create_by_default_only_1_lap_in_cycle(self):
        instance = self.ddf.new(ModelWithRelationships)
        self.assertNotEquals(None, instance.selfforeignkey) # 1 cycle
        self.assertEquals(None, instance.selfforeignkey.selfforeignkey) # 2 cycles

    def test_new_create_n_laps_in_cycle(self):
        self.ddf = DynamicFixture(data_fixture, number_of_laps=2)
        instance = self.ddf.new(ModelWithRelationships)
        self.assertNotEquals(None, instance.selfforeignkey) # 1 cycle
        self.assertNotEquals(None, instance.selfforeignkey.selfforeignkey) # 2 cycles
        self.assertEquals(None, instance.selfforeignkey.selfforeignkey.selfforeignkey) # 3 cycles


class GetFullFilledModelInstanceAndPersistTest(DDFTestCase):
    def test_get_create_and_save_a_full_filled_instance_of_the_model(self):
        instance = self.ddf.get(ModelWithRelationships)
        self.assertTrue(isinstance(instance, ModelWithRelationships))
        self.assertNotEquals(None, instance.id)
        # checking unique problems
        another_instance = self.ddf.get(ModelWithRelationships)
        self.assertTrue(isinstance(another_instance, ModelWithRelationships))
        self.assertNotEquals(None, another_instance.id)

    def test_get_create_and_save_related_fields(self):
        instance = self.ddf.get(ModelWithRelationships)
        self.assertNotEquals(None, instance.selfforeignkey)
        self.assertNotEquals(None, instance.foreignkey)
        self.assertNotEquals(None, instance.onetoone)


class ManyToManyRelationshipTest(DDFTestCase):
    def test_new_ignore_many_to_many_configuratios(self):
        instance = self.ddf.new(ModelWithRelationships, manytomany=3)
        instance.save()
        self.assertEquals(0, instance.manytomany.all().count())

    def test_get_ignore_many_to_many_configuratios(self):
        instance = self.ddf.get(ModelWithRelationships, manytomany=3)
        self.assertEquals(3, instance.manytomany.all().count())

    def test_many_to_many_configuratios_accept_list_of_dynamic_filters(self):
        instance = self.ddf.get(ModelWithRelationships, manytomany=[DynamicFixture(data_fixture, integer=1000), DynamicFixture(data_fixture, integer=1001)])
        self.assertEquals(2, instance.manytomany.all().count())
        self.assertEquals(1000, instance.manytomany.all()[0].integer)
        self.assertEquals(1001, instance.manytomany.all()[1].integer)

    def test_many_to_many_configuratios_accept_list_of_instances(self):
        b1 = self.ddf.get(ModelRelated, integer=1000)
        b2 = self.ddf.get(ModelRelated, integer=1001)
        instance = self.ddf.get(ModelWithRelationships, manytomany=[b1, b2])
        self.assertEquals(2, instance.manytomany.all().count())
        objs = instance.manytomany.all().order_by('integer')
        self.assertEquals(1000, objs[0].integer)
        self.assertEquals(1001, objs[1].integer)

    def test_invalid_many_to_many_configuration(self):
        self.assertRaises(InvalidManyToManyConfigurationError, self.ddf.get, ModelWithRelationships, manytomany='a')

    def test_many_to_many_through(self):
        b1 = self.ddf.get(ModelRelated, integer=1000)
        b2 = self.ddf.get(ModelRelated, integer=1001)
        instance = self.ddf.get(ModelWithRelationships, manytomany_through=[b1, b2])
        objs = instance.manytomany_through.all().order_by('integer')
        self.assertEquals(2, objs.count())
        self.assertEquals(1000, objs[0].integer)
        self.assertEquals(1001, objs[1].integer)


class NewDealWithCyclicDependenciesTest(DDFTestCase):
    def test_new_create_by_default_only_1_lap_in_cycle(self):
        c = self.ddf.new(ModelWithCyclicDependency)
        self.assertNotEquals(None, c.d) # 1 cycle
        self.assertEquals(None, c.d.c) # 2 cycles

    def test_new_create_n_laps_in_cycle(self):
        self.ddf = DynamicFixture(data_fixture, number_of_laps=2)
        c = self.ddf.new(ModelWithCyclicDependency)
        self.assertNotEquals(None, c.d)
        self.assertNotEquals(None, c.d.c) # 1 cycle
        self.assertNotEquals(None, c.d.c.d) # 2 cycles
        self.assertEquals(None, c.d.c.d.c) # 3 cycles


class NewDealWithInheritanceTest(DDFTestCase):
    def test_new_must_not_raise_an_error_if_model_is_abstract(self):
        self.ddf.new(ModelAbstract) # it does not raise an exceptions

    def test_get_must_raise_an_error_if_model_is_abstract(self):
        self.assertRaises(InvalidModelError, self.ddf.get, ModelAbstract)

    def test_get_must_fill_parent_fields_too(self):
        instance = self.ddf.get(ModelParent)
        self.assertTrue(isinstance(instance.integer, int))
        self.assertEquals(1, ModelParent.objects.count())

    def test_get_must_fill_grandparent_fields_too(self):
        instance = self.ddf.get(ModelChild)
        self.assertTrue(isinstance(instance.integer, int))
        self.assertEquals(1, ModelParent.objects.count())
        self.assertEquals(1, ModelChild.objects.count())

    def test_get_must_ignore_parent_link_attributes_but_the_parent_object_must_be_created(self):
        instance = self.ddf.get(ModelChildWithCustomParentLink)
        self.assertTrue(isinstance(instance.integer, int))
        self.assertEquals(1, ModelParent.objects.count())
        self.assertEquals(1, ModelChildWithCustomParentLink.objects.count())
        self.assertNotEquals(None, instance.my_custom_ref.id)
        self.assertNotEquals(None, instance.my_custom_ref.my_custom_ref_x.id)

    # TODO: need to check these tests. Here we are trying to simulate a bug with parent_link attribute
    def test_get_0(self):
        instance = self.ddf.get(ModelWithRefToParent)
        self.assertEquals(1, ModelWithRefToParent.objects.count())
        self.assertEquals(1, ModelParent.objects.count())
        self.assertTrue(isinstance(instance.parent, ModelParent))

    def test_get_1(self):
        instance = self.ddf.get(ModelWithRefToParent, parent=self.ddf.get(ModelChild))
        self.assertEquals(1, ModelWithRefToParent.objects.count())
        self.assertEquals(1, ModelParent.objects.count())
        self.assertEquals(1, ModelChild.objects.count())
        self.assertTrue(isinstance(instance.parent, ModelChild))

    def test_get_2(self):
        instance = self.ddf.get(ModelWithRefToParent, parent=self.ddf.get(ModelChildWithCustomParentLink))
        self.assertEquals(1, ModelWithRefToParent.objects.count())
        self.assertEquals(1, ModelParent.objects.count())
        self.assertEquals(1, ModelChildWithCustomParentLink.objects.count())
        self.assertTrue(isinstance(instance.parent, ModelChildWithCustomParentLink))


class CustomFieldsTest(DDFTestCase):
    def test_new_field_that_extends_django_field_must_be_supported(self):
        instance = self.ddf.new(ModelWithCustomFields)
        self.assertEquals(1, instance.x)

    def test_unsupported_field_is_filled_with_null_if_it_is_possible(self):
        instance = self.ddf.new(ModelWithCustomFields)
        self.assertEquals(None, instance.y)

    def test_unsupported_field_raise_an_error_if_it_does_not_accept_null_value(self):
        self.assertRaises(UnsupportedFieldError, self.ddf.new, ModelWithUnsupportedField)

    def test_new_field_that_double_inherits_django_field_must_be_supported(self):
        instance = self.ddf.new(ModelWithCustomFieldsMultipleInheritance)
        self.assertEquals(1, instance.x)


class ComplexFieldsTest(DDFTestCase):
    def test_x(self):
        if django_greater_than('1.8'):
            instance = self.ddf.new(ModelForUUID)
            self.assertTrue(isinstance(instance.uuid, uuid.UUID))


if settings.DDF_TEST_GEODJANGO:
    class GeoDjangoFieldsTest(DDFTestCase):
        def test_geodjango_fields(self):
            if django_greater_than('1.7'):
                instance = self.ddf.new(ModelForGeoDjango)
                self.assertTrue(isinstance(instance.geometry, GEOSGeometry), msg=str(type(instance.geometry)))
                self.assertTrue(isinstance(instance.point, Point))
                self.assertTrue(isinstance(instance.line_string, LineString))
                self.assertTrue(isinstance(instance.polygon, Polygon))
                self.assertTrue(isinstance(instance.multi_point, MultiPoint))
                self.assertTrue(isinstance(instance.multi_line_string, MultiLineString))
                self.assertTrue(isinstance(instance.multi_polygon, MultiPolygon))
                self.assertTrue(isinstance(instance.geometry_collection, GeometryCollection))


class ModelValidatorsTest(DDFTestCase):
    def test_it_must_create_if_validation_is_disabled(self):
        instance = self.ddf.get(ModelWithValidators, field_validator='nok', clean_validator='nok')
        self.ddf.validate_models = False
        self.assertEquals('nok', instance.field_validator)
        self.assertEquals('nok', instance.clean_validator)

    def test_it_must_create_if_there_is_no_validation_errors(self):
        instance = self.ddf.get(ModelWithValidators, field_validator='ok', clean_validator='ok')
        self.ddf.validate_models = True
        self.assertEquals('ok', instance.field_validator)
        self.assertEquals('ok', instance.clean_validator)

    def test_it_must_raise_a_bad_data_error_if_data_is_not_valid(self):
        self.ddf.validate_models = True
        self.ddf.get(ModelWithValidators, field_validator='nok', clean_validator='ok')
        self.assertRaises(BadDataError, self.ddf.get, ModelWithValidators, field_validator='ok', clean_validator='nok')


class ConfigurationValidatorTest(DDFTestCase):
    def test_it_must_raise_a_bad_data_error_if_data_is_not_valid(self):
        self.ddf.validate_args = True
        self.assertRaises(InvalidConfigurationError, self.ddf.get, EmptyModel, unexistent_field='x')


class DisableAutoGeneratedDateTimesTest(DDFTestCase):
    def test_auto_generated_datetimes_must_be_respected_if_nothing_is_specified(self):
        instance = self.ddf.get(ModelWithAutoDateTimes)
        self.assertEquals(datetime.today().date(), instance.auto_now_add)
        self.assertEquals(datetime.today().date(), instance.auto_now)

    def test_it_must_ignore_auto_generated_datetime_if_a_custom_value_is_provided(self):
        instance = self.ddf.get(ModelWithAutoDateTimes, auto_now_add=date(2000, 12, 31))
        self.assertEquals(date(2000, 12, 31), instance.auto_now_add)

        instance = self.ddf.get(ModelWithAutoDateTimes, auto_now=date(2000, 12, 31))
        self.assertEquals(date(2000, 12, 31), instance.auto_now)

    def test_checking_if_implementation_works_for_m2m_fields_too(self):
        instance = self.ddf.get(ModelWithAutoDateTimes, manytomany=[DynamicFixture(data_fixture, auto_now_add=date(2000, 12, 31))])
        self.assertEquals(date(2000, 12, 31), instance.manytomany.all()[0].auto_now_add)

        instance = self.ddf.get(ModelWithAutoDateTimes, manytomany=[DynamicFixture(data_fixture, auto_now=date(2000, 12, 31))])
        self.assertEquals(date(2000, 12, 31), instance.manytomany.all()[0].auto_now)



class CopyTest(DDFTestCase):
    def test_it_should_copy_from_model_fields(self):
        instance = self.ddf.get(ModelForCopy, int_a=Copier('int_b'), int_b=3)
        self.assertEquals(3, instance.int_a)

    def test_simple_scenario(self):
        instance = self.ddf.get(ModelForCopy, int_b=Copier('int_a'))
        self.assertEquals(instance.int_b, instance.int_a)

    def test_order_of_attributes_must_be_superfluous(self):
        instance = self.ddf.get(ModelForCopy, int_a=Copier('int_b'))
        self.assertEquals(instance.int_a, instance.int_b)

    def test_it_should_deal_with_multiple_copiers(self):
        instance = self.ddf.get(ModelForCopy, int_a=Copier('int_b'), int_c=Copier('int_d'))
        self.assertEquals(instance.int_a, instance.int_b)
        self.assertEquals(instance.int_c, instance.int_d)

    def test_multiple_copiers_can_depend_of_one_field(self):
        instance = self.ddf.get(ModelForCopy, int_a=Copier('int_c'), int_b=Copier('int_c'))
        self.assertEquals(instance.int_a, instance.int_c)
        self.assertEquals(instance.int_b, instance.int_c)

    def test_it_should_deal_with_dependent_copiers(self):
        instance = self.ddf.get(ModelForCopy, int_a=Copier('int_b'), int_b=Copier('int_c'))
        self.assertEquals(instance.int_a, instance.int_b)
        self.assertEquals(instance.int_b, instance.int_c)

    def test_it_should_deal_with_relationships(self):
        instance = self.ddf.get(ModelForCopy, int_a=Copier('e.int_e'))
        self.assertEquals(instance.int_a, instance.e.int_e)

        instance = self.ddf.get(ModelForCopy, int_a=Copier('e.int_e'), e=DynamicFixture(data_fixture, int_e=5))
        self.assertEquals(5, instance.int_a)

    def test_it_should_raise_a_bad_data_error_if_value_is_invalid(self):
        self.assertRaises(BadDataError, self.ddf.get, ModelForCopy, int_a=Copier('int_b'), int_b=None)

    def test_it_should_raise_a_invalid_configuration_error_if_expression_is_bugged(self):
        self.assertRaises(InvalidConfigurationError, self.ddf.get, ModelForCopy, int_a=Copier('invalid_field'))
        self.assertRaises(InvalidConfigurationError, self.ddf.get, ModelForCopy, int_a=Copier('int_b.invalid_field'))

    def test_it_should_raise_a_invalid_configuration_error_if_copier_has_cyclic_dependency(self):
        self.assertRaises(InvalidConfigurationError, self.ddf.get, ModelForCopy, int_a=Copier('int_b'), int_b=Copier('int_a'))


class ShelveAndLibraryTest(DDFTestCase):
    def test_shelve_store_the_current_configuration_as_default_configuration(self):
        self.ddf.use_library = False
        instance = self.ddf.get(ModelForLibrary, integer=1000, shelve=True)
        self.assertEquals(1000, instance.integer)
        self.ddf.use_library = True
        instance = self.ddf.get(ModelForLibrary)
        self.assertEquals(1000, instance.integer)

    def test_do_not_use_library_if_the_programmer_do_not_want_to(self):
        self.ddf.use_library = False
        self.ddf.get(ModelForLibrary, integer=1000, shelve=True)
        self.ddf.use_library = False
        instance = self.ddf.get(ModelForLibrary)
        self.assertNotEquals(1000, instance.integer)

    def test_shelve_may_be_overrided(self):
        self.ddf.use_library = False
        self.ddf.get(ModelForLibrary, integer=1000, shelve=True)
        self.ddf.get(ModelForLibrary, integer=1001, shelve=True)
        self.ddf.use_library = True
        instance = self.ddf.get(ModelForLibrary)
        self.assertEquals(1001, instance.integer)

    def test_it_must_NOT_raise_an_error_if_user_try_to_use_a_not_saved_default_configuration(self):
        self.ddf.use_library = True
        self.ddf.get(ModelForLibrary)

    def test_it_must_raise_an_error_if_try_to_set_a_static_value_to_a_field_with_unicity(self):
        self.assertRaises(InvalidConfigurationError, self.ddf.get, ModelForLibrary, integer_unique=1000, shelve=True)

    def test_it_must_accept_dynamic_values_for_fields_with_unicity(self):
        self.ddf.get(ModelForLibrary, integer_unique=lambda field: 1000, shelve=True)

    def test_it_must_NOT_propagate_shelve_for_internal_dependencies(self):
        self.ddf.get(ModelForLibrary, foreignkey=DynamicFixture(data_fixture, integer=1000), shelve=True)
        instance = self.ddf.get(ModelForLibrary2)
        self.assertNotEquals(1000, instance.integer)

    def test_it_must_propagate_use_library_for_internal_dependencies(self):
        self.ddf.use_library = True
        self.ddf.get(ModelForLibrary, integer=1000, shelve=True)
        self.ddf.get(ModelForLibrary2, integer=1000, shelve=True)
        instance = self.ddf.get(ModelForLibrary)
        self.assertEquals(1000, instance.foreignkey.integer)

#    def test_shelve_must_store_ddf_configs_too(self):
#        self.ddf.use_library = True
#        self.ddf.fill_nullable_fields = False
#        self.ddf.get(ModelForLibrary, shelve=True)
#        self.ddf.fill_nullable_fields = True
#        instance = self.ddf.get(ModelForLibrary)
#        self.assertEquals(None, instance.integer)
#
#    def test_shelved_ddf_configs_must_NOT_be_propagated_to_another_models(self):
#        self.ddf.use_library = True
#        self.ddf.fill_nullable_fields = False
#        self.ddf.get(ModelForLibrary, shelve=True)
#        self.ddf.fill_nullable_fields = True
#        instance = self.ddf.get(ModelForLibrary)
#        self.assertEquals(None, instance.integer)
#        self.assertEquals(None, instance.foreignkey.integer)


class NamedShelveAndLibraryTest(DDFTestCase):
    def test_a_model_can_have_named_configurations(self):
        self.ddf.use_library = True
        self.ddf.get(ModelForLibrary, integer=1000, shelve='a name')
        instance = self.ddf.get(ModelForLibrary, named_shelve='a name')
        self.assertEquals(1000, instance.integer)

    def test_named_shelves_must_not_be_used_if_not_explicity_specified(self):
        self.ddf.use_library = True
        self.ddf.get(ModelForLibrary, integer=1000, shelve='a name')
        instance = self.ddf.get(ModelForLibrary)
        self.assertNotEquals(1000, instance.integer)

    def test_use_library_must_be_enable_to_use_named_shelves(self):
        self.ddf.use_library = False
        self.ddf.get(ModelForLibrary, integer=1000, shelve='a name')
        instance = self.ddf.get(ModelForLibrary, named_shelve='a name')
        self.assertNotEquals(1000, instance.integer)

    def test_a_model_can_have_many_named_shelved_configurations(self):
        self.ddf.get(ModelForLibrary, integer=1000, shelve='a name')
        self.ddf.get(ModelForLibrary, integer=1001, shelve='a name 2')

        self.ddf.use_library = True
        instance = self.ddf.get(ModelForLibrary, named_shelve='a name')
        self.assertEquals(1000, instance.integer)

        instance = self.ddf.get(ModelForLibrary, named_shelve='a name 2')
        self.assertEquals(1001, instance.integer)

    def test_it_must_raise_an_error_if_user_try_to_use_a_not_saved_configuration(self):
        self.ddf.use_library = True
        self.assertRaises(InvalidConfigurationError, self.ddf.get, ModelForLibrary, named_shelve='a name')

    def test_default_shelve_and_named_shelve_must_work_together(self):
        # regression test
        self.ddf.get(ModelForLibrary, integer=1000, shelve='a name')
        self.ddf.get(ModelForLibrary, integer=1001, shelve=True)
        self.ddf.get(ModelForLibrary, integer=1002, shelve='a name2')
        self.ddf.use_library = True
        instance = self.ddf.get(ModelForLibrary, named_shelve='a name')
        self.assertEquals(1000, instance.integer)
        instance = self.ddf.get(ModelForLibrary)
        self.assertEquals(1001, instance.integer)
        instance = self.ddf.get(ModelForLibrary, named_shelve='a name2')
        self.assertEquals(1002, instance.integer)

    def test_default_shelve_and_named_shelve_must_work_together_for_different_models(self):
        # regression test
        self.ddf.get(ModelForLibrary, integer=1000, shelve='a name')
        self.ddf.get(ModelForLibrary, integer=1001, shelve=True)
        self.ddf.get(ModelForLibrary, integer=1002, shelve='a name2')
        self.ddf.get(ModelForLibrary2, integer=2000, shelve='a name')
        self.ddf.get(ModelForLibrary2, integer=2001, shelve=True)
        self.ddf.get(ModelForLibrary2, integer=2002, shelve='a name2')
        self.ddf.use_library = True
        instance = self.ddf.get(ModelForLibrary, named_shelve='a name')
        self.assertEquals(1000, instance.integer)
        instance = self.ddf.get(ModelForLibrary)
        self.assertEquals(1001, instance.integer)
        instance = self.ddf.get(ModelForLibrary, named_shelve='a name2')
        self.assertEquals(1002, instance.integer)

        instance = self.ddf.get(ModelForLibrary2, named_shelve='a name')
        self.assertEquals(2000, instance.integer)
        instance = self.ddf.get(ModelForLibrary2)
        self.assertEquals(2001, instance.integer)
        instance = self.ddf.get(ModelForLibrary2, named_shelve='a name2')
        self.assertEquals(2002, instance.integer)


class DDFLibraryTest(TestCase):
    def setUp(self):
        self.lib = DDFLibrary()

    def test_add_and_get_configuration_without_string_name(self):
        self.lib.add_configuration(ModelForLibrary, {'a': 1})
        self.assertEquals({'a': 1}, self.lib.get_configuration(ModelForLibrary))
        self.assertEquals({'a': 1}, self.lib.get_configuration(ModelForLibrary, name=DDFLibrary.DEFAULT_KEY))
        self.assertEquals({'a': 1}, self.lib.get_configuration(ModelForLibrary, name=None))

        self.lib.add_configuration(ModelForLibrary, {'a': 2}, name=None)
        self.assertEquals({'a': 2}, self.lib.get_configuration(ModelForLibrary))
        self.assertEquals({'a': 2}, self.lib.get_configuration(ModelForLibrary, name=DDFLibrary.DEFAULT_KEY))
        self.assertEquals({'a': 2}, self.lib.get_configuration(ModelForLibrary, name=None))

        self.lib.add_configuration(ModelForLibrary, {'a': 3}, name=True)
        self.assertEquals({'a': 3}, self.lib.get_configuration(ModelForLibrary))
        self.assertEquals({'a': 3}, self.lib.get_configuration(ModelForLibrary, name=DDFLibrary.DEFAULT_KEY))
        self.assertEquals({'a': 3}, self.lib.get_configuration(ModelForLibrary, name=None))

    def test_add_and_get_configuration_with_name(self):
        self.lib.add_configuration(ModelForLibrary, {'a': 1}, name='x')
        self.assertEquals({'a': 1}, self.lib.get_configuration(ModelForLibrary, name='x'))

    def test_clear_config(self):
        self.lib.clear_configuration(ModelForLibrary) # run ok if empty
        self.lib.add_configuration(ModelForLibrary, {'a': 1})
        self.lib.add_configuration(ModelForLibrary, {'a': 2}, name='x')
        self.lib.add_configuration(ModelForLibrary2, {'a': 3})
        self.lib.clear_configuration(ModelForLibrary)
        self.assertEquals({}, self.lib.get_configuration(ModelForLibrary))
        self.assertRaises(Exception, self.lib.get_configuration, ModelForLibrary, name='x')
        self.assertEquals({'a': 3}, self.lib.get_configuration(ModelForLibrary2))

    def test_clear(self):
        self.lib.add_configuration(ModelForLibrary, {'a': 1})
        self.lib.add_configuration(ModelForLibrary, {'a': 2}, name='x')
        self.lib.add_configuration(ModelForLibrary2, {'a': 3})
        self.lib.add_configuration(ModelForLibrary2, {'a': 4}, name='x')
        self.lib.clear()
        self.assertEquals({}, self.lib.get_configuration(ModelForLibrary))
        self.assertRaises(Exception, self.lib.get_configuration, ModelForLibrary, name='x')
        self.assertEquals({}, self.lib.get_configuration(ModelForLibrary2))
        self.assertRaises(Exception, self.lib.get_configuration, ModelForLibrary2, name='x')


class ModelWithCustomValidationTest(DDFTestCase):
    def test_ddf_can_not_create_instance_of_models_with_custom_validations(self):
        self.ddf.validate_models = True
        self.assertRaises(BadDataError, self.ddf.get, ModelWithClean)
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
        self.assertRaises(InvalidReceiverError, set_pre_save_receiver, str, callback_function)

    def test_pre_save_receiver_must_raise_an_error_if_it_is_not_a_function(self):
        self.assertRaises(InvalidReceiverError, set_pre_save_receiver, ModelForSignals, '')

    def test_pre_save_receiver_must_raise_an_error_if_it_is_not_an_only_one_argument_function(self):
        callback_function = lambda x, y: x
        self.assertRaises(InvalidReceiverError, set_pre_save_receiver, ModelForSignals, callback_function)

    def test_pre_save_receiver_must_be_executed_before_saving(self):
        def callback_function(instance):
            if instance.id is not None:
                raise Exception('ops, instance already saved')
            self.ddf.get(ModelForSignals2)
        set_pre_save_receiver(ModelForSignals, callback_function)
        self.ddf.get(ModelForSignals)
        self.assertEquals(1, ModelForSignals2.objects.count())

    def test_bugged_pre_save_receiver_must_raise_an_error(self):
        def callback_function(instance):
            raise Exception('ops')
        set_pre_save_receiver(ModelForSignals, callback_function)
        self.assertRaises(BadDataError, self.ddf.get, ModelForSignals)


class PostSaveTest(DDFTestCase):
    def test_set_post_save_receiver(self):
        def callback_function(instance):
            pass
        set_post_save_receiver(ModelForSignals, callback_function)
        callback_function = lambda x: x
        set_post_save_receiver(ModelForSignals, callback_function)

    def test_post_save_receiver_must_raise_an_error_if_first_parameter_is_not_a_model_class(self):
        callback_function = lambda x: x
        self.assertRaises(InvalidReceiverError, set_post_save_receiver, str, callback_function)

    def test_post_save_receiver_must_raise_an_error_if_it_is_not_a_function(self):
        self.assertRaises(InvalidReceiverError, set_post_save_receiver, ModelForSignals, '')

    def test_post_save_receiver_must_raise_an_error_if_it_is_not_an_only_one_argument_function(self):
        callback_function = lambda x, y: x
        self.assertRaises(InvalidReceiverError, set_post_save_receiver, ModelForSignals, callback_function)

    def test_pre_save_receiver_must_be_executed_before_saving(self):
        def callback_function(instance):
            if instance.id is None:
                raise Exception('ops, instance not saved')
            self.ddf.get(ModelForSignals2)
        set_post_save_receiver(ModelForSignals, callback_function)
        self.ddf.get(ModelForSignals)
        self.assertEquals(1, ModelForSignals2.objects.count())

    def test_bugged_post_save_receiver_must_raise_an_error(self):
        def callback_function(instance):
            raise Exception('ops')
        set_post_save_receiver(ModelForSignals, callback_function)
        self.assertRaises(BadDataError, self.ddf.get, ModelForSignals)


class ExceptionsLayoutMessagesTest(DDFTestCase):
    def test_UnsupportedFieldError(self):
        try:
            self.ddf.new(ModelWithUnsupportedField)
            self.fail()
        except UnsupportedFieldError as e:
            self.assertTrue("""django_dynamic_fixture.models_test.ModelWithUnsupportedField.z""" in str(e))

    def test_BadDataError(self):
        self.ddf = DynamicFixture(data_fixture, ignore_fields=['required', 'required_with_default'])
        try:
            self.ddf.get(ModelForIgnoreList)
            self.fail()
        except BadDataError as e:
            model_msg = 'django_dynamic_fixture.models_test.ModelForIgnoreList'
            error_msg = 'django_dynamic_fixture_modelforignorelist.required may not be NULL'
            error_msg2 = 'NOT NULL constraint failed: django_dynamic_fixture_modelforignorelist.required'
            template1 = "('%s', IntegrityError('%s',))" % (model_msg, error_msg)
            template2 = "('%s', IntegrityError('%s',))" % (model_msg, error_msg2) # py34
            template3 = "('%s', IntegrityError(u'%s',))" % (model_msg, error_msg) # pypy
            template4 = "('%s', IntegrityError(u'%s',))" % (model_msg, error_msg2) # pypy
            self.assertEquals(str(e) in [template1, template2, template3, template4], True, msg=str(e))


    def test_InvalidConfigurationError(self):
        try:
            self.ddf.new(ModelWithNumbers, integer=lambda x: ''.invalidmethod())
            self.fail()
        except InvalidConfigurationError as e:
            self.assertEquals("""('django_dynamic_fixture.models_test.ModelWithNumbers.integer', AttributeError("'str' object has no attribute 'invalidmethod'",))""",
                              str(e))

    def test_InvalidManyToManyConfigurationError(self):
        try:
            self.ddf.get(ModelWithRelationships, manytomany='a')
            self.fail()
        except InvalidManyToManyConfigurationError as e:
            self.assertEquals("""('Field: manytomany', 'a')""",
                              str(e))

    def test_InvalidModelError(self):
        try:
            self.ddf.get(ModelAbstract)
            self.fail()
        except InvalidModelError as e:
            self.assertEquals("""django_dynamic_fixture.models_test.ModelAbstract""",
                              str(e))

    def test_InvalidModelError_for_common_object(self):
        class MyClass(object): pass
        try:
            self.ddf.new(MyClass)
            self.fail()
        except InvalidModelError as e:
            self.assertEquals("""django_dynamic_fixture.tests.test_ddf.MyClass""",
                              str(e))


class SanityTest(DDFTestCase):
    def test_create_lots_of_models_to_verify_data_unicity_errors(self):
        for i in range(1000):
            self.ddf.get(ModelWithNumbers)


class AvoidNameCollisionTest(DDFTestCase):
    def test_avoid_common_name_instance(self):
        self.ddf = DynamicFixture(data_fixture, fill_nullable_fields=False)
        instance = self.ddf.new(ModelWithCommonNames)
        self.assertNotEquals(None, instance.instance)

        instance = self.ddf.new(ModelWithCommonNames, instance=3)
        self.assertEquals(3, instance.instance)

        instance = self.ddf.get(ModelWithCommonNames)
        self.assertNotEquals(None, instance.instance)

        instance = self.ddf.get(ModelWithCommonNames, instance=4)
        self.assertEquals(4, instance.instance)

    def test_avoid_common_name_field(self):
        self.ddf = DynamicFixture(data_fixture, fill_nullable_fields=False)
        instance = self.ddf.new(ModelWithCommonNames)
        self.assertNotEquals(None, instance.field)

        instance = self.ddf.new(ModelWithCommonNames, field=5)
        self.assertEquals(5, instance.field)

        instance = self.ddf.get(ModelWithCommonNames)
        self.assertNotEquals(None, instance.field)

        instance = self.ddf.get(ModelWithCommonNames, field=6)
        self.assertEquals(6, instance.field)
