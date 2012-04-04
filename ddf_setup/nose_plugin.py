# -*- coding: utf-8 -*-

from nose.plugins import Plugin


# http://readthedocs.org/docs/nose/en/latest/plugins/interface.html
class DDFSetup(Plugin):
    "python manage.py test --with-ddf-setup"
    name = 'ddf-setup'
    enabled = True

    _error_message = None

    def begin(self):
        "Called before any tests are collected or run. Use this to perform any setup needed before testing begins."
        try:
            import ddf_setup
        except ImportError as e:
            self._error_message = str(e)

    def report(self, stream):
        """Called after all error output has been printed. Print your
        plugin's report to the provided stream. Return None to allow
        other plugins to print reports, any other value to stop them.

        :param stream: stream object; send your output here
        :type stream: file-like object
        """
        if self._error_message:
            stream.write('\nDDF Setup error: %s\n' % self._error_message)
