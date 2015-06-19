from django.contrib.auth.models import User
from django.core import serializers
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
            list(Request.objects.all()[:10]),
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


class RequestsListTest(TestCase):
    def setUp(self):
        self.LAST_ITEM_DELTA = 4  # No matters how far from the end
        self.not_last_item = Request.objects.count() - self.LAST_ITEM_DELTA

    def test_view_returns_right_value_without_providing_last_item_id(self):
        """If we do not providing id of last item, view should return last 10 items"""
        response = self.client.get('/requests/list/', HTTP_X_REQUESTED_WITH='XMLHttpRequest')  # AJAX request
        requests = serializers.serialize('json', list(Request.objects.all()[:10]))

        self.assertEqual(requests, response.body)

    def test_view_returns_right_value_with_providing_last_item_id(self):
        """If we providing id of last item, view should return JSON accordingly to this value"""
        response = self.client.get('/requests/list/',
                                   {"last": self.not_last_item},
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        requests = serializers.serialize('json', list(Request.objects.all()[:self.LAST_ITEM_DELTA]))
        self.assertEqual(requests, response.body)

    def test_view_process_last_item_correctly(self):
        """In case when there are no new requests, view should return empty JSON"""
        response = self.client.get('/requests/list/',
                               {"last": Request.objects.count()},
                               HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        requests = serializers.serialize('json', list())
        self.assertEqual(requests, response.body)
