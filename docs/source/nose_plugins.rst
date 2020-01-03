.. _nose_plugins:

Nose plugins
*******************************************************************************

DDF Setup Nose Plugin (New in 1.6.0)
===============================================================================

This plugin create a "setup suite". It will load the file *ddf_setup.py* in the root of your Django project before to execute the first test.
The file *ddf_setup.py* may contain default and custom lessons configurations or pythonic initial data. Django just load initial data from YAML, JSON, XML etc::

    python manage.py test --with-ddf-setup


Queries Nose Plugin (New in 1.4.0)
===============================================================================

This plugin print how many queries are executed by a test. It may be useful to determine performance issues of system features::

    python manage.py test --with-queries

The following command print how many queries are executed when a model is saved. It may be useful to determine performance issues in overriding *save* methods and in extensive use of listeners *pre_save* and *post_save*::

    python manage.py count_queries_on_save

