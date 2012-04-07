# -*- coding: utf-8 -*-

from django.test import TestCase
from django.db import models

from django_dynamic_fixture import N, G
from django_dynamic_fixture.models import *
from django_dynamic_fixture.django_helper import *


class DjangoHelperAppsTest(TestCase):
    def test_get_apps_must_return_all_installed_apps(self):
        self.assertEquals(1, len(get_apps()))

    def test_get_apps_may_be_filtered_by_app_names(self):
        self.assertEquals(1, len(get_apps(application_labels=['django_dynamic_fixture'])))

    def test_get_apps_may_ignore_some_apps(self):
        self.assertEquals(0, len(get_apps(exclude_application_labels=['django_dynamic_fixture'])))

    def test_app_name_must_be_valid(self):
        self.assertRaises(Exception, get_apps, application_labels=['x'])
        self.assertRaises(Exception, get_apps, exclude_application_labels=['x'])

    def test_get_app_name_must(self):
        self.assertEquals('django_dynamic_fixture', get_app_name(get_apps()[0]))

    def test_get_models_of_an_app_must(self):
        models_ddf = get_models_of_an_app(get_apps()[0])
        self.assertTrue(models_ddf > 0)
        self.assertTrue(ModelWithNumbers in models_ddf)


class DjangoHelperModelsTest(TestCase):
    def test_get_model_name(self):
        class MyModel(models.Model): pass
        self.assertEquals('MyModel', get_model_name(MyModel))

    def test_get_unique_model_name(self):
        class MyModel(models.Model): pass
        self.assertEquals('django_dynamic_fixture.tests.test_django_helper.MyModel', get_unique_model_name(MyModel))

    def test_get_fields_from_model(self):
        class Model4GetFields(models.Model):
            integer = models.IntegerField()
        fields = get_fields_from_model(Model4GetFields)
        self.assertTrue(get_field_by_name_or_raise(Model4GetFields, 'id') in fields)
        self.assertTrue(get_field_by_name_or_raise(Model4GetFields, 'integer') in fields)

    def test_get_local_fields(self):
        class ModelForGetLocalFields(models.Model):
            integer = models.IntegerField()
        fields = get_local_fields(ModelForGetLocalFields)
        self.assertTrue(get_field_by_name_or_raise(ModelForGetLocalFields, 'id') in fields)
        self.assertTrue(get_field_by_name_or_raise(ModelForGetLocalFields, 'integer') in fields)

    def test_get_field_names_of_model(self):
        class Model4GetFieldNames(models.Model):
            smallinteger = models.SmallIntegerField()
        fields = get_field_names_of_model(Model4GetFieldNames)
        self.assertTrue('smallinteger' in fields)
        self.assertTrue('unknown' not in fields)

    def test_get_many_to_many_fields_from_model(self):
        class ModelRelated(models.Model): pass
        class ModelWithM2M(models.Model):
            manytomany = models.ManyToManyField('ModelRelated', related_name='m2m')
        fields = get_many_to_many_fields_from_model(ModelWithM2M)
        self.assertTrue(get_field_by_name_or_raise(ModelWithM2M, 'manytomany') in fields)
        self.assertTrue(get_field_by_name_or_raise(ModelWithM2M, 'id') not in fields)

    def test_is_model_class(self):
        class MyModel(models.Model): pass
        self.assertEquals(True, is_model_class(MyModel))
        class X(object): pass
        self.assertEquals(False, is_model_class(X))

    def test_is_model_abstract(self):
        class AbstractModel(models.Model):
            class Meta:
                abstract = True
        self.assertEquals(True, is_model_abstract(AbstractModel))

        class ConcreteModel(models.Model):
            class Meta:
                abstract = False
        self.assertEquals(False, is_model_abstract(ConcreteModel))

    def test_is_model_managed(self):
        class NotManagedModel(models.Model):
            class Meta:
                managed = False
        self.assertEquals(False, is_model_managed(NotManagedModel))

        class ManagedModel(models.Model):
            class Meta:
                managed = True
        self.assertEquals(True, is_model_managed(ManagedModel))

    def test_model_has_the_field(self):
        class ModelWithWithoutFields(models.Model):
            integer = models.IntegerField()
            selfforeignkey = models.ForeignKey('self', null=True)
            manytomany = models.ManyToManyField('self', related_name='m2m')
        self.assertEquals(True, model_has_the_field(ModelWithWithoutFields, 'integer'))
        self.assertEquals(True, model_has_the_field(ModelWithWithoutFields, 'selfforeignkey'))
        self.assertEquals(True, model_has_the_field(ModelWithWithoutFields, 'manytomany'))
        self.assertEquals(False, model_has_the_field(ModelWithWithoutFields, 'x'))


class DjangoHelperFieldsTest(TestCase):
    def test_get_unique_field_name(self):
        class Model4GetUniqueFieldName(models.Model):
            integer = models.IntegerField()
        field = get_field_by_name_or_raise(Model4GetUniqueFieldName, 'integer')
        self.assertEquals('django_dynamic_fixture.tests.test_django_helper.Model4GetUniqueFieldName.integer', get_unique_field_name(field))

    def test_get_related_model(self):
        class ModelRelated(models.Model): pass
        class Model4GetRelatedModel(models.Model):
            fk = models.ForeignKey(ModelRelated)
        self.assertEquals(ModelRelated, get_related_model(get_field_by_name_or_raise(Model4GetRelatedModel, 'fk')))

    def test_field_is_a_parent_link(self):
        class ModelParent(models.Model): pass
        class Model4FieldIsParentLink(ModelParent):
            o2o_with_parent_link = models.OneToOneField(ModelParent, parent_link=True, related_name='my_custom_ref_x')
        class Model4FieldIsParentLink2(ModelParent):
            o2o_without_parent_link = models.OneToOneField(ModelParent, parent_link=False, related_name='my_custom_ref_y')
        # FIXME
        #self.assertEquals(True, field_is_a_parent_link(get_field_by_name_or_raise(Model4FieldIsParentLink, 'o2o_with_parent_link')))
        self.assertEquals(False, field_is_a_parent_link(get_field_by_name_or_raise(Model4FieldIsParentLink2, 'o2o_without_parent_link')))

    def test_field_has_choices(self):
        class Model4FieldHasChoices(models.Model):
            with_choices = models.IntegerField(choices=((1, 1), (2, 2)))
            without_choices = models.IntegerField()
        self.assertEquals(True, field_has_choices(get_field_by_name_or_raise(Model4FieldHasChoices, 'with_choices')))
        self.assertEquals(False, field_has_choices(get_field_by_name_or_raise(Model4FieldHasChoices, 'without_choices')))

    def test_field_has_default_value(self):
        class Model4FieldHasDefault(models.Model):
            with_default = models.IntegerField(default=1)
            without_default = models.IntegerField()
        self.assertEquals(True, field_has_default_value(get_field_by_name_or_raise(Model4FieldHasDefault, 'with_default')))
        self.assertEquals(False, field_has_default_value(get_field_by_name_or_raise(Model4FieldHasDefault, 'without_default')))

    def test_field_is_unique(self):
        class Model4FieldMustBeUnique(models.Model):
            unique = models.IntegerField(unique=True)
            not_unique = models.IntegerField()
        self.assertEquals(True, field_is_unique(get_field_by_name_or_raise(Model4FieldMustBeUnique, 'unique')))
        self.assertEquals(False, field_is_unique(get_field_by_name_or_raise(Model4FieldMustBeUnique, 'not_unique')))

    def test_is_key_field(self):
        class ModelForKeyField(models.Model):
            integer = models.IntegerField()
        self.assertEquals(True, is_key_field(get_field_by_name_or_raise(ModelForKeyField, 'id')))
        self.assertEquals(False, is_key_field(get_field_by_name_or_raise(ModelForKeyField, 'integer')))

    def test_is_relationship_field(self):
        class ModelForRelationshipField(models.Model):
            fk = models.ForeignKey('self')
            one2one = models.OneToOneField('self')
        self.assertEquals(True, is_relationship_field(get_field_by_name_or_raise(ModelForRelationshipField, 'fk')))
        self.assertEquals(True, is_relationship_field(get_field_by_name_or_raise(ModelForRelationshipField, 'one2one')))
        self.assertEquals(False, is_relationship_field(get_field_by_name_or_raise(ModelForRelationshipField, 'id')))

    def test_is_file_field(self):
        class ModelForFileField(models.Model):
            filefield = models.FileField()
        self.assertEquals(True, is_file_field(get_field_by_name_or_raise(ModelForFileField, 'filefield')))
        self.assertEquals(False, is_file_field(get_field_by_name_or_raise(ModelForFileField, 'id')))


class PrintFieldValuesTest(TestCase):
    def test_model_not_saved_do_not_raise_an_exception(self):
        instance = N(ModelWithNumbers)
        print_field_values(instance)

    def test_model_saved_do_not_raise_an_exception(self):
        instance = G(ModelWithNumbers)
        print_field_values(instance)

    def test_print_accept_list_of_models_too(self):
        instances = G(ModelWithNumbers, n=2)
        print_field_values(instances)
        print_field_values([G(ModelWithNumbers), G(ModelWithNumbers)])

    def test_print_accept_a_queryset_too(self):
        G(ModelWithNumbers, n=2)
        print_field_values(ModelWithNumbers.objects.all())

