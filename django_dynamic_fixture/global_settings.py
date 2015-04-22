# -*- coding: utf-8 -*-

"""
Module that contains wrappers and shortcuts.
This is the facade of all features of DDF.
"""
import sys

from django.conf import settings
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


def get_boolean_config(config_name, default=False):
    try:
        if hasattr(settings, config_name) and getattr(settings, config_name) not in [True, False]:
            # to educate users to use this property correctly.
            raise DDFImproperlyConfigured()
        return getattr(settings, config_name) if hasattr(settings, config_name) else default
    except DDFImproperlyConfigured:
        six.reraise(DDFImproperlyConfigured, DDFImproperlyConfigured("%s (%s) must be True or False." % (config_name, getattr(settings, config_name))), sys.exc_info()[2])


# DDF_DEFAULT_DATA_FIXTURE default = 'sequential'
# It must be 'sequential', 'static_sequential', 'global_sequential', 'random' or 'path.to.CustomDataFixtureClass'
try:
    INTERNAL_DATA_FIXTURES = {'sequential': SequentialDataFixture(),
                              'static_sequential': StaticSequentialDataFixture(),
                              'global_sequential': GlobalSequentialDataFixture(),
                              'random': RandomDataFixture()}
    if hasattr(settings, 'DDF_DEFAULT_DATA_FIXTURE'):
        if settings.DDF_DEFAULT_DATA_FIXTURE in INTERNAL_DATA_FIXTURES.keys():
            DDF_DEFAULT_DATA_FIXTURE = INTERNAL_DATA_FIXTURES[settings.DDF_DEFAULT_DATA_FIXTURE]
        else:
            # path.to.CustomDataFixtureClass
            mod_name, obj_name = get_mod_func(settings.DDF_DEFAULT_DATA_FIXTURE)
            module = import_module(mod_name)
            custom_data_fixture = getattr(module, obj_name)
            DDF_DEFAULT_DATA_FIXTURE = custom_data_fixture()
    else:
        DDF_DEFAULT_DATA_FIXTURE = INTERNAL_DATA_FIXTURES['sequential']
except:
    six.reraise(DDFImproperlyConfigured, DDFImproperlyConfigured("DDF_DEFAULT_DATA_FIXTURE (%s) must be 'sequential', 'static_sequential', 'global_sequential', 'random' or 'path.to.CustomDataFixtureClass'." % settings.DDF_DEFAULT_DATA_FIXTURE), sys.exc_info()[2])


# DDF_IGNORE_FIELDS default = []
try:
    DDF_IGNORE_FIELDS = list(settings.DDF_IGNORE_FIELDS) if hasattr(settings, 'DDF_IGNORE_FIELDS') else []
except Exception as e:
    six.reraise(DDFImproperlyConfigured, DDFImproperlyConfigured("DDF_IGNORE_FIELDS (%s) must be a list of strings" % settings.DDF_IGNORE_FIELDS), sys.exc_info()[2])


# DDF_NUMBER_OF_LAPS default = 1
try:
    DDF_NUMBER_OF_LAPS = int(settings.DDF_NUMBER_OF_LAPS) if hasattr(settings, 'DDF_NUMBER_OF_LAPS') else 1
except Exception as e:
    six.reraise(DDFImproperlyConfigured, DDFImproperlyConfigured("DDF_NUMBER_OF_LAPS (%s) must be a integer number." % settings.DDF_NUMBER_OF_LAPS), sys.exc_info()[2])


# DDF_FIELD_FIXTURES default = {}
try:
    DDF_FIELD_FIXTURES = dict(settings.DDF_FIELD_FIXTURES) if hasattr(settings, 'DDF_FIELD_FIXTURES') else {}
    DDF_DEFAULT_DATA_FIXTURE.plugins = DDF_FIELD_FIXTURES
except Exception as e:
    six.reraise(DDFImproperlyConfigured, DDFImproperlyConfigured("DDF_FIELD_FIXTURES (%s) must be a dict." % settings.DDF_FIELD_FIXTURES), sys.exc_info()[2])



DDF_FILL_NULLABLE_FIELDS = get_boolean_config('DDF_FILL_NULLABLE_FIELDS', default=True)
DDF_VALIDATE_MODELS = get_boolean_config('DDF_VALIDATE_MODELS', default=False)
DDF_VALIDATE_ARGS = get_boolean_config('DDF_VALIDATE_ARGS', default=False)
DDF_USE_LIBRARY = get_boolean_config('DDF_USE_LIBRARY', default=False)
DDF_DEBUG_MODE = get_boolean_config('DDF_DEBUG_MODE', default=False)

