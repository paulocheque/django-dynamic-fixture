from settings_ddf import *

DDF_TEST_GEODJANGO = False

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

if DDF_TEST_GEODJANGO:
    INSTALLED_APPS += ('django.contrib.gis',)
