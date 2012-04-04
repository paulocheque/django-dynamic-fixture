DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        #'NAME': 'ddf.sqlite' # for tests in shell
    }
}

INSTALLED_APPS = (
    'django_nose',
    'coverage',
    'queries',
    'django_dynamic_fixture',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_PLUGINS = ['queries.Queries', 'ddf_setup.DDFSetup']

# python manage.py test --with-coverage --cover-inclusive --cover-html --cover-package=django_dynamic_fixture.* --with-queries
