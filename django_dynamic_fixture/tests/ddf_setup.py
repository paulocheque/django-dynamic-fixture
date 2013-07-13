from django_dynamic_fixture import N, DDFLibrary
from django_dynamic_fixture.models_test import ModelForDDFSetup


DDF_LIBRARY_FOR_TESTS = DDFLibrary()
DDFLibrary.instance = DDF_LIBRARY_FOR_TESTS
N(ModelForDDFSetup, integer=1000, shelve='test1')
N(ModelForDDFSetup, integer=1001, shelve=True)
N(ModelForDDFSetup, integer=1002, shelve='test2')

# isolating ddf setup test
DDFLibrary.instance = DDFLibrary() # hacking singleton: start a new DDFLibrary
