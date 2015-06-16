from django.test import TestCase

# Create your tests here.


class SomeTests(TestCase):
    def test_homepage_exists(self):
        """Is homepage accessable?"""

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
