from django.conf import settings

import_models = getattr(settings, 'IMPORT_DDF_MODELS', False)

if settings.IMPORT_DDF_MODELS:
    from django_dynamic_fixture.test_models import *
