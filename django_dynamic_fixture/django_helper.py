# -*- coding: utf-8 -*-

"""
Module to wrap dirty stuff of django core.
"""
from django.db import models
from django.db.models import Model, ForeignKey, OneToOneField, FileField
from django.db.models.fields import NOT_PROVIDED, AutoField, FieldDoesNotExist
from django.db.models.base import ModelBase
from django.db.models.query import QuerySet


# Apps
def get_apps(application_labels=[], exclude_application_labels=[]):
    """
    - if not @application_labels and not @exclude_application_labels, it returns all applications.
    - if @application_labels is not None, it returns just these applications,
    except applications with label in exclude_application_labels.
    """
    if application_labels:
        applications = []
        for app_label in application_labels:
            applications.append(models.get_app(app_label))
    else:
        applications = models.get_apps()
    if exclude_application_labels:
        for app_label in exclude_application_labels:
            if app_label:
                applications.remove(models.get_app(app_label))
    return applications


def get_app_name(app):
    """
    app is the object returned by get_apps method
    """
    return app.__name__.replace('.models', '')


def get_models_of_an_app(app):
    """
    app is the object returned by get_apps method
    """
    return models.get_models(app)


# Models
def get_app_name_of_model(model_class):
    return model_class.__module__.split('.')[0]


def get_model_name(model_class):
    "Example: ModelName"
    return model_class.__name__


def get_unique_model_name(model_class):
    "Example: app.packages.ModelName"
    return model_class.__module__.replace('.models', '') + '.' + model_class.__name__


def get_fields_from_model(model_class):
    "Returns all fields, including inherited fields but ignoring M2M fields."
    return model_class._meta.fields


def get_local_fields(model):
    "Returns all local fields!?"
    return model._meta.local_fields


def get_many_to_many_fields_from_model(model_class):
    "Return only M2M fields, including inherited ones?"
    return model_class._meta.many_to_many
    #_meta.local_many_to_many


def get_all_fields_of_model(model_class):
    fields1 = get_fields_from_model(model_class)
    fields2 = get_many_to_many_fields_from_model(model_class)
    fields1.extend(fields2)
    return fields1


def get_field_names_of_model(model_class):
    "Get field names, including inherited fields, except M2M fields."
    fields = get_fields_from_model(model_class)
    return [field.name for field in fields]


def get_field_by_name_or_raise(model_class, field_name):
    "Get field by name, including inherited fields and M2M fields."
    return model_class._meta.get_field_by_name(field_name)[0]


def is_model_class(instance_or_model_class):
    "True if model_class is a Django Model."
    return isinstance(instance_or_model_class, Model) or instance_or_model_class.__class__ == ModelBase


def is_model_abstract(model):
    "True if abstract is True in Meta class"
    return model._meta.abstract


def is_model_managed(model):
    "True if managed is True in Meta class"
    return model._meta.managed


def model_has_the_field(model_class, field_name):
    ""
    try:
        get_field_by_name_or_raise(model_class, field_name)
        return True
    except FieldDoesNotExist:
        return False


# Fields
def get_unique_field_name(field):
    if hasattr(field, 'model'):
        return get_unique_model_name(field.model) + '.' + field.name
    return field.name


def get_related_model(field):
    return field.rel.to


def field_is_a_parent_link(field):
    # FIXME
    #return hasattr(field, 'rel') and hasattr(field.rel, 'parent_link') and field.rel.parent_link
    return hasattr(field, 'parent_link') and field.parent_link


def field_has_choices(field):
    return bool(len(field.choices) > 0 and field.choices)


def field_has_default_value(field):
    return field.default != NOT_PROVIDED


def field_is_unique(field):
    return field.unique


def is_key_field(field):
    return isinstance(field, AutoField)


def is_relationship_field(field):
    return isinstance(field, (ForeignKey, OneToOneField))


def is_file_field(field):
    return isinstance(field, FileField)


def print_field_values_of_a_model(model_instance):
    "Print values from all fields of a model instance."
    if model_instance == None:
        print('\n:: Model Unknown: None')
    else:
        print('\n:: Model %s (%s)' % (get_unique_model_name(model_instance.__class__), model_instance.pk))
        for field in get_fields_from_model(model_instance.__class__):
            print('%s: %s' % (field.name, getattr(model_instance, field.name)))
        if model_instance.pk is not None:
            for field in get_many_to_many_fields_from_model(model_instance.__class__):
                print('%s: %s' % (field.name, getattr(model_instance, field.name).all()))


def print_field_values(model_instance_or_list_of_model_instances_or_queryset):
    "Print values from all fields of a model instance or a list of model instances."
    if isinstance(model_instance_or_list_of_model_instances_or_queryset, (list, tuple, QuerySet)):
        for model_instance in model_instance_or_list_of_model_instances_or_queryset:
            print_field_values_of_a_model(model_instance)
    else:
        model_instance = model_instance_or_list_of_model_instances_or_queryset
        print_field_values_of_a_model(model_instance)


def enable_auto_now(field):
    if hasattr(field, 'auto_now'):
        field.auto_now = True

def disable_auto_now(field):
    if hasattr(field, 'auto_now'):
        field.auto_now = False

def enable_auto_now_add(field):
    if hasattr(field, 'auto_now_add'):
        field.auto_now_add = True

def disable_auto_now_add(field):
    if hasattr(field, 'auto_now_add'):
        field.auto_now_add = False
