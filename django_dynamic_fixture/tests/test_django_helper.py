# -*- coding: utf-8 -*-

from django.test import TestCase
from django.db import models
import pytest

from django_dynamic_fixture import N, G
from django_dynamic_fixture.models_test import *
from django_dynamic_fixture.django_helper import *


class DjangoHelperAppsTest(TestCase):
    def test_get_apps_must_return_all_installed_apps(self):
        assert len(get_apps()) >= 1

    def test_get_apps_may_be_filtered_by_app_names(self):
        apps = get_apps(application_labels=['django_dynamic_fixture'])
        assert len(apps) == 1

    def test_get_apps_may_ignore_some_apps(self):
        apps = len(get_apps(exclude_application_labels=['django_dynamic_fixture']))
        assert len(get_apps()) - apps == 1

    def test_app_name_must_be_valid(self):
        with pytest.raises(Exception):
            get_apps(application_labels=['x'])
        with pytest.raises(Exception):
            get_apps(exclude_application_labels=['x'])

    def test_get_app_name_must(self):
        import django_dynamic_fixture.models as ddf
        assert get_app_name(ddf) == 'django_dynamic_fixture'

    def test_get_models_of_an_app_must(self):
        ddf = get_apps(application_labels=['django_dynamic_fixture'])[0]
        models_ddf = get_models_of_an_app(ddf)
        assert len(models_ddf) > 0
        assert ModelWithNumbers in models_ddf


class DjangoHelperModelsTest(TestCase):
    def test_get_model_name(self):
        class MyModel_test_get_model_name(models.Model): pass
        assert get_model_name(MyModel_test_get_model_name) == 'MyModel_test_get_model_name'

    def test_get_unique_model_name(self):
        class MyModel_test_get_unique_model_name(models.Model): pass
        assert get_unique_model_name(MyModel_test_get_unique_model_name) == 'django_dynamic_fixture.tests.test_django_helper.MyModel_test_get_unique_model_name'

    def test_get_fields_from_model(self):
        class Model4GetFields_test_get_fields_from_model(models.Model):
            integer = models.IntegerField()
        fields = get_fields_from_model(Model4GetFields_test_get_fields_from_model)
        assert get_field_by_name_or_raise(Model4GetFields_test_get_fields_from_model, 'id') in fields
        assert get_field_by_name_or_raise(Model4GetFields_test_get_fields_from_model, 'integer') in fields

    def test_get_local_fields(self):
        class ModelForGetLocalFields_test_get_local_fields(models.Model):
            integer = models.IntegerField()
        fields = get_local_fields(ModelForGetLocalFields_test_get_local_fields)
        assert get_field_by_name_or_raise(ModelForGetLocalFields_test_get_local_fields, 'id') in fields
        assert get_field_by_name_or_raise(ModelForGetLocalFields_test_get_local_fields, 'integer') in fields

    def test_get_field_names_of_model(self):
        class Model4GetFieldNames_test_get_field_names_of_model(models.Model):
            smallinteger = models.SmallIntegerField()
        fields = get_field_names_of_model(Model4GetFieldNames_test_get_field_names_of_model)
        assert 'smallinteger' in fields
        assert 'unknown' not in fields

    def test_get_many_to_many_fields_from_model(self):
        class ModelRelated_test_get_many_to_many_fields_from_model(models.Model): pass
        class ModelWithM2M_test_get_many_to_many_fields_from_model(models.Model):
            manytomany = models.ManyToManyField('ModelRelated_test_get_many_to_many_fields_from_model', related_name='m2m')
        fields = get_many_to_many_fields_from_model(ModelWithM2M_test_get_many_to_many_fields_from_model)
        assert get_field_by_name_or_raise(ModelWithM2M_test_get_many_to_many_fields_from_model, 'manytomany') in fields
        assert get_field_by_name_or_raise(ModelWithM2M_test_get_many_to_many_fields_from_model, 'id') not in fields

    def test_is_model_class(self):
        class MyModel_test_is_model_class(models.Model): pass
        assert is_model_class(MyModel_test_is_model_class) == True
        class X(object): pass
        assert is_model_class(X) == False

    def test_is_model_abstract(self):
        class AbstractModel_test_is_model_abstract(models.Model):
            class Meta:
                abstract = True
        assert is_model_abstract(AbstractModel_test_is_model_abstract)

        class ConcreteModel_test_is_model_abstract(models.Model):
            class Meta:
                abstract = False
        assert is_model_abstract(ConcreteModel_test_is_model_abstract) == False

    def test_is_model_managed(self):
        class NotManagedModel_test_is_model_managed(models.Model):
            class Meta:
                managed = False
        assert is_model_managed(NotManagedModel_test_is_model_managed) == False

        class ManagedModel_test_is_model_managed(models.Model):
            class Meta:
                managed = True
        assert is_model_managed(ManagedModel_test_is_model_managed)

    def test_model_has_the_field(self):
        class ModelWithWithoutFields_test_model_has_the_field(models.Model):
            integer = models.IntegerField()
            selfforeignkey = models.ForeignKey('self', null=True, on_delete=models.DO_NOTHING)
            manytomany = models.ManyToManyField('self', related_name='m2m')
        assert model_has_the_field(ModelWithWithoutFields_test_model_has_the_field, 'integer')
        assert model_has_the_field(ModelWithWithoutFields_test_model_has_the_field, 'selfforeignkey')
        assert model_has_the_field(ModelWithWithoutFields_test_model_has_the_field, 'manytomany')
        assert model_has_the_field(ModelWithWithoutFields_test_model_has_the_field, 'x') == False


class DjangoHelperFieldsTest(TestCase):
    def test_get_unique_field_name(self):
        class Model4GetUniqueFieldName_test_get_unique_field_name(models.Model):
            integer = models.IntegerField()
        field = get_field_by_name_or_raise(Model4GetUniqueFieldName_test_get_unique_field_name, 'integer')
        assert get_unique_field_name(field) == 'django_dynamic_fixture.tests.test_django_helper.Model4GetUniqueFieldName_test_get_unique_field_name.integer'

    def test_get_related_model(self):
        class ModelRelated_test_get_related_model(models.Model): pass
        class Model4GetRelatedModel_test_get_related_model(models.Model):
            fk = models.ForeignKey(ModelRelated_test_get_related_model, on_delete=models.DO_NOTHING)
        assert get_related_model(get_field_by_name_or_raise(Model4GetRelatedModel_test_get_related_model, 'fk')) == \
               ModelRelated_test_get_related_model


    def test_field_is_a_parent_link(self):
        class ModelParent_test_get_related_model(models.Model): pass
        class Model4FieldIsParentLink_test_get_related_model(ModelParent):
            o2o_with_parent_link = models.OneToOneField(ModelParent_test_get_related_model, parent_link=True, related_name='my_custom_ref_x', on_delete=models.DO_NOTHING)
        class Model4FieldIsParentLink2(ModelParent):
            o2o_without_parent_link = models.OneToOneField(ModelParent_test_get_related_model, parent_link=False, related_name='my_custom_ref_y', on_delete=models.DO_NOTHING)
        # FIXME
        # assert field_is_a_parent_link(get_field_by_name_or_raise(Model4FieldIsParentLink, 'o2o_with_parent_link'))
        assert field_is_a_parent_link(get_field_by_name_or_raise(Model4FieldIsParentLink2, 'o2o_without_parent_link')) == False

    def test_field_has_choices(self):
        class Model4FieldHasChoices_test_get_related_model(models.Model):
            with_choices = models.IntegerField(choices=((1, 1), (2, 2)))
            without_choices = models.IntegerField()
        assert field_has_choices(get_field_by_name_or_raise(Model4FieldHasChoices_test_get_related_model, 'with_choices'))
        assert field_has_choices(get_field_by_name_or_raise(Model4FieldHasChoices_test_get_related_model, 'without_choices')) == False

    def test_field_has_default_value(self):
        class Model4FieldHasDefault_test_field_has_default_value(models.Model):
            with_default = models.IntegerField(default=1)
            without_default = models.IntegerField()
        assert field_has_default_value(get_field_by_name_or_raise(Model4FieldHasDefault_test_field_has_default_value, 'with_default'))
        assert field_has_default_value(get_field_by_name_or_raise(Model4FieldHasDefault_test_field_has_default_value, 'without_default')) == False

    def test_field_is_unique(self):
        class Model4FieldMustBeUnique_test_field_is_unique(models.Model):
            unique = models.IntegerField(unique=True)
            not_unique = models.IntegerField()
        assert field_is_unique(get_field_by_name_or_raise(Model4FieldMustBeUnique_test_field_is_unique, 'unique'))
        assert field_is_unique(get_field_by_name_or_raise(Model4FieldMustBeUnique_test_field_is_unique, 'not_unique')) == False

    def test_is_key_field(self):
        class ModelForKeyField_test_is_key_field(models.Model):
            integer = models.IntegerField()
        assert is_key_field(get_field_by_name_or_raise(ModelForKeyField_test_is_key_field, 'id'))
        assert is_key_field(get_field_by_name_or_raise(ModelForKeyField_test_is_key_field, 'integer')) == False

    def test_is_relationship_field(self):
        class ModelForRelationshipField_test_is_relationship_field(models.Model):
            fk = models.ForeignKey('self', on_delete=models.DO_NOTHING)
            one2one = models.OneToOneField('self', on_delete=models.DO_NOTHING)
        assert is_relationship_field(get_field_by_name_or_raise(ModelForRelationshipField_test_is_relationship_field, 'fk'))
        assert is_relationship_field(get_field_by_name_or_raise(ModelForRelationshipField_test_is_relationship_field, 'one2one'))
        assert is_relationship_field(get_field_by_name_or_raise(ModelForRelationshipField_test_is_relationship_field, 'id')) == False

    def test_is_file_field(self):
        class ModelForFileField_test_is_file_field(models.Model):
            filefield = models.FileField()
        assert is_file_field(get_field_by_name_or_raise(ModelForFileField_test_is_file_field, 'filefield'))
        assert is_file_field(get_field_by_name_or_raise(ModelForFileField_test_is_file_field, 'id')) == False


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

