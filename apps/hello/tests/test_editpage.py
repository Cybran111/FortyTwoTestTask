from base64 import b64encode
import json
import StringIO
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django import forms
from django.test import TestCase
from django.utils.image import Image
from apps.hello.forms import EditProfileForm
from apps.hello.models import Profile


class EditPersonPageTests(TestCase):
    def setUp(self):
        self.client.login(username='admin', password='admin')
        self.response = self.client.get('/edit/')

    def test_editpage_accepts_POST_JSON(self):
        """View should accept JSON POST request"""
        response = self.client.post('/edit/',
                                    {'some': 'data'},
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_editpage_handle_B64_photo(self):
        """View should handle JSON Base64 photo"""

        # Create the file object with StringIO
        img = Image.new("RGBA", size=(200, 200), color=(255, 0, 0, 0))
        temp_handle = StringIO.StringIO()
        img.save(temp_handle, 'png')
        temp_handle.seek(0)

        # Creating correct JSON representation of the model
        person = Profile.objects.get(pk=1).to_dict()
        person['photo'] = b64encode(temp_handle.read())
        person['birth_date'] = person['birth_date'].strftime('%Y-%m-%d')
        person_json = json.dumps(person)

        self.client.post('/edit/', person_json,
                         content_type='application/json')
        updated_person = Profile.objects.get(pk=1)

        # Checking if photos are equal
        with open(updated_person.photo.path, 'r') as model_photo:
            temp_handle.seek(0)
            if temp_handle.read() != model_photo.read():
                self.fail("Photos are not equal")

    def test_editpage_declines_POST_form_data(self):
        """View should decline POST request with
        multipart/form-data content type"""

        response = self.client.post('/edit/',
                                    {'some': 'data'})
        self.assertEqual(response.status_code, 400)

    def test_editpage_correct_template(self):
        """Is view uses correct template?"""
        self.assertTemplateUsed(self.response, 'editpage.html')

    def test_editpage_context_correct(self):
        """Is view provides correct context?"""
        self.assertIsInstance(self.response.context["editform"],
                              EditProfileForm)

    def test_editform_has_correct_initial_data(self):
        """Checking if view provides correct initial data to the form"""
        person = Profile.objects.get(pk=1)
        self.assertDictEqual(
            self.response.context["editform"].initial,
            person.to_dict()
        )


class EditPageAuthTests(TestCase):
    def test_admin_can_access(self):
        """Admin can asks for edit page"""
        self.client.login(username='admin', password='admin')
        response = self.client.get("/edit/")
        self.assertEqual(200, response.status_code)

    def test_user_hasnt_access(self):
        """User cannot access edit page"""
        User.objects.create_user(
            'temporary',
            'temporary@example.com',
            'temporary'
        )
        self.client.login(username='temporary', password='temporary')
        response = self.client.get("/edit/")
        self.assertEqual(400, response.status_code)


class EditPersonFormTests(TestCase):

    CORRECT_WIDGETS = {
        "bio": forms.Textarea,
        "contacts": forms.Textarea
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

        form_data = {
            'first_name': "",  # blank
            'last_name': "",  # blank
            'birth_date': "not a date",
            'bio': "",  # blank
            'email': "not an email",
            'jabber': "",  # blank
            'skype': "",  # blank
            'contacts': "",  # blank
            'photo': "not an image",
        }

        self.client.login(username='admin', password='admin')
        response = self.client.post(reverse("editpage"),
                                    data=json.dumps(form_data),
                                    content_type='application/json')
        for key in form_data:
            self.assertFormError(response, "editform",
                                 key, "This field is required.")
