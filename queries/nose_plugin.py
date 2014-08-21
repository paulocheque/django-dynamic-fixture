# -*- coding: utf-8 -*-

from nose.plugins import Plugin


# http://readthedocs.org/docs/nose/en/latest/plugins/interface.html
class Queries(Plugin):
    "python manage.py test --with-queries"
    name = 'queries'
    _queries_by_test_methods = []

    def configure(self, options, conf):
        """
        Called after the command line has been parsed, with the parsed options and the config container. 
        Here, implement any config storage or changes to state or operation that are set by command line options.
        DO NOT return a value from this method unless you want to stop all other plugins from being configured.
        """
        super(Queries, self).configure(options, conf)
        if self.enabled:
            from django.db import connection
            connection.use_debug_cursor = True

    def beforeTest(self, test):
        "Called before the test is run (before startTest)."
        from django.db import connection
        self.initial_amount_of_queries = len(connection.queries)

    def afterTest(self, test):
        "Called after the test has been run and the result recorded (after stopTest)."
        from django.db import connection
        self.final_amount_of_queries = len(connection.queries)
        self._queries_by_test_methods.append((test, self.final_amount_of_queries - self.initial_amount_of_queries))

    def report(self, stream):
        """Called after all error output has been printed. Print your
        plugin's report to the provided stream. Return None to allow
        other plugins to print reports, any other value to stop them.

        :param stream: stream object; send your output here
        :type stream: file-like object
        """
        stream.write('\nREPORT OF AMOUNT OF QUERIES BY TEST:\n')
        for x in self._queries_by_test_methods:
            testcase = x[0]
            queries = x[1]
            stream.write('\n%s: %s' % (testcase, queries))
        stream.write('\n')
