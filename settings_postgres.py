import os
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
        'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
        'PORT': os.getenv('POSTGRES_PORT', 5432),
        'NAME': os.getenv('POSTGRES_DB', 'ddf'),
        'USER': os.getenv('POSTGRES_USER', 'ddf_user'), # please, change this if you want to run tests in your machine
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'ddf_pass'),
    }
}

if DDF_TEST_GEODJANGO:
    INSTALLED_APPS += ('django.contrib.gis',)
