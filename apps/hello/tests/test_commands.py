import json
from django.core import serializers
from django.core.management import call_command
from django.test import TestCase
from django.db import models

class CommandGetModelsTests(TestCase):
    def test_getmodels_returns_all_models_data(self):
        """getmodels should return JSON with all models and objects count in them"""
        model_list = models.get_models(include_auto_created=True)
        expected_result = json.dumps({
            u"%s-%s" % (model._meta.app_label.lower(), model._meta.object_name.lower()): model.objects.count()
            for model in model_list
            })
        actual_result = call_command('getmodels')

        self.assertEqual(expected_result, actual_result)

    def test_getmodels_dublicates_stdout_to_stderr(self):
        pass
