# Short alias to use: # `from ddf import *` instead of `from django_dynamic_fixture import *`
from django_dynamic_fixture import *
from django_dynamic_fixture.decorators import skip_for_database, only_for_database
from django_dynamic_fixture.fdf import FileSystemDjangoTestCase
