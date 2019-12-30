# -*- coding: utf-8 -*-
from django.test import TestCase

from django_dynamic_fixture import G, N, DDFLibrary
from django_dynamic_fixture.models_test import ModelForDDFSetup


class ModuleDDFSetUpTest(TestCase):
    def setUp(self):
        DDFLibrary.instance = DDFLibrary() # singleton object is cleared by another tests
        G(ModelForDDFSetup, integer=9999, shelve=True) # using EXCLUSIVE_DDF_LIBRARY

    def tearDown(self):
        DDFLibrary.instance = DDFLibrary()

    def test_setup_module_load_before_any_test_of_this_module(self):
        instance = G(ModelForDDFSetup, use_library=True)
        assert instance.integer == 9999


class ApplicationDDFSetupTest(TestCase):
    def setUp(self):
        DDFLibrary.instance = DDFLibrary()
        N(ModelForDDFSetup, integer=1000, shelve='test1')
        N(ModelForDDFSetup, integer=1001, shelve=True)
        N(ModelForDDFSetup, integer=1002, shelve='test2')

    def tearDown(self):
        DDFLibrary.instance = DDFLibrary()

    def test_ddf_setup_will_load_initial_shelves(self):
        instance = G(ModelForDDFSetup, use_library=True)
        assert instance.integer == 1001
        instance = G(ModelForDDFSetup, named_shelve='test1', use_library=True)
        assert instance.integer == 1000
        instance = G(ModelForDDFSetup, named_shelve='test2', use_library=True)
        assert instance.integer == 1002
