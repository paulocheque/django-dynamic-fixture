# -*- coding: utf-8 -*-

import inspect
import logging
import sys
import six

from django.core.files import File
from django.db.models import Field

try:
    from importlib import import_module
except ImportError:
    from django.utils.importlib import import_module

from django_dynamic_fixture.django_helper import get_related_model, \
    field_has_choices, field_has_default_value, get_fields_from_model, \
    print_field_values, get_many_to_many_fields_from_model, \
    get_unique_model_name, get_unique_field_name, is_model_abstract, \
    field_is_a_parent_link, get_field_by_name_or_raise, get_app_name_of_model, \
    is_model_class, is_relationship_field, is_file_field, is_key_field, \
    model_has_the_field, enable_auto_now, disable_auto_now, enable_auto_now_add, disable_auto_now_add


LOGGER = logging.getLogger('DDFLog')
_LOADED_DDF_SETUP_MODULES = [] # control to avoid a ddf_setup module be loaded more than one time.
_PRE_SAVE = {} # receivers to be executed before saving a instance;
_POST_SAVE = {} # receivers to be executed after saving a instance;


class UnsupportedFieldError(Exception):
    "DynamicFixture does not support this field."


class InvalidCopierExpressionError(Exception):
    "The specified expression used in a Copier is invalid."


class InvalidConfigurationError(Exception):
    "The specified configuration for the field can not be applied or it is bugged."


class InvalidManyToManyConfigurationError(Exception):
    "M2M attribute configuration must be a number or a list of DynamicFixture or model instances."


class BadDataError(Exception):
    "The data passed to a field has some problem (not unique or invalid) or a required attribute is in ignore list."


class InvalidModelError(Exception):
    "Invalid Model: The class is not a model or it is abstract."


class InvalidDDFSetupError(Exception):
    "ddf_setup.py has execution errors"


class InvalidReceiverError(Exception):
    "Receiver is not a function that receive only the instance as parameter."


class PendingField(Exception):
    "Internal exception to control pending fields when using Copier."


def set_pre_save_receiver(model_class, callback_function):
    """
    :model_class: a model_class can have only one receiver. Do not complicate yourself.
    :callback_function must be a function that receive the instance as unique parameter.
    """
    if not is_model_class(model_class) or not inspect.isfunction(callback_function) or len(inspect.getargspec(callback_function).args) != 1:
        raise InvalidReceiverError(model_class)
    _PRE_SAVE[model_class] = callback_function


def set_post_save_receiver(model_class, callback_function):
    """
    :model_class: a model_class can have only one receiver. Do not complicate yourself.
    :callback_function must be a function that receive the instance as unique parameter.
    """
    if not is_model_class(model_class) or not inspect.isfunction(callback_function) or len(inspect.getargspec(callback_function).args) != 1:
        raise(InvalidReceiverError(model_class))
    _POST_SAVE[model_class] = callback_function


class DataFixture(object):
    """
    Responsibility: return a valid data for a Django Field, according to its type, model class, constraints etc.

    You must create a separated method to generate data for an specific field. For a field called 'MyField',
    the method must be:

    def myfield_config(self, field, key): return 'some value'

    :field: Field object.
    :key: string that represents a unique name for a Field, considering app, model and field names.
    """
    def __init__(self):
        self.plugins = {}

    def _field_fixture_template(self, field_class):
        return '%s_config' % (field_class.__name__.lower(),)

    def _field_fixture_factory(self, field_class):
        try:
            fixture = self._field_fixture_template(field_class)
            getattr(self, fixture)
            return fixture
        except AttributeError:
            if len(field_class.__bases__) > 0:
                # Pick the first parent class that inherits Field (or use the first parent class)
                field_subclasses = (cls for cls in field_class.__bases__ if issubclass(cls, Field))
                parent_class = next(field_subclasses, field_class.__bases__[0])
                return self._field_fixture_factory(parent_class)
            else:
                return None

    def generate_data(self, field):
        "Get a unique and valid data for the field."
        field_fullname = field.__module__ + "." + field.__class__.__name__
        fixture = self.plugins.get(field_fullname, {})
        if type(fixture) == dict:
            fixture = fixture.get('ddf_fixture', None)
        if fixture and callable(fixture):
            return fixture()
        config = self._field_fixture_factory(field.__class__)
        is_supported_field = config != None
        if is_supported_field:
            key = get_unique_field_name(field)
            data = eval('self.%s(field, "%s")' % (config, key,))
        else:
            if field.null:
                data = None # a workaround for versatility
            else:
                raise(UnsupportedFieldError(get_unique_field_name(field) + ' (%s)' % (field_fullname)))
        return data


class Copier(object):
    """
    Wrapper of an expression in the format 'field' or 'field.field' or 'field.field.field' etc
    This expression will be interpreted to copy the value of the specified field to the current field.
    Example of usage: G(MyModel, x=C('y.z')) => the value 'z' of field 'y' will be copied to field 'x'.
    """
    def __init__(self, expression):
        self.expression = expression

    def __str__(self):
        return "C('%s')" % self.expression

    def immediate_field_name(self, instance):
        model_class = instance.__class__
        field_name = self.expression.split('.')[0]
        get_field_by_name_or_raise(model_class, field_name)
        return field_name

    def eval_expression(self, instance):
        try:
            current_instance = instance
            fields = self.expression.split('.')
            for field in fields:
                current_instance = getattr(current_instance, field)
            return current_instance
        except Exception as e:
            six.reraise(InvalidCopierExpressionError, InvalidCopierExpressionError(self.expression, e), sys.exc_info()[2])


class DDFLibrary(object):
    instance = None
    DEFAULT_KEY = 'ddf_default'

    def __init__(self):
        self.configs = {} # {Model: {name: config}}"

    def __str__(self):
        return '\n'.join(['%s = %s' % (key, value) for key, value in self.configs.items()])

    @classmethod
    def get_instance(cls):
        if not cls.instance:
            cls.instance = DDFLibrary()
        return cls.instance

    def add_configuration(self, model_class, kwargs, name=None):
        if name in [None, True]:
            name = self.DEFAULT_KEY
        model_class_config = self.configs.setdefault(model_class, {})
        model_class_config[name] = kwargs

    def get_configuration(self, model_class, name=None):
        if name is None:
            name = self.DEFAULT_KEY
        # copy is important because this dict will be updated every time in the algorithm.
        config = self.configs.get(model_class, {})
        if name != self.DEFAULT_KEY and name not in config.keys():
            raise InvalidConfigurationError('There is no shelved configuration for model %s with the name "%s"' % (get_unique_model_name(model_class), name))
        return config.get(name, {}).copy() # default configuration never raises an error

    def clear(self):
        "Remove all shelved configurations of the library."
        self.configs = {}

    def clear_configuration(self, model_class):
        "Remove from the library an specific configuration of a model."
        if model_class in self.configs.keys():
            del self.configs[model_class]


class DynamicFixture(object):
    """
    Responsibility: create a valid model instance according to the given configuration.
    """

    _DDF_CONFIGS = ['fill_nullable_fields', 'ignore_fields', 'data_fixture', 'number_of_laps', 'use_library',
                    'validate_models', 'validate_args', 'print_errors']

    def __init__(self, data_fixture, fill_nullable_fields=True, ignore_fields=[], number_of_laps=1, use_library=False,
                 validate_models=False, validate_args=False, print_errors=True, model_path=[], debug_mode=False, **kwargs):
        """
        :data_fixture: algorithm to fill field data.
        :fill_nullable_fields: flag to decide if nullable fields must be filled with data.
        :ignore_fields: list of field names that must not be filled with data.
        :number_of_laps: number of laps for each cyclic dependency.
        :use_library: flag to decide if DDF library will be used to load default fixtures.
        :validate_models: flag to decide if the model_instance.full_clean() must be called before saving the object.
        :validate_args: flag to enable field name validation of custom fixtures.
        :print_errors: flag to determine if the model data must be printed to console on errors. For some scripts is interesting to disable it.
        :model_path: internal variable used to control the cycles of dependencies.
        """
        # custom config of fixtures
        self.data_fixture = data_fixture
        self.fill_nullable_fields = fill_nullable_fields
        self.ignore_fields = ignore_fields
        self.number_of_laps = number_of_laps
        self.use_library = use_library
        # other ddfs configs
        self.validate_models = validate_models
        self.validate_args = validate_args
        self.print_errors = print_errors
        # internal logic
        self.model_path = model_path
        self.pending_fields = []
        self.fields_processed = []
        self.debug_mode = debug_mode
        self.kwargs = kwargs
        self.fields_to_disable_auto_now = []
        self.fields_to_disable_auto_now_add = []

    def __str__(self):
        return 'F(%s)' % (', '.join(six.text_type('%s=%s') % (key, value) for key, value in self.kwargs.items()))

    def __eq__(self, that):
        return self.kwargs == that.kwargs

    def _get_data_from_custom_dynamic_fixture(self, field, fixture, persist_dependencies):
        "return data of a Dynamic Fixture: field=F(...)"
        next_model = get_related_model(field)
        if persist_dependencies:
            data = fixture.get(next_model)
        else:
            data = fixture.new(next_model, persist_dependencies=persist_dependencies)
        return data

    def _get_data_from_custom_copier(self, instance, field, fixture):
        "return data of a Copier: field=C(...)"
        field_name = fixture.immediate_field_name(instance)
        if field_name in self.fields_processed:
            data = fixture.eval_expression(instance)
        else:
            self.pending_fields.append(field.name)
            raise PendingField('%s' % field.name)
        return data

    def _get_data_from_data_fixture(self, field, fixture):
        "return data of a Data Fixture: field=DataFixture()"
        next_model = get_related_model(field)
        return fixture.generate_data(next_model)

    def _get_data_from_a_custom_function(self, field, fixture):
        "return data of a custom function: field=lambda field: field.name"
        data = fixture(field)
        return data

    def _get_data_from_static_data(self, field, fixture):
        "return date from a static value: field=3"
        if hasattr(field, 'auto_now_add') and field.auto_now_add:
            self.fields_to_disable_auto_now_add.append(field)
        if hasattr(field, 'auto_now') and field.auto_now:
            self.fields_to_disable_auto_now.append(field)
        return fixture

    def _process_field_with_customized_fixture(self, instance, field, fixture, persist_dependencies):
        "Set a custom value to a field."
        if isinstance(fixture, DynamicFixture): # DynamicFixture (F)
            data = self._get_data_from_custom_dynamic_fixture(field, fixture, persist_dependencies)
        elif isinstance(fixture, Copier): # Copier (C)
            data = self._get_data_from_custom_copier(instance, field, fixture)
        elif isinstance(fixture, DataFixture): # DataFixture
            data = self._get_data_from_data_fixture(field, fixture)
        elif callable(fixture): # callable with the field as parameters
            data = self._get_data_from_a_custom_function(field, fixture)
        else: # attribute value
            data = self._get_data_from_static_data(field, fixture)
        return data

    def _process_foreign_key(self, model_class, field, persist_dependencies):
        "Returns auto-generated value for a field ForeignKey or OneToOneField."
        if field_is_a_parent_link(field):
            return None
        next_model = get_related_model(field)
        occurrences = self.model_path.count(next_model)
        if occurrences >= self.number_of_laps:
            data = None
        else:
            next_model_path = self.model_path[:]
            next_model_path.append(model_class)
            if model_class == next_model: # self reference
                # propagate ignored_fields only for self references
                ignore_fields = self.ignore_fields
            else:
                ignore_fields = []
            # need a new DynamicFixture to control the cycles and ignored fields.
            fixture = DynamicFixture(data_fixture=self.data_fixture,
                                     fill_nullable_fields=self.fill_nullable_fields,
                                     ignore_fields=ignore_fields,
                                     number_of_laps=self.number_of_laps,
                                     use_library=self.use_library,
                                     validate_models=self.validate_models,
                                     validate_args=self.validate_args,
                                     print_errors=self.print_errors,
                                     model_path=next_model_path)
            if persist_dependencies:
                data = fixture.get(next_model)
            else:
                data = fixture.new(next_model, persist_dependencies=persist_dependencies)
        return data

    def _process_field_with_default_fixture(self, field, model_class, persist_dependencies):
        "The field has no custom value, so the default behavior of the tool is applied."
        if field.null and not self.fill_nullable_fields:
            return None
        if field_has_default_value(field):
            if callable(field.default):
                data = field.default() # datetime default can receive a function: datetime.now
            else:
                data = field.default
        elif field_has_choices(field):
            data = field.flatchoices[0][0] # key of the first choice
        elif is_relationship_field(field):
            data = self._process_foreign_key(model_class, field, persist_dependencies)
        else:
            data = self.data_fixture.generate_data(field)
        return data

    def set_data_for_a_field(self, model_class, __instance, __field, persist_dependencies=True, **kwargs):
        if __field.name in kwargs:
            config = kwargs[__field.name]
            try:
                data = self._process_field_with_customized_fixture(__instance, __field, config, persist_dependencies)
            except PendingField:
                return # ignore this field for a while.
            except Exception as e:
                six.reraise(InvalidConfigurationError, InvalidConfigurationError(get_unique_field_name(__field), e), sys.exc_info()[2])
        else:
            data = self._process_field_with_default_fixture(__field, model_class, persist_dependencies)

        if is_file_field(__field) and data:
            django_file = data
            if isinstance(django_file, File):
                setattr(__instance, __field.name, data.name) # set the attribute
                if hasattr(django_file.file, 'mode') and django_file.file.mode != 'rb':
                    django_file.file.close() # this file may be open in another mode, for example, in a+b
                    opened_file = open(django_file.file.name, 'rb') # to save the file it must be open in rb mode
                    django_file.file = opened_file # we update the reference to the rb mode opened file

                # https://github.com/paulocheque/django-dynamic-fixture/issues/10
                # getattr(__instance, __field.name).save(django_file.name, django_file) # save the file into the file storage system
                # django_file.close()
                getattr(instance, field.name).save(django_file.name, django_file, save=False)

            else: # string (saving just a name in the file, without saving the file to the storage file system
                setattr(__instance, __field.name, data) # Model.field = data
        else:
            if self.debug_mode:
                LOGGER.debug('%s.%s = %s' % (get_unique_model_name(model_class), __field.name, data))
            try:
                setattr(__instance, __field.name, data) # Model.field = data
            except ValueError as e:
                if is_relationship_field(__field):
                    setattr(__instance, "%s_id" % __field.name, data) # Model.field = data
                else:
                    six.reraise(*sys.exc_info())
        self.fields_processed.append(__field.name)

    def _validate_kwargs(self, model_class, kwargs):
        "validate all kwargs match Model.fields."
        for field_name in kwargs.keys():
            if field_name in self._DDF_CONFIGS:
                continue
            if not model_has_the_field(model_class, field_name):
                raise InvalidConfigurationError('Field "%s" does not exist.' % field_name)

    def _configure_params(self, model_class, shelve, named_shelve, **kwargs):
        """
        1) validate kwargs
        2) load default fixture from DDF library. Store default fixture in DDF library.
        3) Load fixtures defined in F attributes.
        """
        if self.validate_args:
            self._validate_kwargs(model_class, kwargs)
        library = DDFLibrary.get_instance()
        if shelve: # shelving before use_library property: do not twist two different configurations (anti-pattern)
            for field_name in kwargs.keys():
                if field_name in self._DDF_CONFIGS:
                    continue
                field = get_field_by_name_or_raise(model_class, field_name)
                fixture = kwargs[field_name]
                if field.unique and not (isinstance(fixture, (DynamicFixture, Copier, DataFixture)) or callable(fixture)):
                    raise InvalidConfigurationError('It is not possible to store static values for fields with unique=True (%s)' % get_unique_field_name(field))
            library.add_configuration(model_class, kwargs, name=shelve)
        if self.use_library:
            # load ddf_setup.py of the model application
            app_name = get_app_name_of_model(model_class)
            if app_name not in _LOADED_DDF_SETUP_MODULES:
                full_module_name = '%s.tests.ddf_setup' % app_name
                try:
                    _LOADED_DDF_SETUP_MODULES.append(app_name)
                    import_module(full_module_name)
                except ImportError:
                    pass # ignoring if module does not exist
                except Exception as e:
                    six.reraise(InvalidDDFSetupError, InvalidDDFSetupError(e), sys.exc_info()[2])
            configuration_default = library.get_configuration(model_class, name=DDFLibrary.DEFAULT_KEY)
            configuration_custom = library.get_configuration(model_class, name=named_shelve)
            configuration = {}
            configuration.update(configuration_default) # always use default configuration
            configuration.update(configuration_custom) # override default configuration
            configuration.update(kwargs) # override shelved configuration with current configuration
        else:
            configuration = kwargs
        configuration.update(self.kwargs) # Used by F: kwargs are passed by constructor, not by get.
        return configuration

    def new(self, model_class, shelve=False, named_shelve=None, persist_dependencies=True, **kwargs):
        """
        Create an instance filled with data without persist it.
        1) validate all kwargs match Model.fields.
        2) validate model is a model.Model class.
        3) Iterate model fields: for each field, fill it with data.

        :shelve: the current configuration will be stored in the DDF library. It can be True or a string (named shelve).
        :named_shelve: restore configuration saved in DDF library with a name.
        :persist_dependencies: tell if internal dependencies will be saved in the database or not.
        """
        if self.debug_mode:
            LOGGER.debug('>>> [%s] Generating instance.' % get_unique_model_name(model_class))
        configuration = self._configure_params(model_class, shelve, named_shelve, **kwargs)
        instance = model_class()
        if not is_model_class(instance):
            raise InvalidModelError(get_unique_model_name(model_class))
        for field in get_fields_from_model(model_class):
            if is_key_field(field) and 'id' not in configuration: continue
            if field.name in self.ignore_fields and field.name not in self.kwargs: continue
            self.set_data_for_a_field(model_class, instance, field, persist_dependencies=persist_dependencies, **configuration)
        number_of_pending_fields = len(self.pending_fields)
        # For Copier fixtures: dealing with pending fields that need to receive values of another fields.
        i = 0
        while self.pending_fields != []:
            field_name = self.pending_fields.pop(0)
            field = get_field_by_name_or_raise(model_class, field_name)
            self.set_data_for_a_field(model_class, instance, field, persist_dependencies=persist_dependencies, **configuration)
            i += 1
            if i > 2 * number_of_pending_fields: # dealing with infinite loop too.
                raise InvalidConfigurationError(get_unique_field_name(field), 'Cyclic dependency of Copiers.')
        if self.debug_mode:
            LOGGER.debug('<<< [%s] Instance created.' % get_unique_model_name(model_class))
        return instance

    def _process_many_to_many_field(self, field, manytomany_field, fixture, instance):
        """
        Set ManyToManyField fields with or without 'trough' option.

        :field: model field.
        :manytomany_field: ManyRelatedManager of the field.
        :fixture: value passed by user.
        """
        next_model = get_related_model(field)
        if isinstance(fixture, int):
            amount = fixture
            for _ in range(amount):
                next_instance = self.get(next_model)
                self._create_manytomany_relationship(manytomany_field, instance, next_instance)
        elif isinstance(fixture, (list, tuple)):
            items = fixture
            for item in items:
                if isinstance(item, DynamicFixture):
                    next_instance = item.get(next_model, **item.kwargs) # need to pass F.kwargs recursively.
                else:
                    next_instance = item

                self._create_manytomany_relationship(manytomany_field, instance, next_instance)
        else:
            raise InvalidManyToManyConfigurationError('Field: %s' % field.name, str(fixture))

    def _create_manytomany_relationship(self, manytomany_field, instance, next_instance):
        try:
            manytomany_field.add(next_instance)
        except AttributeError:
            next_instance.save()

            # Create an instance of the "through" model using the current data fixture
            through_model = manytomany_field.through
            through_instance = DynamicFixture(data_fixture=self.data_fixture) \
                    .get(through_model, **{
                        manytomany_field.source_field_name: instance,
                        manytomany_field.target_field_name: next_instance
                    })

    def _save_the_instance(self, instance):
        for field in self.fields_to_disable_auto_now:
            disable_auto_now(field)
        for field in self.fields_to_disable_auto_now_add:
            disable_auto_now_add(field)
        instance.save()
        for field in self.fields_to_disable_auto_now:
            enable_auto_now(field)
        for field in self.fields_to_disable_auto_now_add:
            enable_auto_now_add(field)

    def get(self, model_class, shelve=False, named_shelve=None, **kwargs):
        """
        Create an instance with data and persist it.

        :shelve: the current configuration will be stored in the DDF library.
        :named_shelve: restore configuration saved in DDF library with a name.
        """
        instance = self.new(model_class, shelve=shelve, named_shelve=named_shelve, **kwargs)
        if is_model_abstract(model_class):
            raise InvalidModelError(get_unique_model_name(model_class))
        try:
            if self.validate_models:
                instance.full_clean()
            if model_class in _PRE_SAVE:
                try:
                    _PRE_SAVE[model_class](instance)
                except Exception as e:
                    six.reraise(InvalidReceiverError, InvalidReceiverError(e), sys.exc_info()[2])
            self._save_the_instance(instance)
            if model_class in _POST_SAVE:
                try:
                    _POST_SAVE[model_class](instance)
                except Exception as e:
                    six.reraise(InvalidReceiverError, InvalidReceiverError(e), sys.exc_info()[2])
        except Exception as e:
            if self.print_errors:
                print_field_values(instance)
            six.reraise(BadDataError, BadDataError(get_unique_model_name(model_class), e), sys.exc_info()[2])
        self.fields_processed = [] # TODO: need more tests for M2M and Copier
        self.pending_fields = []
        for field in get_many_to_many_fields_from_model(model_class):
            if field.name in kwargs.keys(): # TODO: library
                manytomany_field = getattr(instance, field.name)
                fixture = kwargs[field.name]
                try:
                    self._process_many_to_many_field(field, manytomany_field, fixture, instance)
                except InvalidManyToManyConfigurationError as e:
                    six.reraise(InvalidManyToManyConfigurationError, e, sys.exc_info()[2])
                except Exception as e:
                    six.reraise(InvalidManyToManyConfigurationError, InvalidManyToManyConfigurationError(get_unique_field_name(field), e), sys.exc_info()[2])
        return instance
