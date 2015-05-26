from datetime import datetime, date, timedelta
from decimal import Decimal
import random
import string
import uuid

import six
try:
    from django.utils.timezone import now
except ImportError:
    now = datetime.now

from django_dynamic_fixture.ddf import DataFixture


class BaseDataFixture(DataFixture):
    def uuidfield_config(self, field, key):
        return uuid.uuid4()
