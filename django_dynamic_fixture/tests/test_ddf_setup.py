# -*- coding: utf-8 -*-
from unittest import TestCase

from django_dynamic_fixture import G, DDFLibrary
from django_dynamic_fixture.models_test import ModelForDDFSetup
from django_dynamic_fixture.tests.ddf_setup import DDF_LIBRARY_FOR_TESTS


EXCLUSIVE_DDF_LIBRARY = DDFLibrary()


def setUpModule():
    DDFLibrary.instance = EXCLUSIVE_DDF_LIBRARY
    G(ModelForDDFSetup, integer=9999, shelve=True) # using EXCLUSIVE_DDF_LIBRARY
    # isolating setup module test
    DDFLibrary.instance = DDFLibrary() # hacking singleton: start a new DDFLibrary


class ModuleDDFSetUpTest(TestCase):
    def setUp(self):
        DDFLibrary.instance = EXCLUSIVE_DDF_LIBRARY # singleton object is cleared by another tests

    def tearDown(self):
        DDFLibrary.instance = DDFLibrary()

    def test_setup_module_load_before_any_test_of_this_module(self):
        instance = G(ModelForDDFSetup, use_library=True)
        self.assertEquals(9999, instance.integer)


class ApplicationDDFSetupTest(TestCase):
    def setUp(self):
        DDFLibrary.instance = DDF_LIBRARY_FOR_TESTS

    def tearDown(self):
        DDFLibrary.instance = DDFLibrary()

    def test_ddf_setup_will_load_initial_shelves(self):
        instance = G(ModelForDDFSetup, use_library=True)
        self.assertEquals(1001, instance.integer)
        instance = G(ModelForDDFSetup, named_shelve='test1', use_library=True)
        self.assertEquals(1000, instance.integer)
        instance = G(ModelForDDFSetup, named_shelve='test2', use_library=True)
        self.assertEquals(1002, instance.integer)
