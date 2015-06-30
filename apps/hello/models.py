from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
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

    def update_user(self, data):
        self.user.first_name = data['first_name']
        self.user.last_name = data['last_name']
        self.bio = data['bio']
        self.user.email = data['email']
        self.jabber = data['jabber']
        self.skype = data['skype']
        self.contacts = data['contacts']

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
    priority = models.IntegerField(default=3,
                                   validators=[
                                       MaxValueValidator(5),
                                       MinValueValidator(1)
                                   ])

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Request, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-priority', '-created_at']

    def __unicode__(self):
        return u"<id: %d, priority: %d," \
               u" date: %s>" % (self.id, self.priority, self.created_at)


class DbAction(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    action = models.TextField()
    model_object = models.TextField()
