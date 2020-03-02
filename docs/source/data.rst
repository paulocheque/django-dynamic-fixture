.. _data:

Field Data Generation
*******************************************************************************

.. contents::
   :local:

Supported Fields
===============================================================================

* **Numbers**: IntegerField, SmallIntegerField, PositiveIntegerField, PositiveSmallIntegerField, BigIntegerField, FloatField,DecimalField

* **Strings**: CharField, TextField, SlugField, CommaSeparatedintegerField

* **Booleans**: BooleanField, NullBooleanField

* **Timestamps**: DateField, TimeField, DatetimeField

* **Utilities**: EmailField, UrlField, IPAddressField, GenericIPAddressField, XMLField, UUIDField

* **Files**: FilePathField, FileField, ImageField

* **Binary**: BinaryField

* **Postgres**: JSONField, ArrayField

* **GIS/Django Geo**: Geometryfield, PointField, LineStringField, PolygonField, MultiPointField, MultiLineStringField, MultiPolygonField, GeometryCollectionField

Use ``DDF_FIELD_FIXTURES`` settings, customized data or even the field default values to deal with not supported fields.


GeoDjango Fields
===============================================================================

After `1.8.4` version, DDF has native support for GeoDjango fields: GeometryField, PointField, LineStringField, PolygonField, MultiPointField, MultiLineStringField, MultiPolygonField, GeometryCollectionField.

For older versions of DDF, please, use the following approach:

You can use ``DDF_FIELD_FIXTURES`` to create fixtures for Geo Django fields::

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
* You can also set the field fixture using the ``DDF_FIELD_FIXTURES`` settings. (new in 1.8.0)
* if a field is not default in Django, but it inherits from a Django field, it will be filled using its config.

* if a field is not default in Django and not related with a Django field, it will raise an ``UnsupportedFieldError``.
* if it does not recognize the Field class, it will raise an ``UnsupportedFieldError``.


Fill Nullable Fields
===============================================================================

This option define if nullable fields (fields with ``null=True``) will receive a generated data or not (``data=None``). It is possible to override the global option for an specific instance. But be careful because this option will be propagate to all internal dependencies.

In settings.py::

    DDF_FILL_NULLABLE_FIELDS = True

In the test file::

    instance = G(MyModel, fill_nullable_fields=False)
    assert instance.a_nullable_field is None
    assert instance.a_required_field is not None

    instance = G(MyModel, fill_nullable_fields=True)
    assert instance.a_nullable_field is not None
    assert instance.a_required_field is not None


Ignoring Fields (New in 1.2.0)
===============================================================================

This option defines a list of fields DDF will ignore. In other words, DDF will not fill it with dynamic data. This option can be useful for fields auto calculated by models, like [MPTT](https://github.com/django-mptt/django-mptt) models. Ignored fields are propagated ONLY to self references.

In settings.py::

    DDF_IGNORE_FIELDS = ['field_x', 'field_y'] # default = []

Ignored field names can use wildcard matching with '*' and '?' characters which substitute multiple or one character respectively. Wildcards are useful for fields that should not be populated and which match a pattern, like ``*_ptr`` fields for [django-polymorphic](https://github.com/django-polymorphic/django-polymorphic).

In settings.py::

    DDF_IGNORE_FIELDS = ['*_ptr'] # Ignore django-polymorphic pointer fields

It is not possible to override the global configuration, just extend the list. So use global option with caution::

    instance = G(MyModel, ignore_fields=['another_field_name'])
    assert instance.another_field_name is None


Minimum Foreign Key Depth
===============================================================================

This option is used by DDF to control dependencies and cyclic dependencies (``ForeignKey`` by ``self``, denormalizations, bad design etc). DDF does not enter infinite loop of instances generation. This option defines how depth DDF should go to create instances of foreign key fields. This option can also be used to create trees with different lengths.

In settings.py::

    DDF_FK_MIN_DEPTH = 0

In the test file::

    instance = G(MyModel, fk_min_depth=1)
    assert instance.self_fk.id is not None
    assert instance.self_fk.self_fk.id is None

    instance = G(MyModel, fk_min_depth=2)
    assert instance.self_fk.id is not None
    assert instance.self_fk.self_fk.id is not None
    assert instance.self_fk.self_fk.self_fk.id is None

> Incompatibility warning: Before DDF 3.0.3, DDF handled FK cycles instead of FK depth, through the removed properties `DDF_NUMBER_OF_LAPS` and `number_of_laps`.
