# -*- coding: utf-8 -*-

from optparse import make_option

from django.core.management.base import AppCommand
from queries.count_queries_on_save import CountQueriesOnSave


class Command(AppCommand):
    help = """
    Default Usage:
    manage.py count_queries_on_save
    manage.py count_queries_on_save --settings=my_settings

    = Specifying apps:
    manage.py count_queries_on_save [APP_NAMES]+
    Usage:
    manage.py count_queries_on_save app1 app2
    manage.py count_queries_on_save app1 app2
    
    = Skipping apps:
    manage.py count_queries_on_save --skip=[APP_NAME,]+
    Usage:
    manage.py count_queries_on_save --skip=app1
    manage.py count_queries_on_save --skip=app1,app2
    manage.py count_queries_on_save app1 app2 --skip=app2
    """
    args = '<app_name app_name ...> --skip=APP1,APP2'
    option_list = AppCommand.option_list + (
        make_option('--skip', '-s', dest='skip-apps', default='',
                    help='Skip applications. Separate application labels by commas.'),
    )

    def handle(self, *args, **options):
        script = CountQueriesOnSave()
        app_labels = args
        exclude_app_labels = options['skip-apps'].split(',')
        report = script.execute(app_labels, exclude_app_labels)
        report.export_csv(order_by_quantity_queries=True)
