from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django import forms
from django.test import TestCase
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
    ERROR_MESSAGES = {
        "required": "This field is required.",
        "invalid_date": "Enter a valid date.",
        "invalid_email": "Enter a valid email address.",
    }
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
        def assert_editform(field, error):
            self.assertFormError(response, "editform", field, error)

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
        response = self.client.post(reverse("editpage"), data=form_data)

        assert_editform("first_name", self.ERROR_MESSAGES["required"])
        assert_editform("last_name", self.ERROR_MESSAGES["required"])
        assert_editform("birth_date", self.ERROR_MESSAGES["invalid_date"])
        assert_editform("bio", self.ERROR_MESSAGES["required"])
        assert_editform("email", self.ERROR_MESSAGES["invalid_email"])
        assert_editform("jabber", self.ERROR_MESSAGES["required"])
        assert_editform("skype", self.ERROR_MESSAGES["required"])
        assert_editform("contacts", self.ERROR_MESSAGES["required"])
        assert_editform("photo", self.ERROR_MESSAGES["required"])
