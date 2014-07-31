.. _more:

Other DDF Configurations
*******************************************************************************

Decorators (New in 1.4.0)
===============================================================================

Example::

    from django_dynamic_fixture.decorators import skip_for_database, only_for_database, SQLITE3, POSTGRES

    @skip_for_database(SQLITE3)
    def test_some_feature_that_use_raw_sql_not_supported_by_sqlite(self): pass

    @only_for_database(POSTGRES)
    def test_some_feature_that_use_raw_sql_specific_to_my_production_database(self): pass

It is possible to pass a custom string as argument, one that would be defined in settings.DATABASES['default']['ENGINE']::

    @skip_for_database('my custom driver')
    @only_for_database('my custom driver')


Validation
===============================================================================

Validate Models (New in 1.5.0)
-------------------------------------------------------------------------------
This option is a flag to determine if the method *full_clean* of model instances will be called before DDF calls the save method.

In settings.py::

    DDF_VALIDATE_MODELS = False

In the test file::

    G(MyModel, validate_models=True)


Validate Arguments (New in 1.5.0)
-------------------------------------------------------------------------------

This option is a flag to determine if field names passed to **G** and **N** function will be validated. In other words, DDF will check if the model has the field.

In settings.py::

    DDF_VALIDATE_ARGS = True # default = False for compatiblity reasons, but it is recommended to activate this option.

In the test file::

    G(MyModel, validate_args=True, mymodel_does_not_contains_this_field=999) # this will raise an error


Signals PRE_SAVE and POST_SAVE:
===============================================================================

In very special cases a signal may facilitate implementing tests with DDF, but Django signals may not be satisfatory for testing pourposes because the developer do not have control of the execution order of the receivers. For this reason, DDF provides its own signals. It is possible to have only one receiver for each model, to avoid anti-patterns::

    from django_dynamic_fixture import PRE_SAVE, POST_SAVE
    def callback_function(instance):
        pass # do something
    PRE_SAVE(MyModel, callback_function)
    POST_SAVE(MyModel, callback_function)


Debugging
===============================================================================

Print model instance values: P
-------------------------------------------------------------------------------

Print all field values of an instance. You can pass also a list of instances or a *QuerySet*. It is useful for debug::

    from django_dynamic_fixture import G, P

    P(G(Model))
    P(G(Model, n=2))
    P(Model.objects.all())

    # This will print some thing like that:
    # :: Model my_app.MyModel (12345)
    # id: 12345
    # field_x: 'abc'
    # field_y: 1
    # field_z: 1


Debug Mode (New in 1.6.2)
-------------------------------------------------------------------------------

Print debug log of DDF.

In settings.py::

    DDF_DEBUG_MODE = True # default = False

In the test file::

    G(MyModel, debug_mode=True)


List of Exceptions
-------------------------------------------------------------------------------

* *UnsupportedFieldError*: DynamicFixture does not support this field.
* *InvalidConfigurationError*: The specified configuration for the field can not be applied or it is bugged.
* *InvalidManyToManyConfigurationError*: M2M attribute configuration must be a number or a list of DynamicFixture or model instances.
* *BadDataError*: The data passed to a field has some problem (not unique or invalid) or a required attribute is in ignore list.
* *InvalidCopierExpressionError*: The specified expression used in a Copier is invalid.
* *InvalidModelError*: Invalid Model: The class is not a model or it is abstract.
* *InvalidDDFSetupError*: ddf_setup.py has execution errors

