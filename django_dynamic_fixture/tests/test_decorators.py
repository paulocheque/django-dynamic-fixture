# -*- coding: utf-8 -*-
from unittest import TestCase

from django.conf import settings

from django_dynamic_fixture import decorators


class SkipForDatabaseTest(TestCase):
    def setUp(self):
        self.it_was_executed = False

    def tearDown(self):
        # It is important to do not break others tests: global and shared variable
        decorators.DATABASE_ENGINE = settings.DATABASES['default']['ENGINE']

    @decorators.only_for_database(decorators.POSTGRES)
    def method_postgres(self):
        self.it_was_executed = True

    def test_annotated_method_only_for_postgres(self):
        decorators.DATABASE_ENGINE = decorators.SQLITE3
        self.method_postgres()
        assert self.it_was_executed == False

        decorators.DATABASE_ENGINE = decorators.POSTGRES
        self.method_postgres()
        assert self.it_was_executed


class OnlyForDatabaseTest(TestCase):
    def setUp(self):
        self.it_was_executed = False

    def tearDown(self):
        # It is important to do not break others tests: global and shared variable
        decorators.DATABASE_ENGINE = settings.DATABASES['default']['ENGINE']

    @decorators.skip_for_database(decorators.SQLITE3)
    def method_sqlite3(self):
        self.it_was_executed = True

    def test_annotated_method_skip_for_sqlite3(self):
        decorators.DATABASE_ENGINE = decorators.SQLITE3
        self.method_sqlite3()
        assert self.it_was_executed == False

        decorators.DATABASE_ENGINE = decorators.POSTGRES
        self.method_sqlite3()
        assert self.it_was_executed
