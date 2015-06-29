from StringIO import StringIO
from django.core.management import call_command
from django.test import TestCase
from django.db import models
import sys


class CommandGetModelsTests(TestCase):

    @staticmethod
    def seek_start():
        sys.stdout.seek(0)
        sys.stderr.seek(0)

    class SwapOutput(object):
        def __enter__(self):
            self.out, sys.stdout = sys.stdout, StringIO()
            self.err, sys.stderr = sys.stderr, StringIO()

        def __exit__(self, exc_type, exc_val, exc_tb):
            sys.stdout = self.out
            sys.stderr = self.err

    def test_getmodels_returns_all_models_data(self):
        """getmodels should return all models
        line by line and objects count in them"""

        model_list = models.get_models(include_auto_created=True)

        expected_list = ['%s-%s - %d' %
                         (
                             model._meta.app_label.lower(),
                             model._meta.object_name.lower(),
                             model.objects.count()
                         )
                         for model in model_list]

        expected_result = '\n'.join(expected_list)+'\n'

        with self.SwapOutput():
            call_command('getmodels')
            self.seek_start()
            actual_result = unicode(sys.stdout.read())

        self.assertEqual(expected_result, actual_result)

    def test_getmodels_dublicates_stdout_to_stderr(self):
        """Command should dublicate stdout to stderr
        Command should prepend 'error: ' to stderr output
        """
        with self.SwapOutput():
            call_command('getmodels')

            self.seek_start()

            for stdout_line, stdrerr_line in zip(sys.stdout.readlines(),
                                                 sys.stderr.readlines()):
                self.assertEqual("error: %s" % stdout_line, stdrerr_line)
