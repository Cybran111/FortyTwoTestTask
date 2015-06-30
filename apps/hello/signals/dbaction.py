from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from apps.hello.models import DbAction


@receiver(post_save)
def db_save_callback(sender, instance, created, **kwargs):
    if sender == DbAction:  # We don't wanna fall into recursion, huh?
        return

    action = "create" if created else "update"
    DbAction.objects.create(action=action, model_object=str(instance))


@receiver(post_delete)
def db_delete_callback(sender, instance, **kwargs):
    DbAction.objects.create(action="delete", model_object=str(instance))
