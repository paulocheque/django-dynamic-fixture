# -*- coding: utf-8 -*-
from django.test import TestCase

from django_dynamic_fixture import G, N, teach, DDFLibrary
from django_dynamic_fixture.models_test import ModelForDDFSetup


class ModuleDDFSetUpTest(TestCase):
    def setUp(self):
        DDFLibrary.instance = DDFLibrary() # singleton object is cleared by another tests
        teach(ModelForDDFSetup, integer=9999) # using EXCLUSIVE_DDF_LIBRARY

    def tearDown(self):
        DDFLibrary.instance = DDFLibrary()

    def test_setup_module_load_before_any_test_of_this_module(self):
        instance = G(ModelForDDFSetup)
        assert instance.integer == 9999


class ApplicationDDFSetupTest(TestCase):
    def setUp(self):
        DDFLibrary.instance = DDFLibrary()
        teach(ModelForDDFSetup, integer=1000, ddf_lesson='test1')
        teach(ModelForDDFSetup, integer=1001)
        teach(ModelForDDFSetup, integer=1002, ddf_lesson='test2')

    def tearDown(self):
        DDFLibrary.instance = DDFLibrary()

    def test_ddf_setup_will_load_initial_lessons(self):
        instance = G(ModelForDDFSetup)
        assert instance.integer == 1001
        instance = G(ModelForDDFSetup, ddf_lesson='test1')
        assert instance.integer == 1000
        instance = G(ModelForDDFSetup, ddf_lesson='test2')
        assert instance.integer == 1002
