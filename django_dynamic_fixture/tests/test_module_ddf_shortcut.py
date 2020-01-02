# -*- coding: utf-8 -*-

try:
    from ddf import N, G, F, C, P, PRE_SAVE, POST_SAVE
    from ddf import new, get, fixture, teach, look_up_alias
    from ddf import skip_for_database, only_for_database
    from ddf import FileSystemDjangoTestCase
except ImportError:
    assert False, 'Import `ddf` module is not working properly.'
