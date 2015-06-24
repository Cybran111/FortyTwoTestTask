import StringIO
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from PIL import Image
from apps.hello.models import Profile


class ProfileModelTests(TestCase):

    def setUp(self):
        self.person = Profile.objects.get(pk=1)

    def test_model_scales_every_photo(self):
        img = Image.new("RGBA", size=(500,500), color=(255, 0, 0, 0))
        temp_handle = StringIO.StringIO()
        img.save(temp_handle, 'png')
        temp_handle.seek(0)
        self.person.photo.save("somefile.png", ContentFile(temp_handle.read()))
        self.assertTupleEqual((200,200), (self.person.photo.height, self.person.photo.width))

    def test_model_can_return_dict_repr(self):
        """Profile model should have to_dict()
        for representing the model"""
        profile = Profile.objects.get(pk=1)
        profile_dict = {
            "first_name": profile.user.first_name,
            "last_name": profile.user.last_name,
            "birth_date": profile.birth_date,
            "photo": profile.photo,
            "email": profile.user.email,
            "jabber": profile.jabber,
            "skype": profile.skype,
            "contacts": profile.contacts,
            "bio": profile.bio,
        }
        self.assertDictEqual(profile.to_dict(), profile_dict)
