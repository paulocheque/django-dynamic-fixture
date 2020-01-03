# PyTest file for global set up.

# Django initialisation
import django
django.setup()

# Django-Nose must import test_models to avoid 'no such table' problem
from django_dynamic_fixture import models_test

# Give DB access to PyTests
import pytest
pytest.mark.django_db

print(':: PyTest conftest.py loaded.')
