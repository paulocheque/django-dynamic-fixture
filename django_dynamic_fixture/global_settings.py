# -*- coding: utf-8 -*-

"""
Module that contains wrappers and shortcuts.
This is the facade of all features of DDF.
"""
import os
import sys
import warnings

from django.conf import settings
try:
    # Django 2.0
    from django.urls import get_mod_func
except ImportError:
    # Django <= 1.11
    from django.core.urlresolvers import get_mod_func
try:
    from importlib import import_module
except ImportError:
    from django.utils.importlib import import_module
import six

from django_dynamic_fixture.fixture_algorithms.sequential_fixture import SequentialDataFixture, StaticSequentialDataFixture, GlobalSequentialDataFixture
from django_dynamic_fixture.fixture_algorithms.random_fixture import RandomDataFixture


class DDFImproperlyConfigured(Exception):
    "DDF is improperly configured. Some global settings has bad value in django settings."


def get_ddf_config(name, default, cast=None, options=None, msg=''):
    try:
        value = os.getenv(name) # Priority for Env variables
        if not value:
            value = getattr(settings, name) if hasattr(settings, name) else default
        value = cast(value) if cast else value
        if options and value not in options:
            # to educate users to use the property correctly.
            raise DDFImproperlyConfigured()
        return value
    except Exception as e:
        six.reraise(
            DDFImproperlyConfigured,
            DDFImproperlyConfigured('{}="{}": {} ({})'.format(name, value, msg, e),
            sys.exc_info()[2])
        )


def get_boolean_config(config_name, default=False):
    return get_ddf_config(config_name, default, options=[True, False], msg='it must be True or False')


def get_data_fixture(default='sequential'):
    # It must be 'sequential', 'static_sequential', 'global_sequential', 'random' or 'path.to.CustomDataFixtureClass'
    try:
        INTERNAL_DATA_FIXTURES = {'sequential': SequentialDataFixture(),
                                  'static_sequential': StaticSequentialDataFixture(),
                                  'global_sequential': GlobalSequentialDataFixture(),
                                  'random': RandomDataFixture()}
        if hasattr(settings, 'DDF_DEFAULT_DATA_FIXTURE'):
            if settings.DDF_DEFAULT_DATA_FIXTURE in INTERNAL_DATA_FIXTURES.keys():
                return INTERNAL_DATA_FIXTURES[settings.DDF_DEFAULT_DATA_FIXTURE]
            else:
                # path.to.CustomDataFixtureClass
                mod_name, obj_name = get_mod_func(settings.DDF_DEFAULT_DATA_FIXTURE)
                module = import_module(mod_name)
                custom_data_fixture = getattr(module, obj_name)
                return custom_data_fixture()
        else:
            return INTERNAL_DATA_FIXTURES[default]
    except:
        six.reraise(DDFImproperlyConfigured, DDFImproperlyConfigured("DDF_DEFAULT_DATA_FIXTURE (%s) must be 'sequential', 'static_sequential', 'global_sequential', 'random' or 'path.to.CustomDataFixtureClass'." % settings.DDF_DEFAULT_DATA_FIXTURE), sys.exc_info()[2])


DDF_DEFAULT_DATA_FIXTURE = get_data_fixture(default='sequential')
DDF_IGNORE_FIELDS = get_ddf_config('DDF_IGNORE_FIELDS', default=[], cast=list, msg='it must be a list of strings')
DDF_FK_MIN_DEPTH = get_ddf_config('DDF_FK_MIN_DEPTH', default=0, cast=int, msg='it must be a integer number')
if hasattr(settings, 'DDF_NUMBER_OF_LAPS'):
    warnings.warn(
        "The old DDF_NUMBER_OF_LAPS settings was replaced by the new DDF_FK_MIN_DEPTH.",
        DeprecationWarning
    )
DDF_FIELD_FIXTURES = get_ddf_config('DDF_FIELD_FIXTURES', default={}, cast=dict, msg='it must be a dict')
DDF_DEFAULT_DATA_FIXTURE.plugins = DDF_FIELD_FIXTURES
DDF_FILL_NULLABLE_FIELDS = get_boolean_config('DDF_FILL_NULLABLE_FIELDS', default=False)
DDF_VALIDATE_MODELS = get_boolean_config('DDF_VALIDATE_MODELS', default=False)
DDF_DEBUG_MODE = get_boolean_config('DDF_DEBUG_MODE', default=False)
