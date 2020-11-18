# -*- coding: utf-8 -*-

"""
This is the facade of all features of DDF.
Module that contains wrappers and shortcuts (aliases).
"""
import warnings
import six

from django.apps import apps

from django_dynamic_fixture.ddf import DynamicFixture, Copier, Mask, DDFLibrary, \
    set_pre_save_receiver, set_post_save_receiver
from django_dynamic_fixture.django_helper import print_field_values, django_greater_than
from django_dynamic_fixture.fixture_algorithms.sequential_fixture import SequentialDataFixture, \
    StaticSequentialDataFixture
from django_dynamic_fixture.global_settings import DDF_DEFAULT_DATA_FIXTURE, DDF_FILL_NULLABLE_FIELDS, DDF_FK_MIN_DEPTH, \
                                                    DDF_IGNORE_FIELDS, DDF_VALIDATE_MODELS, \
                                                    DDF_DEBUG_MODE, DDF_FIELD_FIXTURES
from django_dynamic_fixture.script_ddf_checkings import ddf_check_models


__version__ = '3.1.1'


if not django_greater_than('1.10'):
    warnings.warn("DDF supports oficially only Django 1.11 or higher.", DeprecationWarning)


LOOKUP_SEP = '__'

def look_up_alias(ddf_as_f=True, **kwargs):
    """
    Example of parameters:
    a__b__c=1 => {a: {b: {c: 1}}}
    """
    field_dict = {}
    params_to_be_skipped = []
    for alias, value in kwargs.items():
        parts = alias.split(LOOKUP_SEP)
        if len(parts) == 1:
            params_to_be_skipped.append(alias)
        level_dict = field_dict
        for part in parts[:-1]:
            level_dict = level_dict.setdefault(part, {})
        level_dict[parts[-1]] = value
    if ddf_as_f:
        for root, value in field_dict.items():
            if root in params_to_be_skipped:
                field_dict[root] = value
            else:
                field_dict[root] = dict_to_f(value)
    return field_dict


def dict_to_f(value):
    """
    Example:
    1 => 1
    {b: 1} => F(b=1)
    {b: {c: 1}} => F(b=F(c=1))
    """
    if not isinstance(value, dict):
        return value
    else:
        kwargs = {}
        for k, v in value.items():
            if not isinstance(v, dict):
                kwargs[k] = v
            else:
                kwargs[k] = dict_to_f(v)
        return F(**kwargs)


def fixture(**kwargs):
    """
    DynamicFixture factory: It instantiate a DynamicFixture using global configurations.
    Same as F(...)
    """
    kwargs = look_up_alias(**kwargs)
    f = DynamicFixture(data_fixture=kwargs.pop('data_fixture', DDF_DEFAULT_DATA_FIXTURE),
                       fill_nullable_fields=kwargs.pop('fill_nullable_fields', DDF_FILL_NULLABLE_FIELDS),
                       ignore_fields=kwargs.pop('ignore_fields', []),
                       fk_min_depth=kwargs.pop('fk_min_depth', DDF_FK_MIN_DEPTH),
                       validate_models=kwargs.pop('validate_models', DDF_VALIDATE_MODELS),
                       print_errors=kwargs.pop('print_errors', True),
                       debug_mode=kwargs.pop('debug_mode', DDF_DEBUG_MODE),
                       **kwargs)
    return f


# Wrappers

def _new(model, n=1, ddf_lesson=None, persist_dependencies=False, **kwargs):
    """
    Return one or many valid instances of Django Models with fields filled with auto generated or customized data.
    All instances will NOT be persisted in the database, except its dependencies, in case @persist_dependencies is True.

    @model: The class of the Django model. It can be a string `<app_label>.<model_name>`
    @n: number of instances to be created with the given configuration. Default is 1.
    @ddf_lesson: use a custom ddf_lesson to build the model object.
    @persist_dependencies: If True, save internal dependencies, otherwise just instantiate them. Default is False.

    @data_fixture: override DDF_DEFAULT_DATA_FIXTURE configuration. Default is SequentialDataFixture().
    @fill_nullable_fields: override DDF_FILL_NULLABLE_FIELDS global configuration. Default is True.
    @ignore_fields: List of fields that will be ignored by DDF. It will be concatenated with the global list DDF_IGNORE_FIELDS. Default is [].
    @fk_min_depth: override DDF_FK_MIN_DEPTH global configuration. Default 0.
    @validate_models: override DDF_VALIDATE_MODELS global configuration. Default is False.
    @print_errors: print on console all instance values if DDF can not generate a valid object with the given configuration.

    Wrapper for the method DynamicFixture.new
    """
    if isinstance(model, str):
        model = apps.get_model(model)
    kwargs = look_up_alias(**kwargs)
    d = fixture(**kwargs)
    if n == 1:
        return d.new(model, ddf_lesson=ddf_lesson, persist_dependencies=persist_dependencies, **kwargs)
    instances = []
    for _ in range(n):
        instances.append(d.new(model, ddf_lesson=ddf_lesson, persist_dependencies=persist_dependencies, **kwargs))
    return instances


def _get(model, n=1, ddf_lesson=None, **kwargs):
    """
    Return one or many valid instances of Django Models with fields filled with auto generated or customized data.
    All instances will be persisted in the database.

    @model: The class of the Django model. It can be a string `<app_label>.<model_name>`
    @n: number of instances to be created with the given configuration. Default is 1.
    @ddf_lesson: use a custom ddf_lesson to build the model object.

    @data_fixture: override DDF_DEFAULT_DATA_FIXTURE configuration. Default is SequentialDataFixture().
    @fill_nullable_fields: override DDF_FILL_NULLABLE_FIELDS global configuration. Default is True.
    @ignore_fields: List of fields that will be ignored by DDF. It will be concatenated with the global list DDF_IGNORE_FIELDS. Default is [].
    @fk_min_depth: override DDF_FK_MIN_DEPTH global configuration. Default 0.
    @validate_models: override DDF_VALIDATE_MODELS global configuration. Default is False.
    @print_errors: print on console all instance values if DDF can not generate a valid object with the given configuration.

    Wrapper for the method DynamicFixture.get
    """
    if isinstance(model, str):
        model = apps.get_model(model)
    kwargs = look_up_alias(**kwargs)
    d = fixture(**kwargs)
    if n == 1:
        return d.get(model, ddf_lesson=ddf_lesson, **kwargs)
    instances = []
    for _ in range(n):
        instances.append(d.get(model, ddf_lesson=ddf_lesson, **kwargs))
    return instances


def _teach(model, ddf_lesson=None, **kwargs):
    '''
    @model: The class of the Django model. It can be a string `<app_label>.<model_name>`
    @ddf_lesson: Name of custom ddf_lesson to be created.

    @raise an CantOverrideddf_lesson error if the same model/ddf_lesson were called twice.

    Sometimes DDF can't create an model instance because the particularities of the model.
    The workaround for this is to teach DDF how to create it.
    Basically, we use the same object creation approach that will be saved as a template
    for the next DDF calls.

    Use this method to teach DDF how to create an instance.

    New metaphor for the shelve/library feature.
    `Shelve` becomes `Teach`
    `Library` becomes `Lessons`
    '''
    if isinstance(model, str):
        model = apps.get_model(model)
    kwargs = look_up_alias(**kwargs)
    d = fixture(**kwargs)
    return d.teach(model, ddf_lesson=ddf_lesson, **kwargs)


# Shortcuts
N = new = _new
G = get = _get
T = teach = _teach
F = fixture
C = Copier
M = Mask
P = print_field_values
DDFLibrary = DDFLibrary
PRE_SAVE = set_pre_save_receiver
POST_SAVE = set_post_save_receiver

if six.PY3:
    # Add type hints for Python >= 3.5
    try:
        import typing

        INSTANCE_TYPE = typing.TypeVar('INSTANCE')

        hack_to_avoid_py2_syntax_errors = '''
def new(model: typing.Type[INSTANCE_TYPE], n=1, ddf_lesson=None, persist_dependencies=True, **kwargs) -> INSTANCE_TYPE:
    return _new(model, n=n, ddf_lesson=ddf_lesson, persist_dependencies=persist_dependencies, **kwargs)

def get(model: typing.Type[INSTANCE_TYPE], n=1, ddf_lesson=None, **kwargs) -> INSTANCE_TYPE:
    return _get(model, n=n, ddf_lesson=ddf_lesson, **kwargs)

def teach(model: typing.Type[INSTANCE_TYPE], ddf_lesson=None, **kwargs):
    return _teach(model, ddf_lesson=ddf_lesson, **kwargs)

N = new
G = get
T = teach
        '''
        exec(hack_to_avoid_py2_syntax_errors)
    except (ImportError, SyntaxError) as e:
        pass

