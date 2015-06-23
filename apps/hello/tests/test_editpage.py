import django
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.forms import forms
from django.test import TestCase
from apps.hello.forms import EditProfileForm


class EditPersonPageTests(TestCase):
    def setUp(self):
        self.response = self.client.get('/edit/')

    def test_editpage_exists(self):
        """Is edit page accessable?"""
        self.assertEqual(self.response.status_code, 200)

    def test_editpage_can_http_post(self):
        response = self.client.post('/edit/post/')
        self.assertEqual(response.status_code, 200)

    def test_editpage_correct_template(self):
        """Is view uses correct template?"""
        self.assertTemplateUsed(self.response, 'editpage.html')

    def test_editpage_context_correct(self):
        """Is view provides correct context?"""
        self.assertIsInstance(self.response.context["editform"],
                              EditProfileForm)

class EditPersonFormTests(TestCase):
    ERROR_MESSAGES = {
        "required": "This field is required.",
        "invalid_date": "Enter a valid date.",
        "invalid_email": "Enter a valid email address.",
        "invalid_image": "Invalid Image.",
    }

    def test_form_checks_data_for_correctness(self):
        user = User.objects.get(pk=1)
        form_data = {
            'firstname': user.firstname,
            'lastname': user.lastname,
            'birthdate': user.profile.birth_date,
            'bio': user.profile.bio,
            'email': user.email,
            'jabber': user.profile.jabber,
            'skype': user.profile.skype,
            'contacts': user.profile.contacts,
            'photo': user.profile.photo,
        }
        form = EditProfileForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_checks_data_for_incorrectness(self):
        form_data = {
            'firstname': "",  # blank
            'lastname': "",  # blank
            'birthdate': "not a date",
            'bio': "",  # blank
            'email': "not an email",
            'jabber': "",  # blank
            'skype': "",  # blank
            'contacts': "",  # blank
            'photo': "not an image",
        }
        response = self.client.post(reverse("editpage"), data=form_data)

        self.assertFormError(response, EditProfileForm, "firstname", self.ERROR_MESSAGES["required"])
        self.assertFormError(response, EditProfileForm, "lastname", self.ERROR_MESSAGES["required"])
        self.assertFormError(response, EditProfileForm, "birthdate", self.ERROR_MESSAGES["invalid_date"])
        self.assertFormError(response, EditProfileForm, "bio", self.ERROR_MESSAGES["required"])
        self.assertFormError(response, EditProfileForm, "email", self.ERROR_MESSAGES["invalid_email"])
        self.assertFormError(response, EditProfileForm, "jabber", self.ERROR_MESSAGES["required"])
        self.assertFormError(response, EditProfileForm, "skype", self.ERROR_MESSAGES["required"])
        self.assertFormError(response, EditProfileForm, "contacts", self.ERROR_MESSAGES["required"])
        self.assertFormError(response, EditProfileForm, "photo", self.ERROR_MESSAGES["invalid_image"])
