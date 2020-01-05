# -*- coding: utf-8 -*-
from django.test import TestCase
import pytest

from django_dynamic_fixture.models_test import *
from django_dynamic_fixture.ddf import *
from django_dynamic_fixture import G

try:
    from polymorphic.models import PolymorphicModel

    class PolymorphicModelTest(TestCase):
        def test_create_polymorphic_model_and_retrieve(self):
            p = G(ModelPolymorphic)
            assert list(ModelPolymorphic.objects.all()) == [p]

        def test_create_polymorphic_model_2_and_retrieve(self):
            p = G(ModelPolymorphic2)
            assert list(ModelPolymorphic2.objects.all()) == [p]

        def test_cannot_save(self):
            with self.assertRaises(BadDataError):
                G(ModelPolymorphic3)
except ImportError:
    pass
