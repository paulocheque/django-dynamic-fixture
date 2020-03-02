# -*- coding: utf-8 -*-
from datetime import datetime, date
from decimal import Decimal
import uuid

from django.test import TestCase
import pytest

from django_dynamic_fixture.models_test import *
from django_dynamic_fixture.ddf import *
from django_dynamic_fixture.fixture_algorithms.sequential_fixture import SequentialDataFixture


data_fixture = SequentialDataFixture()


class DDFTestCase(TestCase):
    def setUp(self):
        self.ddf = DynamicFixture(data_fixture)


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
        self.ddf = DynamicFixture(data_fixture, ignore_fields=['not_required'], fk_min_depth=1, not_required=10)
        instance = self.ddf.new(ModelForIgnoreList)
        assert instance.not_required == 10
        assert instance.self_reference is not None
        assert instance.self_reference.not_required is None

    def test_ignore_fields_are_not_propagated_to_different_references(self):
        self.ddf = DynamicFixture(data_fixture, ignore_fields=['non_nullable'], different_reference=DynamicFixture(data_fixture))
        instance = self.ddf.new(ModelForIgnoreList)
        assert instance.different_reference is not None
        assert instance.different_reference.non_nullable is not None

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
        instance = self.ddf.new(ModelWithRelationships, selfforeignkey=DynamicFixture(data_fixture, fill_nullable_fields=True))
        assert instance.integer is None
        assert isinstance(instance.selfforeignkey.integer, int)


class NewDealWithSelfReferencesTest(DDFTestCase):
    def test_new_create_by_default_no_self_fks(self):
        instance = self.ddf.new(ModelWithRelationships, fill_nullable_fields=False)
        assert instance.selfforeignkey is None # no cycle
        instance = self.ddf.new(ModelWithRelationships, fill_nullable_fields=True)
        assert instance.selfforeignkey is None # no cycle

    def test_new_create_only_1_lap_in_cycle(self):
        self.ddf = DynamicFixture(data_fixture, fk_min_depth=1)
        instance = self.ddf.new(ModelWithRelationships)
        assert instance.selfforeignkey is not None # 1 cycle
        assert instance.selfforeignkey.selfforeignkey is None # 2 cycles

    def test_new_create_with_min_depth_2(self):
        self.ddf = DynamicFixture(data_fixture, fk_min_depth=2)
        instance = self.ddf.new(ModelWithRelationships)
        assert instance.selfforeignkey is not None # 1 cycle
        assert instance.selfforeignkey.selfforeignkey is not None # 2 cycles
        assert instance.selfforeignkey.selfforeignkey.selfforeignkey is None # 3 cycles

    def test_number_of_fk_cycles_does_not_break_default_non_null_fk(self):
        self.ddf = DynamicFixture(data_fixture, fk_min_depth=0)
        instance = self.ddf.new(ModelWithRefToParent)
        assert instance.parent is not None


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
        assert instance.selfforeignkey is None
        assert instance.foreignkey is not None
        assert instance.onetoone is not None
        self.ddf = DynamicFixture(data_fixture, fk_min_depth=1)
        instance = self.ddf.get(ModelWithRelationships)
        assert instance.selfforeignkey is not None


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
    def test_new_create_by_default_no_cycles(self):
        a = self.ddf.new(ModelWithCyclicDependency)
        assert a.model_b is None

    def test_new_create_only_1_lap_in_fk_cycle(self):
        self.ddf = DynamicFixture(data_fixture, fk_min_depth=1)
        a = self.ddf.get(ModelWithCyclicDependency)
        assert a.model_b.model_a is None

    def test_new_create_with_min_depth_2(self):
        self.ddf = DynamicFixture(data_fixture, fk_min_depth=2)
        a = self.ddf.get(ModelWithCyclicDependency)
        assert a.model_b.model_a.model_b is None


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


class ComplexFieldsTest(DDFTestCase):
    def test_x(self):
        instance = self.ddf.new(ModelForUUID)
        assert isinstance(instance.uuid, uuid.UUID)


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


class ModelWithCustomValidationTest(DDFTestCase):
    def test_ddf_can_not_create_instance_of_models_with_custom_validations(self):
        self.ddf.validate_models = True
        with pytest.raises(BadDataError):
            self.ddf.get(ModelWithClean)
        self.ddf.get(ModelWithClean, integer=9999) # this does not raise an exception


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
