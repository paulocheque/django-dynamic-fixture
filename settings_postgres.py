from settings_ddf import *

DDF_TEST_GEODJANGO = True

# Postgres and PostGis
# > psql -d ddf -c "CREATE EXTENSION postgis;"
# > psql -d ddf -c "select postgis_lib_version();"
DATABASES = {
    'default': {
        # Postgis supports all Django features
        # createdb ddf
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'ddf',
        'USER': 'ddf_user', # please, change this if you want to run tests in your machine
        'PASSWORD': 'ddf_pass',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}

if DDF_TEST_GEODJANGO:
    INSTALLED_APPS += ('django.contrib.gis',)