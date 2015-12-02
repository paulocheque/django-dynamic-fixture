# -*- coding: utf-8 -*-

from django.test import TestCase
from django.db import models

from django_dynamic_fixture import N, G
from django_dynamic_fixture.models_test import *
from django_dynamic_fixture.django_helper import *


class DjangoHelperAppsTest(TestCase):
    def test_get_apps_must_return_all_installed_apps(self):
        self.assertTrue(len(get_apps()) >= 1)

    def test_get_apps_may_be_filtered_by_app_names(self):
        apps = get_apps(application_labels=['django_dynamic_fixture'])
        self.assertEquals(1, len(apps))

    def test_get_apps_may_ignore_some_apps(self):
        apps = len(get_apps(exclude_application_labels=['django_dynamic_fixture']))
        self.assertEquals(1, len(get_apps()) - apps)

    def test_app_name_must_be_valid(self):
        self.assertRaises(Exception, get_apps, application_labels=['x'])
        self.assertRaises(Exception, get_apps, exclude_application_labels=['x'])

    def test_get_app_name_must(self):
        import django_dynamic_fixture.models as ddf
        self.assertEquals('django_dynamic_fixture', get_app_name(ddf))

    def test_get_models_of_an_app_must(self):
        ddf = get_apps(application_labels=['django_dynamic_fixture'])[0]
        models_ddf = get_models_of_an_app(ddf)
        self.assertTrue(len(models_ddf) > 0)
        self.assertTrue(ModelWithNumbers in models_ddf)


class DjangoHelperModelsTest(TestCase):
    def test_get_model_name(self):
        class MyModel_test_get_model_name(models.Model): pass
        self.assertEquals('MyModel_test_get_model_name', get_model_name(MyModel_test_get_model_name))

    def test_get_unique_model_name(self):
        class MyModel_test_get_unique_model_name(models.Model): pass
        self.assertEquals('django_dynamic_fixture.tests.test_django_helper.MyModel_test_get_unique_model_name',
                          get_unique_model_name(MyModel_test_get_unique_model_name))

    def test_get_fields_from_model(self):
        class Model4GetFields_test_get_fields_from_model(models.Model):
            integer = models.IntegerField()
        fields = get_fields_from_model(Model4GetFields_test_get_fields_from_model)
        self.assertTrue(get_field_by_name_or_raise(Model4GetFields_test_get_fields_from_model, 'id') in fields)
        self.assertTrue(get_field_by_name_or_raise(Model4GetFields_test_get_fields_from_model, 'integer') in fields)

    def test_get_local_fields(self):
        class ModelForGetLocalFields_test_get_local_fields(models.Model):
            integer = models.IntegerField()
        fields = get_local_fields(ModelForGetLocalFields_test_get_local_fields)
        self.assertTrue(get_field_by_name_or_raise(ModelForGetLocalFields_test_get_local_fields, 'id') in fields)
        self.assertTrue(get_field_by_name_or_raise(ModelForGetLocalFields_test_get_local_fields, 'integer') in fields)

    def test_get_field_names_of_model(self):
        class Model4GetFieldNames_test_get_field_names_of_model(models.Model):
            smallinteger = models.SmallIntegerField()
        fields = get_field_names_of_model(Model4GetFieldNames_test_get_field_names_of_model)
        self.assertTrue('smallinteger' in fields)
        self.assertTrue('unknown' not in fields)

    def test_get_many_to_many_fields_from_model(self):
        class ModelRelated_test_get_many_to_many_fields_from_model(models.Model): pass
        class ModelWithM2M_test_get_many_to_many_fields_from_model(models.Model):
            manytomany = models.ManyToManyField('ModelRelated_test_get_many_to_many_fields_from_model', related_name='m2m')
        fields = get_many_to_many_fields_from_model(ModelWithM2M_test_get_many_to_many_fields_from_model)
        self.assertTrue(get_field_by_name_or_raise(ModelWithM2M_test_get_many_to_many_fields_from_model, 'manytomany') in fields)
        self.assertTrue(get_field_by_name_or_raise(ModelWithM2M_test_get_many_to_many_fields_from_model, 'id') not in fields)

    def test_is_model_class(self):
        class MyModel_test_is_model_class(models.Model): pass
        self.assertEquals(True, is_model_class(MyModel_test_is_model_class))
        class X(object): pass
        self.assertEquals(False, is_model_class(X))

    def test_is_model_abstract(self):
        class AbstractModel_test_is_model_abstract(models.Model):
            class Meta:
                abstract = True
        self.assertEquals(True, is_model_abstract(AbstractModel_test_is_model_abstract))

        class ConcreteModel_test_is_model_abstract(models.Model):
            class Meta:
                abstract = False
        self.assertEquals(False, is_model_abstract(ConcreteModel_test_is_model_abstract))

    def test_is_model_managed(self):
        class NotManagedModel_test_is_model_managed(models.Model):
            class Meta:
                managed = False
        self.assertEquals(False, is_model_managed(NotManagedModel_test_is_model_managed))

        class ManagedModel_test_is_model_managed(models.Model):
            class Meta:
                managed = True
        self.assertEquals(True, is_model_managed(ManagedModel_test_is_model_managed))

    def test_model_has_the_field(self):
        class ModelWithWithoutFields_test_model_has_the_field(models.Model):
            integer = models.IntegerField()
            selfforeignkey = models.ForeignKey('self', null=True)
            manytomany = models.ManyToManyField('self', related_name='m2m')
        self.assertEquals(True, model_has_the_field(ModelWithWithoutFields_test_model_has_the_field, 'integer'))
        self.assertEquals(True, model_has_the_field(ModelWithWithoutFields_test_model_has_the_field, 'selfforeignkey'))
        self.assertEquals(True, model_has_the_field(ModelWithWithoutFields_test_model_has_the_field, 'manytomany'))
        self.assertEquals(False, model_has_the_field(ModelWithWithoutFields_test_model_has_the_field, 'x'))


class DjangoHelperFieldsTest(TestCase):
    def test_get_unique_field_name(self):
        class Model4GetUniqueFieldName_test_get_unique_field_name(models.Model):
            integer = models.IntegerField()
        field = get_field_by_name_or_raise(Model4GetUniqueFieldName_test_get_unique_field_name, 'integer')
        self.assertEquals('django_dynamic_fixture.tests.test_django_helper.Model4GetUniqueFieldName_test_get_unique_field_name.integer', get_unique_field_name(field))

    def test_get_related_model(self):
        class ModelRelated_test_get_related_model(models.Model): pass
        class Model4GetRelatedModel_test_get_related_model(models.Model):
            fk = models.ForeignKey(ModelRelated_test_get_related_model)
        self.assertEquals(ModelRelated_test_get_related_model,
                          get_related_model(get_field_by_name_or_raise(Model4GetRelatedModel_test_get_related_model, 'fk')))

    def test_field_is_a_parent_link(self):
        class ModelParent_test_get_related_model(models.Model): pass
        class Model4FieldIsParentLink_test_get_related_model(ModelParent):
            o2o_with_parent_link = models.OneToOneField(ModelParent_test_get_related_model, parent_link=True, related_name='my_custom_ref_x')
        class Model4FieldIsParentLink2(ModelParent):
            o2o_without_parent_link = models.OneToOneField(ModelParent_test_get_related_model, parent_link=False, related_name='my_custom_ref_y')
        # FIXME
        #self.assertEquals(True, field_is_a_parent_link(get_field_by_name_or_raise(Model4FieldIsParentLink, 'o2o_with_parent_link')))
        self.assertEquals(False, field_is_a_parent_link(get_field_by_name_or_raise(Model4FieldIsParentLink2, 'o2o_without_parent_link')))

    def test_field_has_choices(self):
        class Model4FieldHasChoices_test_get_related_model(models.Model):
            with_choices = models.IntegerField(choices=((1, 1), (2, 2)))
            without_choices = models.IntegerField()
        self.assertEquals(True, field_has_choices(get_field_by_name_or_raise(Model4FieldHasChoices_test_get_related_model, 'with_choices')))
        self.assertEquals(False, field_has_choices(get_field_by_name_or_raise(Model4FieldHasChoices_test_get_related_model, 'without_choices')))

    def test_field_has_default_value(self):
        class Model4FieldHasDefault_test_field_has_default_value(models.Model):
            with_default = models.IntegerField(default=1)
            without_default = models.IntegerField()
        self.assertEquals(True, field_has_default_value(get_field_by_name_or_raise(Model4FieldHasDefault_test_field_has_default_value, 'with_default')))
        self.assertEquals(False, field_has_default_value(get_field_by_name_or_raise(Model4FieldHasDefault_test_field_has_default_value, 'without_default')))

    def test_field_is_unique(self):
        class Model4FieldMustBeUnique_test_field_is_unique(models.Model):
            unique = models.IntegerField(unique=True)
            not_unique = models.IntegerField()
        self.assertEquals(True, field_is_unique(get_field_by_name_or_raise(Model4FieldMustBeUnique_test_field_is_unique, 'unique')))
        self.assertEquals(False, field_is_unique(get_field_by_name_or_raise(Model4FieldMustBeUnique_test_field_is_unique, 'not_unique')))

    def test_is_key_field(self):
        class ModelForKeyField_test_is_key_field(models.Model):
            integer = models.IntegerField()
        self.assertEquals(True, is_key_field(get_field_by_name_or_raise(ModelForKeyField_test_is_key_field, 'id')))
        self.assertEquals(False, is_key_field(get_field_by_name_or_raise(ModelForKeyField_test_is_key_field, 'integer')))

    def test_is_relationship_field(self):
        class ModelForRelationshipField_test_is_relationship_field(models.Model):
            fk = models.ForeignKey('self')
            one2one = models.OneToOneField('self')
        self.assertEquals(True, is_relationship_field(get_field_by_name_or_raise(ModelForRelationshipField_test_is_relationship_field, 'fk')))
        self.assertEquals(True, is_relationship_field(get_field_by_name_or_raise(ModelForRelationshipField_test_is_relationship_field, 'one2one')))
        self.assertEquals(False, is_relationship_field(get_field_by_name_or_raise(ModelForRelationshipField_test_is_relationship_field, 'id')))

    def test_is_file_field(self):
        class ModelForFileField_test_is_file_field(models.Model):
            filefield = models.FileField()
        self.assertEquals(True, is_file_field(get_field_by_name_or_raise(ModelForFileField_test_is_file_field, 'filefield')))
        self.assertEquals(False, is_file_field(get_field_by_name_or_raise(ModelForFileField_test_is_file_field, 'id')))


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

