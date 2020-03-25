# -*- coding: utf-8 -*-
from datetime import datetime
import six
import uuid

from django.db import models
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


from django.contrib.gis.geos import *
try:
    from django.contrib.gis.db import models as geomodels
except ImproperlyConfigured:
    pass  # environment without geo libs


from django.test import TestCase

from django_dynamic_fixture.fixture_algorithms.default_fixture import BaseDataFixture


class BaseDataFixtureTestCase(TestCase):
    def setUp(self):
        self.fixture = BaseDataFixture()

    def test_uuid(self):
        assert isinstance(self.fixture.generate_data(models.UUIDField()), uuid.UUID)


if (hasattr(settings, 'DDF_TEST_GEODJANGO') and settings.DDF_TEST_GEODJANGO):
    from django_dynamic_fixture.fixture_algorithms.default_fixture import GeoDjangoFixtureMixin

    # Mixing for tests
    class GeoDjangoFixtureMixin(BaseDataFixture, GeoDjangoFixtureMixin):
        pass

    class GeoDjangoDataFixtureTestCase(TestCase):
        def setUp(self):
            self.fixture = GeoDjangoFixtureMixin()

        def test_geometryfield_config(self):
            assert isinstance(self.fixture.generate_data(geomodels.GeometryField()), GEOSGeometry)

        def test_pointfield_config(self):
            assert isinstance(self.fixture.generate_data(geomodels.PointField()), Point)

        def test_linestringfield_config(self):
            assert isinstance(self.fixture.generate_data(geomodels.LineStringField()), LineString)

        def test_polygonfield_config(self):
            assert isinstance(self.fixture.generate_data(geomodels.PolygonField()), Polygon)

        def test_multipointfield_config(self):
            assert isinstance(self.fixture.generate_data(geomodels.MultiPointField()), MultiPoint)

        def test_multilinesstringfield_config(self):
            assert isinstance(self.fixture.generate_data(geomodels.MultiLineStringField()), MultiLineString)

        def test_multipolygonfield_config(self):
            assert isinstance(self.fixture.generate_data(geomodels.MultiPolygonField()), MultiPolygon)

        def test_geometrycollectionfield_config(self):
            assert isinstance(self.fixture.generate_data(geomodels.GeometryCollectionField()), GeometryCollection)
