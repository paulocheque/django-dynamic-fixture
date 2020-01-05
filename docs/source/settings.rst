.. _settings:

DDF Settings
===============================================================================

.. contents::
   :local:

.. role:: python(code)
   :language: python


Global Settings
-------------------------------------------------------------------------------

You can configure DDF in ``settings.py`` file. You can also override the global config per instance creation when necessary.

* **DDF_FILL_NULLABLE_FIELDS** (Default = False): DDF can fill nullable fields (``null=True``) with None or some data::

    # SomeModel(models.Model): nullable_field = Field(null=True)
    G(SomeModel).nullable_field is None # True if DDF_FILL_NULLABLE_FIELDS is True
    G(SomeModel).nullable_field is None # False if DDF_FILL_NULLABLE_FIELDS is False

    # You can override the global config for one case:
    assert G(Model, fill_nullable_fields=False).nullable_field is None
    assert G(Model, fill_nullable_fields=True).nullable_field is not None


*  **DDF_VALIDATE_MODELS** (Default = False): DDF will call ``model.full_clean()`` method before saving to the database::

    # You can override the global config for one case:
    G(Model, validate_models=True)
    G(Model, validate_models=False)


* **DDF_FIELD_FIXTURES** (Default = {}) (new in 1.8.0): Dictionary where the key is the full qualified name of the field and the value is a function without parameters that returns a value::

    DDF_FIELD_FIXTURES = {'path.to.your.Field': lambda: random.randint(0, 10) }


* **DDF_NUMBER_OF_LAPS** (Default = 0):  For models with foreign keys to itself (``ForeignKey('self')``), DDF will avoid infinite loops because it stops creating objects after it create **n** **laps** for the cycle::

    # You can override the global config for one case:
    G(Model, number_of_laps=5)


* **DDF_DEBUG_MODE** (Default = False): To show some DDF logs::

    # You can override the global config for one case:
    G(Model, debug_mode=True)
    G(Model, debug_mode=False)
