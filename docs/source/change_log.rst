.. about:

Change Log
*******************************************************************************

.. contents::
   :local:

Date format: yyyy/mm/dd

Version 3.1.0 - 2020/03/29
-------------------------------------------------------------------------------
  * <http://pypi.python.org/pypi/django-dynamic-fixture/3.1.0>
  * Compatibility check report improvements: PR #131
  * DDF now accepts to override a DDF lesson: PR #130
  * New feature: DDF Mask: ``M``: PR #129
  * Option to configure DDF via Environment variables

Version 3.0.3 - 2020/03/01
-------------------------------------------------------------------------------
  * <http://pypi.python.org/pypi/django-dynamic-fixture/3.0.3>
  * Setting ``DDF_NUMBER_OF_LAPS`` was removed in favor of the new ``DDF_FK_MIN_DEPTH``
  * Parameter ``number_of_laps`` was removed in favor of new ``fk_min_depth``
  * Important bugfix for the FK field management: Issue #120
  * Give priority to default values instead of null values: Issue #121
  * Fixed lookup fields that was breaking JSONFields: Issue #122

Version 3.0.2 - 2020/01/10
-------------------------------------------------------------------------------
  * <http://pypi.python.org/pypi/django-dynamic-fixture/3.0.2>
  * Changed ``VERSION`` to ``__version__``: ``from ddf import __version``
  * Changed ``lesson`` to ``ddf_lesson``:  ``G(Model, ddf_lesson='...')``

Version 3.0.1 - 2020/01/07
-------------------------------------------------------------------------------
  * <http://pypi.python.org/pypi/django-dynamic-fixture/3.0.1>
  * Fixed importing ``from ddf import ddf_check_models``
  * Added a CSV report for the ddf_check_models
  * Added the VERSION property in ddf: ``from ddf import VERSION``

Version 3.0.0 - 2020/01/05
-------------------------------------------------------------------------------
  * <http://pypi.python.org/pypi/django-dynamic-fixture/3.0.0>
  * New ``teach`` method that replaced the old ``shelve=True``.
  * Support to ``app_label.ModelName`` strings instead of the model class.
  * New ``ddf`` shortcut: ``from ddf import G, N, C, P, teach``.
  * Support for **Django 3.0.0**.
  * New ``ddf_check_models`` method to print a compatibility report.
  * Added Python 3 Type Hints.
  * Added native support for the ``Postgres.JSONField``.
  * Added native support for Django-Polymorphic models.
  * Bugfix for the ``data_fixture`` parameter to accept string alias.
  * Another small bugfixes with ``choices`` parameter.
  * Many internal refactorings.
  * Travis/Tests integration fixed.
  * Documentation organised, updated and simplified.
  * Changed the default value of the ``persist_dependencies`` in ``N`` from True to False.
  * DDF_USE_LIBRARY settings removed. Now, it is always activated by default.
  * DDF_VALIDATE_ARGS settings removed. Now, it is always activated by default.
  * DDF_FILL_NULLABLE_FIELDS default changed from True to False
  * DDF_NUMBER_OF_LAPS default changed from 1 to 0
  * Bugfix for named primary keys.

Version 2.0.0 - 2017/12/08
-------------------------------------------------------------------------------
  * <http://pypi.python.org/pypi/django-dynamic-fixture/2.0.0>
  * `DDF_IGNORE_FIELDS` globally for all new instances
  * Bugfix for auto generated `_ptr` fields.
  * Support for Django 2.0.0.

Version 1.9.5 - 2017/05/09
-------------------------------------------------------------------------------
  * <http://pypi.python.org/pypi/django-dynamic-fixture/1.9.5>
  * Bugfix: avoid GDALException on Django 1.11

Version 1.9.4 - 2017/04/17
-------------------------------------------------------------------------------
  * <http://pypi.python.org/pypi/django-dynamic-fixture/1.9.4>
  * Added support for django.contrib.postgres.fields.ArrayField field
  * Fixed GeoDjango Point instantiation.

Version 1.9.3 - 2017/03/08
-------------------------------------------------------------------------------
  * <http://pypi.python.org/pypi/django-dynamic-fixture/1.9.3>
  * Improve compatibility for the DDF internal tests

Version 1.9.2 - 2017/03/08
-------------------------------------------------------------------------------
  * <http://pypi.python.org/pypi/django-dynamic-fixture/1.9.2>
  * Django 2.0 compatibility
  * New: Support for wildcards `?` and `*` in the ignore fields
  * Bugfix: Fixed DDF_TEST_GEODJANGO test issues

Version 1.9.1 - 2016/12/21
-------------------------------------------------------------------------------
  * <http://pypi.python.org/pypi/django-dynamic-fixture/1.9.1>
  * Bugfix: Django version parser
  * Bugfix: NameError on invalid variable name

Version 1.9.0 - 2016/05/23
-------------------------------------------------------------------------------
  * <http://pypi.python.org/pypi/django-dynamic-fixture/1.9.0>
  * [New] Django 1.9 support
  * [Bugfix] Fixed issue on ForeignKey field with default id
  * [Bugfix] Fixed issue with SimpleUploadedFile

Version 1.8.4 - 2015/05/26
-------------------------------------------------------------------------------
  * <http://pypi.python.org/pypi/django-dynamic-fixture/1.8.4>
  * [New] UUIDField support
  * [New] GeoDjango fields support (GeometryField, PointField, LineStringField, PolygonField, MultiPointField, MultiLineStringField, MultiPolygonField, GeometryCollectionField)
  * [Update] Better error messages
  * [Bugfix] BinaryField fixture fix
  * [Update] Optimizations


Version 1.8.3 - 2015/05
-------------------------------------------------------------------------------
  * <http://pypi.python.org/pypi/django-dynamic-fixture/1.8.3>
  * [Update] No more deprecated methods


Version 1.8.2 - 2015/05
-------------------------------------------------------------------------------
  * <http://pypi.python.org/pypi/django-dynamic-fixture/1.8.2>
  * [New] Support for Django 1.8


Version 1.8.1 - 2014/12
-------------------------------------------------------------------------------
  * <http://pypi.python.org/pypi/django-dynamic-fixture/1.8.1>
  * [Update] Avoid conflicts with "instance" and "field" model field names.

Version 1.8.0 - 2014/09
-------------------------------------------------------------------------------
  * <http://pypi.python.org/pypi/django-dynamic-fixture/1.8.0>
  * [New] DDF_FIELD_FIXTURES global settings. You can include support of other fields here.
  * [New] Support for BinaryField
  * [Update] Django 1.7, Python 3.4 and Pypy official suppport (fixed some tests)
  * [New] ReadTheDocs full documentation
  * [Update] Fixed some print calls for python 3
  * [Update] Nose plugin disable as default. Recommended behavior of nose plugins.
  * [Update] ignore_fields parameter does not consider fields explicitly defined by the developer.
  * [Update] Travis env using Tox

Version 1.7.0 - 2014/03/26
-------------------------------------------------------------------------------

  * <http://pypi.python.org/pypi/django-dynamic-fixture/1.7.0>

Version 1.6.4 - 2012/12/30
-------------------------------------------------------------------------------
  * <http://pypi.python.org/pypi/django-dynamic-fixture/1.6.4>
  * [Bugfix] auto_now and auto_now_add must not be disabled forever (thanks for reporting)
  * [New] Added global_sequential data fixture (Pull request, thanks)

Version 1.6.3 - 2012/04/10
-------------------------------------------------------------------------------
  * <http://pypi.python.org/pypi/django-dynamic-fixture/1.6.3>
  * [New] Pre save and post save special signals

Version 1.6.2 - 2012/04/09
-------------------------------------------------------------------------------
  * <http://pypi.python.org/pypi/django-dynamic-fixture/1.6.2>
  * [New] Debug Mode and option (global/local) to enable/disable debug mode

Version 1.6.1 - 2012/04/07
-------------------------------------------------------------------------------
  * <http://pypi.python.org/pypi/django-dynamic-fixture/1.6.1>
  * [New] New alias for F: field1__field2=value instead of field1=F(field2=value)
  * [New] Named shelves inherit from default shelve

Version 1.6.0 - 2012/03/31
-------------------------------------------------------------------------------
  * <http://pypi.python.org/pypi/django-dynamic-fixture/1.6.0>
  * [New] Copier: option to copy a generated value for a field to another one. Useful for denormalizated fields.
  * [New] Shelve/Library: option to store a default configuration of a specific model. Useful to avoid replicated code of fixtures. Global option: DDF_USE_LIBRARY.
  * [New] Named Shelve: option to store multiple configurations for a model in the library.
  * [New] Nose plugin for global set up.
  * [New] P function now accept a queryset.

Version 1.5.1 - 2012/03/26
-------------------------------------------------------------------------------
  * <http://pypi.python.org/pypi/django-dynamic-fixture/1.5.0>
  * [New] global option: DDF_VALIDATE_ARGS that enable or disable field names.
  * [Bugfix] F feature stop working.

Version 1.5.0 - 2012/03/25
-------------------------------------------------------------------------------
  * <http://pypi.python.org/pypi/django-dynamic-fixture/1.5.0>
  * [New] global settings: DDF_DEFAULT_DATA_FIXTURE, DDF_FILL_NULLABLE_FIELDS, DDF_IGNORE_FIELDS, DDF_NUMBER_OF_LAPS, DDF_VALIDATE_MODELS
  * [New] new data fixture that generates random data
  * [New] new data fixture that use sequential numbers only for fields that have unique=True
  * [New] P function now accept a list of model instances
  * [New] Option to call model_instance.full_clean() validation method before saving the object (DDF_VALIDATE_MODELS).
  * [New] Validate field names. If a invalid field name is passed as argument, it will raise an InvalidConfigurationError exception.
  * [Bugfix] DateField options 'auto_add_now' and 'auto_add' are disabled if a custom value is used.

Version 1.4.3 - 2012/02/23
-------------------------------------------------------------------------------
  * <http://pypi.python.org/pypi/django-dynamic-fixture/1.4.3>
  * [Bugfix] Bugfix in ForeignKeys with default values

Version 1.4.2 - 2011/11/07
-------------------------------------------------------------------------------
  * <http://pypi.python.org/pypi/django-dynamic-fixture/1.4.2>
  * [Bugfix] Bugfix in FileSystemDjangoTestCase

Version 1.4.1 - 2011/11/07
-------------------------------------------------------------------------------
  * <http://pypi.python.org/pypi/django-dynamic-fixture/1.4.1>
  * [New] Now you can set a custom File to a FileField and the file will be saved in the file storage system.
  * **FileSystemDjangoTestCase**:
  * [New] create_django_file_using_file create a django.File using the content of your file
  * [New] create_django_file_with_temp_file now accepts a content attribute that will be saved in the generated file
  * [Bugfix] now create_django_file_with_temp_file close the generated file

Version 1.4.0 - 2011/10/29
-------------------------------------------------------------------------------
  * <http://pypi.python.org/pypi/django-dynamic-fixture/1.4.0>
  * [New] Nose plugin to count queries on each test
  * [New] Command line to count queries on the save (insert and update) of each model
  * [Update] Field with choice and default must use the default value, not the first choice value
  * [Update] Validation if the class is a models.Model instance
  * [Update] Showing all stack trace, when an exception occurs

  * **Decorators**:
  * [Bugfix] default values of database engines were not used correctly
  * **FileSystemDjangoTestCase**:
  * [Testfix] Fixing tests

Version 1.3.1 - 2011/10/03
-------------------------------------------------------------------------------
  * <http://pypi.python.org/pypi/django-dynamic-fixture/1.3.1>
  * [Bugfix] Bugfixes in FileSystemDjangoTestCase

Version 1.3.0 - 2011/10/03
-------------------------------------------------------------------------------
  * <http://pypi.python.org/pypi/django-dynamic-fixture/1.3.0>
  * [New] File System Django Test Case
  * [New] Decorators skip_for_database and only_for_database
  * [Bugfix] Inheritance problems, before this version the DDF filled fields with the attribute parent_link

Version 1.2.3 - 2011/06/27
-------------------------------------------------------------------------------
  * <http://pypi.python.org/pypi/django-dynamic-fixture/1.2.3>
  * [Bugfix] string truncation to max_length

Version 1.2.2 - 2011/05/05
-------------------------------------------------------------------------------
  * <http://pypi.python.org/pypi/django-dynamic-fixture/1.2.2>
  * [Update] Improvements in exception messages

Version 1.2.1 - 2011/03/11
-------------------------------------------------------------------------------
  * <http://pypi.python.org/pypi/django-dynamic-fixture/1.2.1>
  * [Bugfix] Propagate ignored fields to self references
  * [Refact] Refactoring

Version 1.2 - 2011/03/04
-------------------------------------------------------------------------------
  * <http://pypi.python.org/pypi/django-dynamic-fixture/1.2>
  * [New] ignore_fields
  * [New] now it is possible to set the ID

Version 1.1
-------------------------------------------------------------------------------
  * <http://pypi.python.org/pypi/django-dynamic-fixture/1.0> (1.0 has the 1.1 package)
  * [Bugfix] Bug fixes for 1.0

Version 1.0
-------------------------------------------------------------------------------
  * Initial version
  * Ready to use in big projects
