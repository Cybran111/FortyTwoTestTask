from StringIO import StringIO
from django.core.management import call_command
from django.test import TestCase
from django.db import models
import sys


class CommandGetModelsTests(TestCase):
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
        out, sys.stdout = sys.stdout, StringIO()
        call_command('getmodels')

        sys.stdout.seek(0)

        actual_result = unicode(sys.stdout.read())
        sys.stdout = out

        self.assertEqual(expected_result, actual_result)

    def test_getmodels_dublicates_stdout_to_stderr(self):
        """Command should dublicate stdout to stderr
        Command should prepend 'error: ' to stderr output
        """
        out, sys.stdout = sys.stdout, StringIO()
        err, sys.stderr = sys.stderr, StringIO()

        call_command('getmodels')

        sys.stdout.seek(0)
        sys.stderr.seek(0)

        for stdout_line, stdrerr_line in zip(sys.stdout.readlines(),
                                             sys.stderr.readlines()):
            self.assertEqual("error: %s" % stdout_line, stdrerr_line)

        sys.stdout = out
        sys.stderr = err
