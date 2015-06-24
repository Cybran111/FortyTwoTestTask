from django.core import serializers
from django.test import TestCase
from apps.hello import settings as hello_settings
from apps.hello.models import Request


LAST_ITEM_ID = 6


class RequestsPageTests(TestCase):
    fixtures = ['requests.json']

    def setUp(self):
        self.response = self.client.get('/requests/')

    def test_requests_page_exists(self):
        """Is Requests page accessable?"""
        self.assertEqual(self.response.status_code, 200)

    def test_requests_page_correct_template(self):
        """Is view uses correct template?"""
        self.assertTemplateUsed(self.response, 'requests.html')

    def test_requests_page_context_correct(self):
        """Is view provides correct context?
        Requests page shouldn't contains requests
        that are in REQUESTS_IGNORE_FILTERS from hello/settings.py"""
        self.assertListEqual(
            list(Request.objects.order_by("created_at")
                 .exclude(path__in=hello_settings.REQUESTS_IGNORE_FILTERS)
                 [:hello_settings.MAX_REQUESTS]),
            list(self.response.context["requests"])
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


    def test_middleware_doesnt_catches_banned_requests(self):
        """Middleware shouldn't catch requests
        that are in REQUESTS_IGNORE_FILTERS from hello/settings.py"""
        for banned_link in hello_settings.REQUESTS_IGNORE_FILTERS:
            self.client.get(banned_link)
        self.assertEqual(0, Request.objects.count())


class RequestsListTest(TestCase):
    fixtures = ['requests.json']

    def test_view_correct_list_without_providing_last_item_id(self):
        """If we do not providing id of last item,
        view should return HTTP 400 Bad Request"""
        response = self.client.get('/requests/list/')
        self.assertEqual(400, response.status_code)

    def test_view_correct_list_with_providing_last_item_id(self):
        """If we providing id of last item,
        view should return JSON accordingly to this value.
        Also, view shouldn't return requests
        that are in REQUESTS_IGNORE_FILTERS from hello/settings.py"""

        response = self.client.get(
            '/requests/list/',
            {"last_id": LAST_ITEM_ID}
        )

        requests = serializers.serialize(
            'json',
            list(Request.objects.order_by("created_at")
                 .exclude(path__in=hello_settings.REQUESTS_IGNORE_FILTERS)
                 [LAST_ITEM_ID:])
        )
        self.assertEqual(requests, response.content)
