.. _data:

Field Data Generation
*******************************************************************************

Supported Fields
===============================================================================

* **Numbers**: IntegerField, SmallIntegerField, PositiveIntegerField, PositiveSmallIntegerField, BigIntegerField, FloatField,DecimalField

* **Strings**: CharField, TextField, SlugField, CommaSeparatedintegerField

* **Booleans**: BooleanField, NullBooleanField

* **Timestamps**: DateField, TimeField, DatetimeField

* **Utilities**: EmailField, UrlField, IPAddressField, XMLField

* **Files**: FilePathField, FileField, ImageField

* **Binary**: BinaryField

PS: Use **DDF_FIELD_FIXTURES** settings, customized data or even the field default values to deal with not supported fields.


GeoDjango Fields
===============================================================================

After `1.8.4` version, DDF has native support for GeoDjango fields: GeometryField, PointField, LineStringField, PolygonField, MultiPointField, MultiLineStringField, MultiPolygonField, GeometryCollectionField.

For older versions of DDF, please, use the following approach:

You can use DDF_FIELD_FIXTURES to create fixtures for Geo Django fields::

    # https://docs.djangoproject.com/en/dev/ref/contrib/gis/
    from django.contrib.gis.geos import Point
    DDF_FIELD_FIXTURES = {
        'django.contrib.gis.db.models.GeometryField': lambda: None,
        'django.contrib.gis.db.models.PointField': lambda: None,
        'django.contrib.gis.db.models.LineStringField': lambda: None,
        'django.contrib.gis.db.models.PolygonField': lambda: None,
        'django.contrib.gis.db.models.MultiPointField': lambda: None,
        'django.contrib.gis.db.models.MultiLineStringField': lambda: None,
        'django.contrib.gis.db.models.MultiPolygonField': lambda: None,
        'django.contrib.gis.db.models.GeometryCollectionField': lambda: None,
    }


About Custom Fields
===============================================================================

* Customized data is also valid for unsupported fields.
* You can also set the field fixture using the **DDF_FIELD_FIXTURES** settings. (new in 1.8.0)
* if a field is not default in Django, but it inherits from a Django field, it will be filled using its config.

* if a field is not default in Django and not related with a Django field, it will raise an *UnsupportedFieldError*.
* if it does not recognize the Field class, it will raise an *UnsupportedFieldError*.


Fill Nullable Fields
===============================================================================

This option define if nullable fields (fields with *null=True*) will receive a generated data or not (data=None). It is possible to override the global option for an specific instance. But be careful because this option will be propagate to all internal dependencies.

In settings.py::

    DDF_FILL_NULLABLE_FIELDS = True

In the test file::

    instance = G(MyModel, fill_nullable_fields=False)
    print instance.a_nullable_field # this will print None
    print instance.a_required_field # this will print a generated data

    instance = G(MyModel, fill_nullable_fields=True)
    print instance.a_nullable_field # this will print a generated data
    print instance.a_required_field # this will print a generated data


Ignoring Fields (New in 1.2.0)
===============================================================================

This option defines a list of fields DDF will ignore. In other words, DDF will not fill it with dynamic data. This option can be useful for fields auto calculated by models, like [MPTT](https://github.com/django-mptt/django-mptt) models. Ignored fields are propagated ONLY to self references.

In settings.py::

    DDF_IGNORE_FIELDS = ['field_x', 'field_y'] # default = []

It is not possible to override the global configuration, just extend the list. So use global option with caution::

    instance = G(MyModel, ignore_fields=['another_field_name'])
    print instance.another_field_name # this will print None


Number of Laps
===============================================================================

This option is used by DDF to control cyclic dependencies (*ForeignKey* by *self*, denormalizations, bad design etc). DDF does not enter infinite loop of instances generation. This option defines how many laps DDF will create for each cyclic dependency. This option can also be used to create trees with different lengths.

In settings.py::

    DDF_NUMBER_OF_LAPS = 1

In the test file::

    instance = G(MyModel, number_of_laps=1)
    print instance.self_fk.id # this will print the ID
    print instance.self_fk.self_fk.id # this will print None

    instance = G(MyModel, number_of_laps=2)
    print instance.self_fk.id # this will print the ID
    print instance.self_fk.self_fk.id  # this will print the ID
    print instance.self_fk.self_fk.self_fk.id # this will print None


Copier (New in 1.6.0)
===============================================================================

Copier is a feature to copy the data of a field to another one. It is necessary to avoid cycles in the copier expression. If a cycle is found, DDF will alert the programmer the expression is invalid::

    instance = G(MyModel, some_field=C('another_field'))
    print instance.some_field == instance.another_field # this will print True

    instance = G(MyModel, some_field=C('another_field'), another_field=50)
    print instance.some_field # this will print 50

It is possible to copy values of internal relationships, but only in the bottom-up way::

    instance = G(MyModel, some_field=C('some_fk_field.another_field'))
    print instance.some_field == instance.some_fk_field.another_field # this will print True


Default Shelve (New in 1.6.0)
===============================================================================

Sometimes DDF can not generate a valid and persisted instance because it contains custom fields or custom validations (field or model validation). In these cases it is possible to teach DDF how to build a valid instance. It is necessary to create a valid configuration and shelve it in an internal and global DDF library of configurations. All future instances of that model will use the shelved configuration as base. All custom configurations will override the shelved option just for the current model instance generation. But to use the default configuration it is necessary to enable the use of the DDF library.

In settings.py::

    DDF_USE_LIBRARY = True

In the test file::

    instance = G(Model, shelve=True, field_x=99)
    print instance.field_x # this will print 99

    instance = G(Model, use_library=True)
    print instance.field_x # this will print 99

    instance = G(Model, use_library=False)
    print instance.field_x # this will a dynamic generated data

It is possible to override shelved configuration::

    G(Model, shelve=True, field_x=888)
    instance = G(Model, use_library=True, field_x=999)
    print instance.field_x # this will print 999

It is possible to store custom functions of data fixtures for fields too::

    zip_code_data_fixture = lambda field: 'MN 55416'
    instance = G(Model, shelve=True, zip_code=zip_code_data_fixture)

    instance = G(Model, use_library=True)
    print instance.zip_code # this will print 'MN 55416'

It is possible to store Copiers too::

    instance = G(Model, shelve=True, x=C('y'))

    instance = G(Model, use_library=True, y=5)
    print instance.x # this will print 5

If the model is used by another applications, it is important to put the code that shelve configurations in the file *your_app.tests.ddf_setup.py* because DDF can not control the order tests will be executed, so a test of other application can be executed before the valid configuration is shelved. The file *ddf_setup.py* prevents this, because it is loaded before DDF starts to generate the instance of a particular model. It works like a "setup suite", like the DDF Setup Nose plugin.


Named Shelve (New in 1.6.0)
===============================================================================

The named shelve works like default shelve, but it has to have a name. It is possible to store more than one configuration by model type.

In settings.py::

    DDF_USE_LIBRARY = True

In the test file::

    G(Model, shelve='some name', field_x=888)
    G(Model, shelve='another name', field_x=999)

    instance = G(Model, named_shelve='some name', use_library=True)
    print instance.field_x # this will print 888

    instance = G(Model, named_shelve='another name', use_library=True)
    print instance.field_x # this will print 999

    instance = G(Model, named_shelve='some name', use_library=False)
    print instance.field_x # this will print a dynaimc generated data

If a DDF does not found the named shelve, it will raise an error::

    G(Model, named_shelve='name not found in DDF library', use_library=True)

It is important to note that all named shelve will inherit the configuration from the default shelve::

    G(Model, shelve=True, x=999)
    G(Model, shelve='some name', y=888)

    instance = G(Model, named_shelve='some name', use_library=True)
    print instance.x # this will print 999
    print instance.y # this will print 888

