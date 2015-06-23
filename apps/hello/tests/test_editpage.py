from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from apps.hello.forms import EditProfileForm


class EditPersonPageTests(TestCase):
    def setUp(self):
        self.response = self.client.get('/edit/')

    def test_editpage_exists(self):
        """Is edit page accessable?"""
        self.assertEqual(self.response.status_code, 200)

    def test_editpage_can_http_post(self):
        """Is view serves POST request?"""
        response = self.client.post('/edit/')
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
    }

    def test_form_checks_data_for_correctness(self):
        """Testing form with correct data"""
        user = User.objects.get(pk=1)
        form_data = {
            'firstname': user.first_name,
            'lastname': user.last_name,
            'birthdate': user.profile.birth_date,
            'bio': user.profile.bio,
            'email': user.email,
            'jabber': user.profile.jabber,
            'skype': user.profile.skype,
            'contacts': user.profile.contacts,
        }
        form = EditProfileForm(data=form_data,
                               files={'photo': user.profile.photo})
        self.assertTrue(form.is_valid())

    def test_form_checks_data_incorrectness(self):
        """Testing form with invalid data"""
        def assertEditForm(field, error):
            self.assertFormError(response, "editform", field, error)

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

        assertEditForm("firstname", self.ERROR_MESSAGES["required"])
        assertEditForm("lastname", self.ERROR_MESSAGES["required"])
        assertEditForm("birthdate", self.ERROR_MESSAGES["invalid_date"])
        assertEditForm("bio", self.ERROR_MESSAGES["required"])
        assertEditForm("email", self.ERROR_MESSAGES["invalid_email"])
        assertEditForm("jabber", self.ERROR_MESSAGES["required"])
        assertEditForm("skype", self.ERROR_MESSAGES["required"])
        assertEditForm("contacts", self.ERROR_MESSAGES["required"])
        assertEditForm("photo", self.ERROR_MESSAGES["required"])
