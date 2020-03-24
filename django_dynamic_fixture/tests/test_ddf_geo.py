# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

try:
    from django.contrib.gis.geos import *
except ImproperlyConfigured:
    pass  # environment without geo libs

try:
    from django.contrib.gis.db import models as geomodel
except ImproperlyConfigured:
    pass  # environment without geo libs

from django.test import TestCase
import pytest

from django_dynamic_fixture.models_test import *
from django_dynamic_fixture.ddf import *
from django_dynamic_fixture.fixture_algorithms.sequential_fixture import SequentialDataFixture


data_fixture = SequentialDataFixture()


class DDFTestCase(TestCase):
    def setUp(self):
        self.ddf = DynamicFixture(data_fixture)


if (hasattr(settings, 'DDF_TEST_GEODJANGO') and settings.DDF_TEST_GEODJANGO):
    class GeoDjangoFieldsTest(DDFTestCase):
        def test_geodjango_fields(self):
            instance = self.ddf.new(ModelForGeoDjango)
            assert isinstance(instance.geometry, GEOSGeometry), str(type(instance.geometry))
            assert isinstance(instance.point, Point)
            assert isinstance(instance.line_string, LineString)
            assert isinstance(instance.polygon, Polygon)
            assert isinstance(instance.multi_point, MultiPoint)
            assert isinstance(instance.multi_line_string, MultiLineString)
            assert isinstance(instance.multi_polygon, MultiPolygon)
            assert isinstance(instance.geometry_collection, GeometryCollection)
