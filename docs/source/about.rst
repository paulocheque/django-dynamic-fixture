.. about:

About
*******************************************************************************


Change Log
===============================================================================

Date format: yyyy/mm/dd

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

Collaborators
===============================================================================

Paulo Cheque <http://twitter.com/paulocheque> <https://github.com/paulocheque>

Valder Gallo <http://valdergallo.com.br> <https://github.com/valdergallo>

Julio Netto <http://www.inerciasensorial.com.br> <https://bitbucket.org/inerte>


Pull Requests tips
===============================================================================

About commit messages
-------------------------------------------------------------------------------

* Messages in english only
* All messages have to follow the pattern: "[TAG] message"
* TAG have to be one of the following: new, update, bugfix, delete, refactoring, config, log, doc, mergefix

About the code
-------------------------------------------------------------------------------

* One change (new feature, update, refactoring, bugfix etc) by commit
* All bugfix must have a test simulating the bug
* All commit must have 100% of test coverage

Running tests
-------------------------------------------------------------------------------

Command::

    python manage.py test --with-coverage --cover-inclusive --cover-html --cover-package=django_dynamic_fixture.* --with-queries --with-ddf-setup

TODO list
===============================================================================

Tests and Bugfixes
-------------------------------------------------------------------------------
* with_queries bugfixes (always print 0 queries)
* Deal with relatioships with dynamic related_name
* bugfix in fdf or ddf: some files/directories are not deleted
* tests with files in ddf
* tests with proxy models
* tests with GenericRelations, GenericForeignKey etc
* more tests with OneToOneField(parent_link=True)
* Test with python 2.4
* Test with python 2.5
* Test with python 3.*

Features
-------------------------------------------------------------------------------
* auto config of denormalizated fields
* related_name documentation or workaround
* today, yesterday, tomorrow on fdf
* string generation according to a regular expression

Documentation
-------------------------------------------------------------------------------
* with_queries documentation
* example to generate models with validators in fields or in clean methods
