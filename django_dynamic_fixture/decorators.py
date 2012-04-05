# -*- coding: utf-8 -*-

from django.conf import settings


DATABASE_ENGINE = settings.DATABASES['default']['ENGINE']

SQLITE3 = 'sqlite3'
POSTGRES = 'postgresql'
MYSQL = 'mysql'
ORACLE = 'oracle'
SQLSERVER = 'pyodbc'


def skip_for_database(database):
    def main_decorator(testcase_function):
        def wrapper(*args, **kwargs):
            if database not in DATABASE_ENGINE:
                testcase_function(*args, **kwargs)
        return wrapper
    return main_decorator


def only_for_database(database):
    def main_decorator(testcase_function):
        def wrapper(*args, **kwargs):
            if database in DATABASE_ENGINE:
                testcase_function(*args, **kwargs)
        return wrapper
    return main_decorator
