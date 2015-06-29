import datetime
import StringIO
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.test import TestCase
from django.utils.image import Image
from apps.hello.models import DbAction, Profile


class DbActionSignalTests(TestCase):
    def setUp(self):
        self.dbaction_count = DbAction.objects.count()

    def test_signal_catches_create(self):
        """db_action signal should catch creation of any model entry"""

        # some foreign model such as auth.user
        user = User.objects.create_user("dumb", "user@example.com", "user")
        self.assertEqual(self.dbaction_count + 1, DbAction.objects.count())

        img = Image.new("RGBA", size=(200, 200), color=(255, 0, 0, 0))
        temp_handle = StringIO.StringIO()
        img.save(temp_handle, 'png')
        temp_handle.seek(0)

        # some local model
        Profile.objects.create(user=user, birth_date=datetime.date.today(),
                               bio="bio", contacts="contacts",
                               jabber="jab", skype="sky",
                               photo=ContentFile(temp_handle.read()))
        self.assertEqual(self.dbaction_count + 2, DbAction.objects.count())

    def test_signal_catches_update(self):
        """db_action signal should catch updating of any model entry"""

        # some foreign model such as auth.user
        user = User.objects.get(id=1)
        user.first_name = "Somebody"
        user.save()
        self.assertEqual(self.dbaction_count+1, DbAction.objects.count())

        # some local model
        profile = Profile.objects.get(id=1)
        profile.bio = "Such a biography"
        profile.save()
        self.assertEqual(self.dbaction_count+2, DbAction.objects.count())

    def test_signal_catches_delete(self):
        """db_action signal should catch deletion of any model entry"""

        # some local model
        profile = Profile.objects.get(id=1)
        profile.delete()
        self.assertEqual(self.dbaction_count+1, DbAction.objects.count())

        # some foreign model such as auth.user
        user = User.objects.get(id=1)
        user.delete()
        self.assertEqual(self.dbaction_count+2, DbAction.objects.count())
