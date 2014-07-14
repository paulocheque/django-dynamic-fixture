# -*- coding: utf-8 -*-

from django_dynamic_fixture import new

from django.conf import settings
from django.db import connection
from django import db
from django_dynamic_fixture.django_helper import get_models_of_an_app, is_model_managed, get_unique_model_name, get_apps


class Report(object):
    def __init__(self):
        self.data = []
        self.errors = []

    def add_record(self, app, model, queries_insert, queries_update):
        self.data.append((app, model, queries_insert, queries_update))

    def add_error(self, msg):
        self.errors.append(msg)

    def export_csv(self, order_by_quantity_queries=False):
        if order_by_quantity_queries:
            self.data.sort(key=lambda t: t[2], reverse=True)
        print('APP.MODEL;QUERIES ON INSERT;QUERIES ON UPDATE')
        for app, model, queries_insert, queries_update in self.data:
            print('%s;%s;%s' % (get_unique_model_name(model), queries_insert, queries_update))

        for err in self.errors:
            print(err)


class CountQueriesOnSave(object):
    def __init__(self):
        self.report = Report()

    def count_queries_for_model(self, app, model):
        try:
            model_instance = new(model, print_errors=False)
        except Exception as e:
            self.report.add_error('- Could not prepare %s: %s' % (get_unique_model_name(model), str(e)))
            return

        db.reset_queries()
        try:
            model_instance.save()
        except Exception as e:
            self.report.add_error('- Could not insert %s: %s' % (get_unique_model_name(model), str(e)))
            return
        queries_insert = len(connection.queries)

        db.reset_queries()
        try:
            model_instance.save()
        except Exception as e:
            self.report.add_error('- Could not update %s: %s' % (get_unique_model_name(model), str(e)))
            return
        queries_update = len(connection.queries)

        self.report.add_record(app, model, queries_insert, queries_update)

    def execute(self, app_labels=[], exclude_app_labels=[]):
        settings.DEBUG = True
        apps = get_apps(application_labels=app_labels, exclude_application_labels=exclude_app_labels)
        for app in apps:
            models = get_models_of_an_app(app)
            for model in models:
                if not is_model_managed(model):
                    continue
                self.count_queries_for_model(app, model)
        return self.report
