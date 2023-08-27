from distutils.version import StrictVersion
import django
DJANGO_VERSION = django.get_version()[0:3]

DEBUG = True

IMPORT_DDF_MODELS = True

SECRET_KEY = 'ddf-secret-key'

ALLOWED_HOSTS = ['*'] # Since Django 1.11, it is verified when running tests


INSTALLED_APPS = ()

INSTALLED_APPS += (
    'queries',
    'django_dynamic_fixture',
    'django.contrib.contenttypes',
)
try:
    import polymorphic
    INSTALLED_APPS += ('polymorphic',)
except ImportError:
    pass


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
