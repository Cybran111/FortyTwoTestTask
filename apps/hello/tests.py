from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from apps.hello.models import Request


class HomePageTests(TestCase):
    def test_homepage_exists(self):
        """Is homepage accessable?"""
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


class RequestsPageTests(TestCase):
    def test_page_exists(self):
        """Is Requests page accessable?"""
        response = self.client.get('/requests/')
        self.assertEqual(response.status_code, 200)

    def test_homepage_correct_template(self):
        """Is view uses correct template?"""
        response = self.client.get('/requests/')
        self.assertTemplateUsed(response, 'requests.html')

    def test_homepage_context_correct(self):
        """Is view provides correct context?"""

        # making dumb requests
        self.client.get('/requests/')
        self.client.get('/requests/')
        self.client.get('/')
        self.client.get('/dumb')
        self.client.get('/')

        # Actually testing
        response = self.client.get('/requests/')

        self.assertListEqual(
            list(Request.objects.all()[1:11]),  # last request not in response
            list(response.context["requests"])
        )


class RequestMiddlewareTest(TestCase):
    def test_middleware_catches_good_get(self):
        """Is middleware saves good GET request?"""
        self.client.get('/')  # homepage
        self.assertEqual(1, Request.objects.count())

    def test_middleware_catches_bad_get(self):
        """Is middleware saves bad GET request?"""
        self.client.get('/somedumblink/')
        self.assertEqual(1, Request.objects.count())

    def test_middleware_catches_good_post(self):
        """Is middleware saves good POST request?"""
        self.client.post('/')  # homepage
        self.assertEqual(1, Request.objects.count())

    def test_middleware_catches_bad_post(self):
        """Is middleware saves bad POST request?"""
        self.client.post('/somedumblink/')
        self.assertEqual(1, Request.objects.count())
