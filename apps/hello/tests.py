from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.


class SomeTests(TestCase):
    def test_homepage_exists(self):
        """ Is homepage accessable? """

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_homepage_correct_template(self):
        """Is view uses correct template?"""
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'index.html')

    def test_homepage_context_correct(self):
        """Is view provides correct context?"""
        response = self.client.get('/')
        self.assertEqual(User.objects.get(pk=1), response.context["person"])
