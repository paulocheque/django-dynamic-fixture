from distutils.version import StrictVersion
import django
DJANGO_VERSION = django.get_version()[0:3]

IMPORT_DDF_MODELS = True

DDF_TEST_GEODJANGO = False

# Postgres and PostGis
# DATABASES = {
#     'default': {
#         # Postgis supports all Django features
#         # createdb ddf
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'ddf',
#         'USER': 'paulocheque', # please, change this if you want to run tests in your machine
#         'PASSWORD': '',
#         'HOST': 'localhost',
#         'PORT': 5432,
#     }
# }
# if StrictVersion(DJANGO_VERSION) >= StrictVersion('1.7'):
#     # psql -d ddf -c "CREATE EXTENSION postgis;"
#     # psql -d ddf -c "select postgis_lib_version();"
#     DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'
#     DDF_TEST_GEODJANGO = True

# MySQL
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'ddf',
#         'USER': 'paulocheque', # please, change this if you want to run tests in your machine
#         'PASSWORD': '',
#         'HOST': 'localhost',
#         'PORT': 3306,
#     }
# }


# SQlite and SpatialLite
# brew install spatialite-tools
# brew install gdal
SPATIALITE_LIBRARY_PATH = '/usr/local/lib/mod_spatialite.dylib'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

SECRET_KEY = 'ddf-secret-key'


INSTALLED_APPS = ()

if DDF_TEST_GEODJANGO:
    INSTALLED_APPS += ('django.contrib.gis',)

INSTALLED_APPS += (
    'queries',
    'django_coverage',
    'django_nose',
    'django_dynamic_fixture',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_PLUGINS = ['queries.Queries', 'ddf_setup.DDFSetup']

# Tell nose to measure coverage on the 'foo' and 'bar' apps
NOSE_ARGS = [
    '--with-coverage',
    '--cover-html',
    '--cover-package=django_dynamic_fixture',
    '--cover-tests',
    '--cover-erase',
    ]

# EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
# EMAIL_FILE_PATH = '/tmp/invest-messages'  # change this to a proper location
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# python manage.py test --with-coverage --cover-inclusive --cover-html --cover-package=django_dynamic_fixture.* --with-queries --with-ddf-setup


# To avoid warnings
MIDDLEWARE_CLASSES = ()

# Example of DDF plugins for Custom fields
import json
DDF_FIELD_FIXTURES = {
    'django_dynamic_fixture.models_test.CustomDjangoField': {'ddf_fixture': lambda: 123456789},
    'django_dynamic_fixture.models_test.CustomDjangoField2': lambda: 987654321,

    # https://github.com/bradjasper/django-jsonfield
    'jsonfield.fields.JSONCharField': {'ddf_fixture': lambda: json.dumps({'some random value': 'c'})},
    'jsonfield.fields.JSONField': {'ddf_fixture': lambda: json.dumps([1, 2, 3])},
}
