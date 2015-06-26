from django.contrib.auth import get_user_model
from django.db import models
from django_resized import ResizedImageField


class Profile(models.Model):
    user = models.OneToOneField(get_user_model())
    birth_date = models.DateField()
    bio = models.TextField()
    contacts = models.TextField()
    jabber = models.TextField()
    skype = models.TextField()
    photo = ResizedImageField(size=[200, 200],
                              upload_to="hello/photos",
                              default="pictures/notfound.png")

    def to_dict(self):
        return {
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "birth_date": self.birth_date,
            "photo": self.photo,
            "email": self.user.email,
            "jabber": self.jabber,
            "skype": self.skype,
            "contacts": self.contacts,
            "bio": self.bio,
        }


class Request(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    method = models.TextField()
    path = models.TextField()

    class Meta:
        ordering = ['created_at']
