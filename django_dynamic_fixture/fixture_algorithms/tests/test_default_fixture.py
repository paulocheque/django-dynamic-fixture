# -*- coding: utf-8 -*-
from datetime import datetime
import six
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
from django_dynamic_fixture.fixture_algorithms.default_fixture import BaseDataFixture


class BaseDataFixtureTestCase(TestCase):
    def setUp(self):
        self.fixture = BaseDataFixture()

    def test_uuid(self):
        if django_greater_than('1.8'):
            self.assertTrue(isinstance(self.fixture.generate_data(models.UUIDField()), uuid.UUID))


if django_greater_than('1.7') and (hasattr(settings, 'DDF_TEST_GEODJANGO') and settings.DDF_TEST_GEODJANGO):
    from django_dynamic_fixture.fixture_algorithms.default_fixture import GeoDjangoFixtureMixin

    # Mixing for tests
    class GeoDjangoFixtureMixin(BaseDataFixture, GeoDjangoFixtureMixin):
        pass

    class GeoDjangoDataFixtureTestCase(TestCase):
        def setUp(self):
            self.fixture = GeoDjangoFixtureMixin()

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


if django_greater_than('1.8'):
    try:
        import psycopg2
        from django.contrib.postgres.fields import ArrayField
        from django_dynamic_fixture.fixture_algorithms.default_fixture import PostgresFixtureMixin
        from django_dynamic_fixture.fixture_algorithms.sequential_fixture import SequentialDataFixture, StaticSequentialDataFixture
        from django_dynamic_fixture.fixture_algorithms.random_fixture import RandomDataFixture
        from django_dynamic_fixture.fixture_algorithms.unique_random_fixture import UniqueRandomDataFixture

        class PostgresDataFixtureTestMixin(object):
            def test_arrayfield_integer_config(self):
                data = self.fixture.generate_data(ArrayField(models.IntegerField()))
                self.assertTrue(isinstance(data, list))
                self.assertTrue(isinstance(data[0], int))

            def test_arrayfield_char_config(self):
                data = self.fixture.generate_data(ArrayField(models.CharField()))
                self.assertTrue(isinstance(data, list))
                self.assertTrue(isinstance(data[0], six.text_type))

            def test_arrayfield_datetime_config(self):
                data = self.fixture.generate_data(ArrayField(models.DateTimeField()))
                self.assertTrue(isinstance(data, list))
                self.assertTrue(isinstance(data[0], datetime))

            def test_arrayfield_email_config(self):
                data = self.fixture.generate_data(ArrayField(models.EmailField(max_length=100)))
                self.assertTrue(isinstance(data, list))
                self.assertTrue(isinstance(data[0], six.text_type))


        class PostgresSequentialDataFixtureTestCase(TestCase, PostgresDataFixtureTestMixin):
            def setUp(self):
                class CustomFixture(SequentialDataFixture, PostgresFixtureMixin):
                    pass
                self.fixture = CustomFixture()

        class PostgresStaticSequentialDataFixtureTestCase(TestCase, PostgresDataFixtureTestMixin):
            def setUp(self):
                class CustomFixture(StaticSequentialDataFixture, PostgresFixtureMixin):
                    pass
                self.fixture = CustomFixture()

        class PostgresRandomDataFixtureTestCase(TestCase, PostgresDataFixtureTestMixin):
            def setUp(self):
                class CustomFixture(RandomDataFixture, PostgresFixtureMixin):
                    pass
                self.fixture = CustomFixture()

        class PostgresUniqueRandomDataFixtureTestCase(TestCase, PostgresDataFixtureTestMixin):
            def setUp(self):
                class CustomFixture(UniqueRandomDataFixture, PostgresFixtureMixin):
                    pass
                self.fixture = CustomFixture()

    except ImportError:
        print('Skipping Postgres tests because psycopg2 has not been installed.')
