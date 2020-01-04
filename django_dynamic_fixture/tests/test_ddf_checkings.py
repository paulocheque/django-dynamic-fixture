# -*- coding: utf-8 -*-

from django.test import TestCase

from django_dynamic_fixture.ddf import DDFLibrary
from django_dynamic_fixture import ddf_check_models, teach


class DDFTestCase(TestCase):
    def setUp(self):
        DDFLibrary.get_instance().clear()


class TestCheckCompatibility(DDFTestCase):
    def test_default(self):
        succeeded, errors = ddf_check_models()

        compatible_models = [
            'django_dynamic_fixture.EmptyModel',
            'django_dynamic_fixture.ModelWithNumbers',
        ]
        for model in compatible_models:
            assert model in succeeded.keys(), model

        incompatible_models = [
            'django_dynamic_fixture.ModelWithUnsupportedField',
        ]
        for model in incompatible_models:
            assert model in errors.keys(), model
        # TODO: Consider the RelatedObjectDoesNotExist errors
        # https://stackoverflow.com/questions/26270042/how-do-you-catch-this-exception

    def test_teaching_ddf(self):
        teach('django_dynamic_fixture.ModelWithUnsupportedField', z='z')
        succeeded, errors = ddf_check_models()

        compatible_models = [
            'django_dynamic_fixture.ModelWithUnsupportedField',
        ]
        for model in compatible_models:
            assert model in succeeded.keys(), model
            assert model not in errors.keys(), model
