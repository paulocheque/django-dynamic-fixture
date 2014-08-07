
IMPORT_DDF_MODELS = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

SECRET_KEY = 'ddf-secret-key'

INSTALLED_APPS = (
    'queries',
    'django_coverage',
    'django_nose',
    'django_dynamic_fixture',
    'django.contrib.contenttypes',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_PLUGINS = ['queries.Queries', 'ddf_setup.DDFSetup']

# Tell nose to measure coverage on the 'foo' and 'bar' apps
NOSE_ARGS = [
    # '--with-coverage',
    '--cover-html',
    '--cover-package=django_dynamic_fixture',
    '--cover-tests',
    '--cover-erase',
    ]

# EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
# EMAIL_FILE_PATH = '/tmp/invest-messages'  # change this to a proper location
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# python manage.py test --with-coverage --cover-inclusive --cover-html --cover-package=django_dynamic_fixture.* --with-queries --with-ddf-setup
