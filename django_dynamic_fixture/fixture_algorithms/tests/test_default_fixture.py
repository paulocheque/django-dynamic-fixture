# -*- coding: utf-8 -*-
import uuid

from django.db import models
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


try:
    from django.contrib.gis.geos import *
except ImportError:
    pass  # Django < 1.7
try:
    from django.contrib.gis.db import models as geomodels
except ImportError:
    pass  # Django < 1.7
except ImproperlyConfigured:
    pass  # enviroment without geo libs


from django.test import TestCase

from django_dynamic_fixture.django_helper import django_greater_than
from django_dynamic_fixture.fixture_algorithms.default_fixture import BaseDataFixture, GeoDjangoDataFixture


# Mixing for tests
class GeoDjangoDataFixture(BaseDataFixture, GeoDjangoDataFixture):
    pass


class BaseDataFixtureTestCase(TestCase):
    def setUp(self):
        self.fixture = BaseDataFixture()

    def test_uuid(self):
        if django_greater_than('1.8'):
            self.assertTrue(isinstance(self.fixture.generate_data(models.UUIDField()), uuid.UUID))


if django_greater_than('1.7') and settings.DDF_TEST_GEODJANGO:
    class GeoDjangoDataFixtureTestCase(TestCase):
        def setUp(self):
            self.fixture = GeoDjangoDataFixture()

        def test_geometryfield_config(self):
            self.assertTrue(isinstance(self.fixture.generate_data(geomodels.GeometryField()), GEOSGeometry))

        def test_pointfield_config(self):
            self.assertTrue(isinstance(self.fixture.generate_data(geomodels.PointField()), Point))

        def test_linestringfield_config(self):
            self.assertTrue(isinstance(self.fixture.generate_data(geomodels.LineStringField()), LineString))

        def test_polygonfield_config(self):
            self.assertTrue(isinstance(self.fixture.generate_data(geomodels.PolygonField()), Polygon))

        def test_multipointfield_config(self):
            self.assertTrue(isinstance(self.fixture.generate_data(geomodels.MultiPointField()), MultiPoint))

        def test_multilinesstringfield_config(self):
            self.assertTrue(isinstance(self.fixture.generate_data(geomodels.MultiLineStringField()), MultiLineString))

        def test_multipolygonfield_config(self):
            self.assertTrue(isinstance(self.fixture.generate_data(geomodels.MultiPolygonField()), MultiPolygon))

        def test_geometrycollectionfield_config(self):
            self.assertTrue(isinstance(self.fixture.generate_data(geomodels.GeometryCollectionField()), GeometryCollection))
