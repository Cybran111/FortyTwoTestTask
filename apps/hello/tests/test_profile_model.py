from django.test import TestCase
from apps.hello.models import Profile


class ProfileModelTests(TestCase):
    def test_model_can_return_dict_repr(self):
        profile = Profile.objects.get(pk=1)
        profile_dict = {
            "first_name": profile.user.first_name,
            "last_name": profile.user.first_name,
            "birth_date": profile.birth_date,
            "photo": profile.photo,
            "email": profile.user.email,
            "jabber": profile.jabber,
            "skype": profile.skype,
            "contacts": profile.contacts,
            "bio": profile.bio,
        }
        self.assertDictEqual(profile.to_dict(), profile_dict)
