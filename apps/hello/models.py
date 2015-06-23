from django.contrib.auth import get_user_model
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(get_user_model())
    birth_date = models.DateField()
    bio = models.TextField()
    contacts = models.TextField()
    jabber = models.TextField()
    skype = models.TextField()
    photo = models.ImageField(upload_to="pictures/",
                              default="pictures/notfound.jpg")


class Request(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    method = models.TextField()
    path = models.TextField()

    class Meta:
        ordering = ['created_at']
