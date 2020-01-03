# PyTest file for global set up.

# Django initialisation
import django
django.setup()

# Django-Nose must import test_models to avoid 'no such table' problem
from django_dynamic_fixture import models_test

# Give DB access to PyTests
import pytest
pytest.mark.django_db

# MonkeyPatch Django-Test teardown
from django.test import utils
original_teardown_test_environment = utils.teardown_test_environment
def fixed_teardown_test_environment():
    try:
        original_teardown_test_environment()
    except TypeError:
        # Ignore some Django or PyTest-Django bug
        pass
utils.teardown_test_environment = fixed_teardown_test_environment

print(':: PyTest conftest.py loaded.')
