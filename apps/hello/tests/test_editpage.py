from base64 import b64encode
import json
import StringIO

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django import forms
from django.test import TestCase

from django.utils.image import Image

from apps.hello.forms import EditProfileForm, PhotoInput
from apps.hello.models import Profile


class EditPersonPageTests(TestCase):
    def setUp(self):
        self.client.login(username='admin', password='admin')
        self.response = self.client.get('/edit/')

    def test_editpage_accepts_POST_JSON(self):
        """View should accept JSON POST request"""
        response = self.client.post('/edit/',
                                    json.dumps({'some': 'data'}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_editpage_declines_POST_form_data(self):
        """View should decline POST request with
        multipart/form-data content type"""

        response = self.client.post('/edit/', {'some': 'data'})
        self.assertEqual(response.status_code, 400)

    def test_editpage_correct_template(self):
        """Is view uses correct template?"""
        self.assertTemplateUsed(self.response, 'editpage.html')

    def test_editpage_context_correct(self):
        """Is view provides correct context?"""
        self.assertEqual(User.objects.get(pk=1),
                         self.response.context["person"])
        self.assertIsInstance(self.response.context["editform"],
                              EditProfileForm)

    def test_editform_has_correct_initial_data(self):
        """Checking if view provides correct initial data to the form"""
        person = Profile.objects.get(pk=1)
        self.assertDictEqual(self.response.context["editform"].initial,
                             person.to_dict())


class EditPagePhotoTests(TestCase):
    def setUp(self):
        self.client.login(username='admin', password='admin')

    def create_imagefile(self):
        """Creates a PNG image with StringIO"""
        img = Image.new("RGBA", size=(200, 200), color=(255, 0, 0, 0))
        file_object = StringIO.StringIO()
        img.save(file_object, 'png')
        file_object.seek(0)
        return file_object

    def jsonify_model(self, model_data, extra_data):
        """Receives model as dict, dict with some extra data
        that should be in returned JSON and return JSONed dict"""
        for k, v in extra_data.iteritems():
            model_data[k] = v(model_data) if callable(v) else v
        return json.dumps(model_data)

    def test_editpage_handles_B64_photo(self):
        """View should handle JSON Base64 photo"""

        imagefile = self.create_imagefile()

        person_json = self.jsonify_model(
            Profile.objects.get(pk=1).to_dict(),
            {
                "photo": "data:image/png;base64,"+b64encode(imagefile.read()),
                "birth_date": lambda m: m['birth_date'].strftime('%Y-%m-%d')
            }
        )
        response = self.client.post('/edit/',
                                    person_json,
                                    content_type='application/json')
        self.assertEqual(200, response.status_code)
        updated_person = Profile.objects.get(pk=1)

        # Checking if photos are equal
        with open(updated_person.photo.path, 'r') as model_photo:
            imagefile.seek(0)
            if imagefile.read() != model_photo.read():
                self.fail("Photos are not equal")

    def test_editpage_uses_old_photo_if_none_sent(self):
        """View should handle JSON with empty photo field"""
        old_photo = Profile.objects.get(pk=1).photo

        person_json = self.jsonify_model(
            Profile.objects.get(pk=1).to_dict(),
            {
                "photo": "",
                "birth_date": lambda m:
                m['birth_date'].strftime('%Y-%m-%d')
            }
        )
        response = self.client.post('/edit/',
                                    person_json,
                                    content_type='application/json')
        self.assertEqual(200, response.status_code)
        new_photo = Profile.objects.get(pk=1).photo

        self.assertEqual(old_photo, new_photo)


class EditPageAuthTests(TestCase):
    def test_admin_can_access(self):
        """Admin can asks for edit page"""
        self.client.login(username='admin', password='admin')
        response = self.client.get("/edit/")
        self.assertEqual(200, response.status_code)

    def test_user_hasnt_access(self):
        """User cannot access edit page"""
        User.objects.create_user('temporary',
                                 'temporary@example.com',
                                 'temporary')
        self.client.login(username='temporary', password='temporary')
        response = self.client.get("/edit/")
        self.assertEqual(403, response.status_code)
        self.assertEqual("Only admin can access this page.", response.content)


class EditPersonFormTests(TestCase):
    # 'field': ('value', 'error_type')
    FORM_DATA = {
        'first_name': ("", "required"),
        'last_name': ("", "required"),
        'birth_date': ("not a date", "invalid_date"),
        'bio': ("", "required"),
        'email': ("not an email", "invalid_email"),
        'jabber': ("", "required"),
        'skype': ("", "required"),
        'contacts': ("", "required"),
        'photo': ("not an image", "invalid_image"),
    }

    ERROR_MESSAGES = {
        "required": "This field is required.",
        "invalid_date": "Enter a valid date.",
        "invalid_email": "Enter a valid email address.",
        "invalid_image": "No file was submitted. "
                         "Check the encoding type on the form.",
    }

    CORRECT_WIDGETS = {
        "bio": forms.Textarea,
        "contacts": forms.Textarea,
        "photo": PhotoInput
    }

    def test_form_has_correct_widgets(self):
        """Checking form if it provides correct widget in some fields"""
        form = EditProfileForm()
        for field, widget in self.CORRECT_WIDGETS.iteritems():
            self.assertIsInstance(form.fields[field].widget, widget)

    def test_form_checks_data_for_correctness(self):
        """Testing form with correct data"""
        person = Profile.objects.get(pk=1)
        form = EditProfileForm(data=person.to_dict(),
                               files={'photo': person.photo})
        self.assertTrue(form.is_valid())

    def test_form_checks_data_incorrectness(self):
        """Testing form with invalid data"""

        self.client.login(username='admin', password='admin')
        data = json.dumps({k: v[0] for k, v in self.FORM_DATA.iteritems()})
        response = self.client.post(reverse("editpage"),
                                    data=data,
                                    content_type='application/json')

        for k, v in self.FORM_DATA.iteritems():
            self.assertFormError(response, "editform",
                                 k, self.ERROR_MESSAGES[v[1]])
