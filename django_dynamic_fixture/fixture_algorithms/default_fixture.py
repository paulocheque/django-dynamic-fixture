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
    # Django >= 1.6
    def binaryfield_config(self, field, key):
        return six.b('\x00\x46\xFE')

    # Django >= 1.8
    def uuidfield_config(self, field, key):
        return uuid.uuid4()