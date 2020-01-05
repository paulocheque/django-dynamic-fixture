.. about:

About
*******************************************************************************

.. contents::
   :local:


Collaborators
===============================================================================

* Paulo Cheque <https://paulocheque.codeart.io> <https://github.com/paulocheque> - Master Dissertation about Automated Test Patterns: https://teses.usp.br/teses/disponiveis/45/45134/tde-02042012-120707/pt-br.php
* Valder Gallo <http://valdergallo.com.br> <https://github.com/valdergallo>
* Julio Netto <http://www.inerciasensorial.com.br> <https://bitbucket.org/inerte>


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

External references
===============================================================================

  * http://stackoverflow.com/search?q=django+dynamic+fixture
  * http://stackoverflow.com/questions/12487337/optimizing-setup-and-teardown-for-sample-django-model-using-django-nose-and-djan
  * http://stackoverflow.com/questions/4400609/initial-data-fixture-management-in-django


Running tests locally
===============================================================================

Install GDAL: https://docs.djangoproject.com/en/1.11/ref/contrib/gis/install/geolibs/#gdal

Commands::

    make build
    make tox
