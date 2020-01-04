# -*- coding: utf-8 -*-

"""
This is the facade of all features of DDF.
Module that contains wrappers and shortcuts (aliases).
"""
import warnings
import six

from django_dynamic_fixture.ddf import DynamicFixture, Copier, DDFLibrary, \
    set_pre_save_receiver, set_post_save_receiver
from django_dynamic_fixture.django_helper import print_field_values, django_greater_than
from django_dynamic_fixture.fixture_algorithms.sequential_fixture import SequentialDataFixture, \
    StaticSequentialDataFixture
from django_dynamic_fixture.global_settings import DDF_DEFAULT_DATA_FIXTURE, DDF_FILL_NULLABLE_FIELDS, DDF_NUMBER_OF_LAPS, \
                                                    DDF_IGNORE_FIELDS, DDF_VALIDATE_MODELS, DDF_VALIDATE_ARGS, \
                                                    DDF_DEBUG_MODE, DDF_FIELD_FIXTURES


if not django_greater_than('1.10'):
    warnings.warn("DDF supports oficially only Django 1.11 or higher.", DeprecationWarning)


LOOKUP_SEP = '__'

def look_up_alias(**kwargs):
    """
    a__b__c=1 => a=F(b=F(c=1))
    """
    field_dict = {}
    for key, value in kwargs.items():
        parts = key.split(LOOKUP_SEP)
        current_dict = {parts[-1]: value}
        first_fields = parts[:-1]
        first_fields.reverse()
        for part in first_fields:
            current_dict = {part: F(**current_dict)}
        field_dict.update(current_dict)
    return field_dict


def fixture(**kwargs):
    """
    DynamicFixture factory: It instantiate a DynamicFixture using global configurations.
    Same as F(...)
    """
    kwargs = look_up_alias(**kwargs)
    f = DynamicFixture(data_fixture=kwargs.pop('data_fixture', DDF_DEFAULT_DATA_FIXTURE),
                       fill_nullable_fields=kwargs.pop('fill_nullable_fields', DDF_FILL_NULLABLE_FIELDS),
                       ignore_fields=kwargs.pop('ignore_fields', []),
                       number_of_laps=kwargs.pop('number_of_laps', DDF_NUMBER_OF_LAPS),
                       validate_models=kwargs.pop('validate_models', DDF_VALIDATE_MODELS),
                       validate_args=kwargs.pop('validate_args', DDF_VALIDATE_ARGS),
                       print_errors=kwargs.pop('print_errors', True),
                       debug_mode=kwargs.pop('debug_mode', DDF_DEBUG_MODE),
                       **kwargs)
    return f


# Wrappers

def _new(model, n=1, lesson=None, persist_dependencies=True, **kwargs):
    """
    Return one or many valid instances of Django Models with fields filled with auto generated or customized data.
    All instances will NOT be persisted in the database, except its dependencies, in case @persist_dependencies is True.

    @model: The class of the Django model.
    @n: number of instances to be created with the given configuration. Default is 1.
    @lesson: use a custom lesson to build the model object.
    @persist_dependencies: If True, save internal dependencies, otherwise just instantiate them. Default is True.

    @data_fixture: override DDF_DEFAULT_DATA_FIXTURE configuration. Default is SequentialDataFixture().
    @fill_nullable_fields: override DDF_FILL_NULLABLE_FIELDS global configuration. Default is True.
    @ignore_fields: List of fields that will be ignored by DDF. It will be concatenated with the global list DDF_IGNORE_FIELDS. Default is [].
    @number_of_laps: override DDF_NUMBER_OF_LAPS global configuration. Default 1.
    @validate_models: override DDF_VALIDATE_MODELS global configuration. Default is False.
    @validate_args: override DDF_VALIDATE_ARGS global configuration. Default is False.
    @print_errors: print on console all instance values if DDF can not generate a valid object with the given configuration.

    Wrapper for the method DynamicFixture.new
    """
    kwargs = look_up_alias(**kwargs)
    d = fixture(**kwargs)
    if n == 1:
        return d.new(model, lesson=lesson, persist_dependencies=persist_dependencies, **kwargs)
    instances = []
    for _ in range(n):
        instances.append(d.new(model, lesson=lesson, persist_dependencies=persist_dependencies, **kwargs))
    return instances


def _get(model, n=1, lesson=None, **kwargs):
    """
    Return one or many valid instances of Django Models with fields filled with auto generated or customized data.
    All instances will be persisted in the database.

    @model: The class of the Django model.
    @n: number of instances to be created with the given configuration. Default is 1.
    @lesson: use a custom lesson to build the model object.

    @data_fixture: override DDF_DEFAULT_DATA_FIXTURE configuration. Default is SequentialDataFixture().
    @fill_nullable_fields: override DDF_FILL_NULLABLE_FIELDS global configuration. Default is True.
    @ignore_fields: List of fields that will be ignored by DDF. It will be concatenated with the global list DDF_IGNORE_FIELDS. Default is [].
    @number_of_laps: override DDF_NUMBER_OF_LAPS global configuration. Default 1.
    @validate_models: override DDF_VALIDATE_MODELS global configuration. Default is False.
    @validate_args: override DDF_VALIDATE_ARGS global configuration. Default is False.
    @print_errors: print on console all instance values if DDF can not generate a valid object with the given configuration.

    Wrapper for the method DynamicFixture.get
    """
    kwargs = look_up_alias(**kwargs)
    d = fixture(**kwargs)
    if n == 1:
        return d.get(model, lesson=lesson, **kwargs)
    instances = []
    for _ in range(n):
        instances.append(d.get(model, lesson=lesson, **kwargs))
    return instances


def _teach(model, lesson=None, **kwargs):
    '''
    @model: The class of the Django model.
    @lesson: Name of custom lesson to be created.

    @raise an CantOverrideLesson error if the same model/lesson were called twice.

    Sometimes DDF can't create an model instance because the particularities of the model.
    The workaround for this is to teach DDF how to create it.
    Basically, we use the same object creation approach that will be saved as a template
    for the next DDF calls.

    Use this method to teach DDF how to create an instance.

    New metaphor for the shelve/library feature.
    `Shelve` becomes `Teach`
    `Library` becomes `Lessons`
    '''
    kwargs = look_up_alias(**kwargs)
    d = fixture(**kwargs)
    return d.teach(model, lesson=lesson, **kwargs)


# Shortcuts
N = new = _new
G = get = _get
T = teach = _teach
F = fixture
C = Copier
P = print_field_values
DDFLibrary = DDFLibrary
PRE_SAVE = set_pre_save_receiver
POST_SAVE = set_post_save_receiver

if six.PY3:
    # Add type hints for Python >= 3.5
    try:
        import typing

        INSTANCE_TYPE = typing.TypeVar('INSTANCE')

        def new(model: typing.Type[INSTANCE_TYPE], n=1, lesson=None, persist_dependencies=True, **kwargs) -> INSTANCE_TYPE:
            return _new(model, n=n, lesson=lesson, persist_dependencies=persist_dependencies, **kwargs)

        def get(model: typing.Type[INSTANCE_TYPE], n=1, lesson=None, **kwargs) -> INSTANCE_TYPE:
            return _get(model, n=n, lesson=lesson, **kwargs)

        def teach(model: typing.Type[INSTANCE_TYPE], lesson=None, **kwargs):
            return _teach(model, lesson=lesson, **kwargs)

        N = new
        G = get
        T = teach
    except (ImportError, SyntaxError):
        pass
