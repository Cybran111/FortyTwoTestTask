from django.contrib.auth import get_user_model
from django.test import TestCase
User = get_user_model()


class ProfileModelTests(TestCase):
    def test_model_can_return_dict_repr(self):
        user = User.objects.get(pk=1)
        profile_dict = {
            "first_name": user.first_name,
            "last_name": user.first_name,
            "birth_date": user.profile.birth_date,
            "photo": user.profile.photo,
            "email": user.profile.email,
            "jabber": user.profile.jabber,
            "skype": user.profile.skype,
            "contacts": user.profile.contacts,
            "bio": user.profile.bio,
        }
        self.assertDictEqual(user.to_dict(), profile_dict)
