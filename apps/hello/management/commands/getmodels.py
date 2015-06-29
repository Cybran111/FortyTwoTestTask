from django.core.management import BaseCommand
from django.db import models


class Command(BaseCommand):

    def handle(self, *args, **options):
        for model in models.get_models(include_auto_created=True):
            model_info = '%s-%s - %d' % (model._meta.app_label.lower(),
                                         model._meta.object_name.lower(),
                                         model.objects.count())

            self.stdout.write(model_info)
            self.stderr.write(model_info)
