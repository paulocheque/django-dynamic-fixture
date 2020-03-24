# -*- coding: utf-8 -*-
from datetime import datetime, date, timedelta
from decimal import Decimal
import random
import string
import uuid

import six

from django.core.exceptions import ImproperlyConfigured


try:
    from django.utils.timezone import now
except ImportError:
    now = datetime.now

try:
    from django.contrib.gis.geos import *
except ImproperlyConfigured:
    pass  # environment without geo libs
except Exception:
    pass # Avoid errors like GDALException


from django_dynamic_fixture.ddf import DataFixture


class BaseDataFixture(DataFixture):
    # Django >= 1.6
    def binaryfield_config(self, field, key):
        return six.b('\x00\x46\xFE')

    # Django >= 1.8
    def uuidfield_config(self, field, key):
        return uuid.uuid4()

    # Django >= 1.4
    def genericipaddressfield_config(self, field, key):
        return self.ipaddressfield_config(field, key)

    # POSTGRES
    def  jsonfield_config(self, field, key):
        return {}


# GIS/GeoDjango
class GeoDjangoFixtureMixin(object):
    def create_point(self, x=None, y=None):
        # latitude: [-90,90], longitude: [-180,180]
        latitude = x or random.randint(-90, 90)
        longitude = y or random.randint(-180, 180)
        return Point(longitude, latitude)

    def create_points(self, n=3, closed=True):
        points = [self.create_point() for i in range(n)]
        if closed: # LinearRing
            points.append(points[0])
        return points

    def geometryfield_config(self, field, key):
        return GEOSGeometry('POINT(%s %s)' % self.create_point().coords)

    def pointfield_config(self, field, key):
        return self.create_point()

    def linestringfield_config(self, field, key, n=3):
        return LineString(self.create_points(n))

    def polygonfield_config(self, field, key, n=3):
        return Polygon(self.create_points(n))

    def multipointfield_config(self, field, key, n=3):
        return MultiPoint(self.create_points(n))

    def multilinestringfield_config(self, field, key, n=3):
        lines = [self.linestringfield_config(field, key, n) for i in range(n)]
        return MultiLineString(lines)

    def multipolygonfield_config(self, field, key, n=3):
        polygons = [self.polygonfield_config(field, key, n) for i in range(n)]
        return MultiPolygon(polygons)

    def geometrycollectionfield_config(self, field, key, n=3):
        polygons = [self.polygonfield_config(field, key, n) for i in range(n)]
        return GeometryCollection(polygons)


# Postgres fields
# https://docs.djangoproject.com/en/1.8/ref/contrib/postgres/fields/
class PostgresFixtureMixin(object):
    def arrayfield_config(self, field, key, n=1):
        data = [self.generate_data(field.base_field) for i in range(n)]
        return data
