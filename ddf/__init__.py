# Short alias to use: # `from ddf import *` instead of `from django_dynamic_fixture import *`
from django_dynamic_fixture import N, G, F, C, P, PRE_SAVE, POST_SAVE
from django_dynamic_fixture import new, get, fixture, teach, look_up_alias
from django_dynamic_fixture.decorators import skip_for_database, only_for_database
from django_dynamic_fixture.fdf import FileSystemDjangoTestCase
