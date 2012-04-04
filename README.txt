=Description=
A full library to create dynamic model instances for testing purposes.

=Installation=
pip install django-dynamic-fixture

or

  # Download zip file
  # Extract it
  # Execute in the extracted directory: python setup.py install

=Upgrade=
pip install django-dynamic-fixture --upgrade --no-deps

=Motivation=
  * It is a TERRIBLE practice to use STATIC data in tests. 
  * Create dynamic fixture for each model is boring and it produces a lot of replicated code.
  * It is a bad idea to use uncontrolled data in tests, like bizarre random data.

=Comparison with another fixture tools=

  * We tried to use another fixture tools in a big Django project but the experience was not satisfactory. 
  * Either they are incomplete, or bugged or it produces erratic tests, because they use random and uncontrolled data.
  * Also, the syntax of others tools is too verbose, which polutes the tests.
  * Complete, lean and practice documentation.
  * It is hard to debug tests with another tools.
  * List of other tools: http://djangopackages.com/grids/g/fixtures

=Features=
  * Highly customizable: you can customize fields recursively
  * Deal with unique=True
  * Deal with cyclic dependencies (including self references)
  * Deal with many to many relationship (common M2M or M2M with additional data, i.e. through='table')
  * Deal with custom fields (specially if the custom field inherit of a django field)
  * It is supported for parallel tests
  * Deal with auto calculated attributes
  * It is easy to debug errors

=Example of Usage=

{{{
from django_dynamic_fixture import N, G, F, P
#or use old default names:
#from django_dynamic_fixture import new, get, DynamicFixture as F, print_field_values

# Models:

from django.db import models

class ModelA(models.Model): pass

class ModelY(models.Model):
    other_text = models.CharField()
    other_list = models.ManyToManyField('ModelA')

class ModelX(models.Model):
    some_text = models.CharField(null=True)
    parent_left = models.ForeingKey('self')
    y_reference = models.ForeingKey('ModelY')
    list_a = models.ManyToManyField('ModelA')

# Summary:

# DynamicFixture (F): receive arguments and create model instances.
# new: it is just a wrapper: it creates a F to create a not saved model instance.
# get: basically, call the new method and save the instance. You can set ManyToMany fields only after the instance is saved.

# Examples:

instance_of_modelx = N(ModelX)
assert instance_of_modelx.some_text != None
assert instance_of_modelx.parent_left != None
assert instance_of_modelx.parent_left.parent_left == None
assert instance_of_modelx.id == None # new do not save the instance
assert instance_of_modelx.y_reference.id != None # save dependencies by default
assert len(instance_of_modelx.list_a.all()) == 0 # do not create many2many fields by default

instance_of_modelx = N(ModelX, fill_nullable_fields=False) # default = True
assert instance_of_modelx.some_text == None

# you can ignore fields, but do not ignore required fields (with null=False).
instance_of_modelx = G(ModelX, ignore_fields=['some_text'])
assert instance_of_modelx.some_text == None

# Very nice feature to work with trees
instance_of_modelx = N(ModelX, number_of_laps=2) # default = 1
assert instance_of_modelx.parent_left != None
assert instance_of_modelx.parent_left.parent_left != None
assert instance_of_modelx.parent_left.parent_left.parent_left == None

# This feature is specially useful to test search methods
instance_of_modelx = N(ModelX, some_text='some fixed data') # attribute accepts static data
assert instance_of_modelx.some_text == 'some fixed data'

# Use this with attention. First, check for design mistakes
instance_of_modelx = N(ModelX, id=99999) # you can define the id too
assert instance_of_modelx.id == 99999

# You can create your own function to create data..
instance_of_modelx = N(ModelX, some_text=lambda field: field.name) # attribute accepts callables
assert instance_of_modelx.some_text == 'some_text'

# Use this with attention, you can get an error if you try to save an instance with not saved dependencies
instance_of_modelx = N(ModelX, persist_dependencies=False)
assert instance_of_modelx.y_reference.id == None

instance_of_modelx = G(ModelX) # get save the model instance
assert instance_of_modelx.id != None

instance_of_modelx = G(ModelX, list_a=2) # Many2Many can receive a number of instances to be created
assert len(instance_of_modelx.list_a.all()) == 2

instance_of_modelx = G(ModelX, list_a=[F(), F(), F()]) # Many2Many can receive a list of DynamicFixtures
assert len(instance_of_modelx.list_a.all()) == 3

a = G(ModelA)
instance_of_modelx = G(ModelX, list_a=[F(), a, F()]) # Many2Many can receive a list of instances
assert len(instance_of_modelx.list_a.all()) == 3

# You can pass arguments to F (DynamicFixture) recursively. This works for ForeignKey and ManyToMany Fields! Easy and customizable!
instance_of_modelx = G(ModelX, parent_left=F(other_text='wow', other_list=2))
assert len(instance_of_modelx.y_reference.other_list.all()) == 2

# Highly recursivable example:
# X has a ForeignKey to A
# A has a ForeignKey to B
# B has a ForeignKey to C
# this will create instances of C, B, A and X (in this order). Attribute d of C will be 'some value'
G(X, a=F(b=F(c=F(d='some value'))))


# for debug:
P(instance_of_modelx)

# Custom FileField:
class ModelX(models.Model):
    my_file = models.FileField(upload_to='/')

from tempfile import mkstemp
pdf_a = File(open(mkstemp()[1], 'w'), name='a.pdf')
G(ModelX, my_file=pdf_a)

# Copier
G(ModelX, my_field=C('my_field_y.x'))

# Shelve/Library
G(ModelX, my_field='x', shelve=True)
G(ModelX, use_library=True)

# Named Shelve
G(ModelX, my_field='x', shelve='some name')
G(ModelX, use_library=True, named_shelve='some name')


# Shelving before all tests of a module:
def setUpModule():
    N(ModelX, my_field='x', shelve=True)
    
# Shelving before all tests of all modules:
Put the code in the tests.py or tests/__init__.py of specific application.
N(ModelX, my_field='x', shelve=True)

OR

Add in ddf_setup.py:
N(ModelX, my_field='x', shelve=True)

Run with nose plugin:
python manage.py test --with-ddf-setup

}}}

== Decorators ==

{{{
from django_dynamic_fixture.decorators import skip_for_database, only_for_database, SQLITE3 

@only_for_database(SQLITE3)
def test_something1(self): pass

@skip_for_database(SQLITE3)
def test_something2(self): pass

@only_for_database("some value used in settings.DATABASES['default']['ENGINE']")
def test_something3(self): pass

@skip_for_database("some value used in settings.DATABASES['default']['ENGINE']")
def test_something4(self): pass
}}}

== Queries Module ==
{{{
python manage.py test --with-queries
python manage.py count_queries_on_save
}}}

=Information about the logic of the library=

==List of exceptions==
  * UnsupportedFieldError: DynamicFixture does not support this field.
  * InvalidConfigurationError: The specified configuration for the field can not be applied or it is bugged.
  * InvalidManyToManyConfigurationError: M2M attribute configuration must be a number or a list of DynamicFixture or model instances.
  * BadDataError: The data passed to a field has some problem (not unique or invalid) or a required attribute is in ignore list.
  * InvalidCopierExpressionError: The specified expression used in a Copier is invalid.
  * InvalidModelError: Invalid Model: The class is not a model or it is abstract.
  * InvalidDDFSetupError: ddf_setup.py has execution errors

==DynamicFixture assume==

  * if a field has a default value, it does not have unique=True.
  * if a field has choices, it does not have unique=True.
  * if there is a cyclic dependency, in some part the relationship must be nullable.
  * if any of these requirements is a problem, you have to use customized values or override the behavior.

==DynamicFixture rules==

===General===

  * The id (AutoField) is auto filled, unless you set a value to it.
  * if a field has default value, it will be used by default.
  * if a field has choices, it select each the first option by default.
  * it fill nullable fields with data unless fill_nullable_fields is False.
  * boolean fields will always receive False, unless it has default value.
  * null boolean fields will always receive None, unless it has default value.
  * Strings (CharField, Text, Url, Email...) and numbers (IntegerField, Float, Decimal...) are filled with a sequential and unique number for each test (1, '1', 2, '2'...). Each attribute has its own counter.
  * You can override the behavior of the string and number fillers, if you want to.

===Custom Attributes===

  * if it receive a customized data, it do not care about attributes null, unique, default or choices.
  * if the specified fixture was bugged, it will raise an InvalidConfigurationError.

===Custom Fields===

  * if it does not recognize the Field class, it will raise an UnsupportedFieldError.
  * if a field is not default in Django, but it inherits from a Django field, it will be filled using its config.
  * if a field is not default in Django and not related with a Django field, it will raise an UnsupportedFieldError.
  * Customized data is also valid for unsupported fields.

===Related Objects===

  * ForeignKey will be filled by default, considering unicity of data.
  * It deal with cyclic dependencies, including self references (this avoid infinite recursion).
  * By default, the fixture create just one cycle, but it is possible to specify more maps with number_of_laps parameter.


===Many to Many relationship===

  * To add models in a m2m relation, the model must be persisted, so use the 'get' method.
  * it expect to receive a parameter with the amount of instances that need to be created (using default configuration).
  * Also, it can receive a list with DynamicFixture (F) or model instances (for custom items). The size of the list is the number of items that will be created.
  * It works for default Many2Many and Many2Many with through.


===Ignoring fields===

  * Useful when some fields need some calculation. For example, Django-MPTT models.
  * Ignored fields are propagated ONLY to self references.
  * Do not ignore required fields with 'get', only with 'new'. In other words, do not save an instance without a required field, unless you are expecting for an exception.


===Patterns===

  * Use 'new' method for unit tests (not integration tests) for the main model.
  * Use 'ignore_fields' option to deal with fields filled by listeners.
  * Use custom values for unsupported fields.
  * Use 'number_of_laps' option to test trees.


===Anti-Patterns===

  * Use a auto generated data in an assertion method.


=Links of Comments=
  * http://www.reddit.com/r/django/comments/fv1re/django_dynamic_fixture
  * http://djangopackages.com/grids/g/fixtures/
  * http://news.ycombinator.com/item?id=2275406
  * http://pythonsmalltalk.blogspot.com/2011/02/django-dynamic-fixture.html
  * http://pythonsmalltalk.blogspot.com/2011/03/django-dynamic-fixture-121.html
  * http://pypi.python.org/pypi/django-dynamic-fixture/1.2
  * http://code.activestate.com/pypm/django-dynamic-fixture
  * http://groups.google.com/group/django-mptt-dev/browse_thread/thread/d9eb9e22ad4aa656
  * http://groups.google.com/group/django-users/browse_thread/thread/1346a60008c21a7b
  * http://groups.google.com/group/django-brasil/browse_thread/thread/757df09d3c3be81d
  * http://linux.softpedia.com/get/Internet/HTTP-WWW-/django-dynamic-fixture-68711.shtml


=Change Log=

==Version 1.6.1==
  * 2012/04/06 (yyyy/mm/dd)
  * New features in DDF:
  * New alias for F: field1__field2=value instead of field1=F(field2=value)

==Version 1.6.0==
  * 2012/03/31 (yyyy/mm/dd)
  * http://pypi.python.org/pypi/django-dynamic-fixture/1.6.0
  * New features in DDF:
  * Copier: option to copy a generated value for a field to another one. Useful for denormalizated fields.
  * Shelve/Library: option to store a default configuration of a specific model. Useful to avoid replicated code of fixtures. Global option: DDF_USE_LIBRARY.
  * Named Shelve: option to store multiple configurations for a model in the library.
  * Nose plugin for global set up.
  * P function now accept a queryset.

==Version 1.5.1==
  * 2012/03/26 (yyyy/mm/dd)
  * http://pypi.python.org/pypi/django-dynamic-fixture/1.5.0
  * New fatures in DDF:
  * global option: DDF_VALIDATE_ARGS that enable or disable field names.
  
  * BugFixes of 1.5.0:
  * F feature stop working.

==Version 1.5.0==
  * 2012/03/25 (yyyy/mm/dd)
  * http://pypi.python.org/pypi/django-dynamic-fixture/1.5.0
  * New features in DDF:
  * global settings: DDF_DEFAULT_DATA_FIXTURE, DDF_FILL_NULLABLE_FIELDS, DDF_IGNORE_FIELDS, DDF_NUMBER_OF_LAPS, DDF_VALIDATE_MODELS
  * new data fixture that generates random data
  * new data fixture that use sequential numbers only for fields that have unique=True
  * P function now accept a list of model instances
  * Option to call model_instance.full_clean() validation method before saving the object (DDF_VALIDATE_MODELS).
  * Validate field names. If a invalid field name is passed as argument, it will raise an InvalidConfigurationError exception.
  * DateField options 'auto_add_now' and 'auto_add' are disabled if a custom value is used.

==Version 1.4.3==
  * 2012/02/23 (yyyy/mm/dd)
  * http://pypi.python.org/pypi/django-dynamic-fixture/1.4.3
  * Bugfix in ForeignKeys with default values

==Version 1.4.2==
  * 2011/11/07 (yyyy/mm/dd)
  * http://pypi.python.org/pypi/django-dynamic-fixture/1.4.2
  * Bugfix in FileSystemDjangoTestCase

==Version 1.4.1==
  * 2011/11/07 (yyyy/mm/dd)
  * http://pypi.python.org/pypi/django-dynamic-fixture/1.4.1
  * New features in DDF:
  * Now you can set a custom File to a FileField and the file will be saved in the file storage system.
  
  * New features in FileSystemDjangoTestCase:
  * create_django_file_using_file create a django.File using the content of your file
  * create_django_file_with_temp_file now accepts a content attribute that will be saved in the generated file

  * Bugfix in FileSystemDjangoTestCase:
  * now create_django_file_with_temp_file close the generated file

==Version 1.4.0==
  * 2011/10/29 (yyyy/mm/dd)
  * http://pypi.python.org/pypi/django-dynamic-fixture/1.4.0
  * New features:
  * Nose plugin to count queries on each test
  * Command line to count queries on the save (insert and update) of each model
  
  * Bugfixes in DDF: 
  * Field with choice and default must use the default value, not the first choice value
  * Validation if the class is a models.Model instance
  * Showing all stack trace, when an exception occurs
  
  * Bugfixes in decorators: default values of database engines were not used correctly
  * Bugfixes in FileSystemDjangoTestCase tests

==Version 1.3.1==
  * 2011/10/03 (yyyy/mm/dd)
  * http://pypi.python.org/pypi/django-dynamic-fixture/1.3.1
  * Bugfixes in FileSystemDjangoTestCase

==Version 1.3.0==
  * 2011/10/03 (yyyy/mm/dd)
  * http://pypi.python.org/pypi/django-dynamic-fixture/1.3.0
  * New Feature: File System Django Test Case
  * New Feature: Decorators skip_for_database and only_for_database
  * Bugfix: Inheritance problems, before this version the DDF filled fields with the attribute parent_link 

==Version 1.2.3==

  * 2011/06/27 (yyyy/mm/dd)
  * http://pypi.python.org/pypi/django-dynamic-fixture/1.2.3
  * Bugfix in string truncation to max_length

==Version 1.2.2==

  * 2011/05/05 (yyyy/mm/dd)
  * http://pypi.python.org/pypi/django-dynamic-fixture/1.2.2
  * Improvements in exception messages

==Version 1.2.1==

  * 2011/03/11 (yyyy/mm/dd)
  * http://pypi.python.org/pypi/django-dynamic-fixture/1.2.1
  * Propagate ignored fields to self references
  * Refactoring + Bug fixes

==Version 1.2==
  * 2011/03/04 (yyyy/mm/dd)
  * http://pypi.python.org/pypi/django-dynamic-fixture/1.2
  * New Feature: ignore_fields
  * New Feature: now it is possible to set the ID

==Version 1.1==
  * Bug fixes
  * http://pypi.python.org/pypi/django-dynamic-fixture/1.0 (1.0 has the 1.1 package)

==Version 1.0==
  * Initial version
  * Ready to use in big projects


= Testing = 
* python manage.py test
* python manage.py test --with-coverage --cover-inclusive --cover-html --cover-package=django_dynamic_fixture.* --with-queries


= TODO List =
* auto config of denormalizated fields
* with_queries documentation and bugfixes (always print 0 queries)
* related_name documentation or workaround
* today, yesterday, tomorrow on fdf
* bugfix in fdf or ddf: some files/directories are not deleted
* tests with files in ddf
* tests with proxy models
* doc factory: example to generate models with validators in fields or in clean methods
* tests with GenericRelations, GenericForeignKey etc
* more tests with OneToOneField(parent_link=True)
* documentation: examples of usage
