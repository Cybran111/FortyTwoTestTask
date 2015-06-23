from datetime import datetime
from django.contrib.auth.models import User
from django.test import TestCase
from apps.hello.models import Profile


class HomePageTests(TestCase):
    def setUp(self):
        self.response = self.client.get('/')

    def test_homepage_exists(self):
        """Is homepage accessable?"""
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_correct_template(self):
        """Is view uses correct template?"""
        self.assertTemplateUsed(self.response, 'index.html')

    def test_homepage_context_correct(self):
        """Is view provides correct context?"""
        self.assertEqual(User.objects.get(pk=1),
                         self.response.context["person"])

    def test_homepage_should_return_only_admin_info(self):
        """If we have another registered user (superuser) in DB,
        we should see only the first admin"""
        second_admin = User.objects.create_superuser("ad", "min", "superuser")
        Profile.objects.create(
            user=second_admin,
            birth_date=datetime.now(),
            bio="bio",
            contacts="contacts",
            jabber="jabber",
            skype="skype"
        )

        self.assertEqual(User.objects.get(username="admin"),
                         self.response.context["person"])


class EditPersonPageTests(TestCase):
    def setUp(self):
        self.response = self.client.get('/edit/')

    def test_editpage_exists(self):
        """Is edit page accessable?"""
        self.assertEqual(self.response.status_code, 200)

    def test_editpage_correct_template(self):
        """Is view uses correct template?"""
        self.assertTemplateUsed(self.response, 'editpage.html')

    def test_editpage_context_correct(self):
        """Is view provides correct context?"""
        self.assertEqual(EditProfileForm(),
                         self.response.context["editform"])


class AuthPagesTests(TestCase):
    def test_loginpage_exists(self):
        """Is login page accessable?"""
        response = self.client.get("/accounts/login/")
        self.assertEqual(response.status_code, 200)

    def test_loginpage_uses_correct_template(self):
        """Is login page accessable?"""
        response = self.client.get("/accounts/login/")
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_logoutpage_exists(self):
        """Is logout page accessable?"""
        response = self.client.get("/accounts/logout/")
        self.assertEqual(response.status_code, 200)
