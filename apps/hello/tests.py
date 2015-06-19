from datetime import datetime
from django.contrib.auth.models import User
from django.core import serializers
from django.test import TestCase

# Create your tests here.
from apps.hello.models import Request, Profile


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


class RequestsPageTests(TestCase):
    def setUp(self):
        self.response = self.client.get('/requests/')

    def test_page_exists(self):
        """Is Requests page accessable?"""
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_correct_template(self):
        """Is view uses correct template?"""
        self.assertTemplateUsed(self.response, 'requests.html')

    def test_homepage_context_correct(self):
        """Is view provides correct context?"""
        self.assertListEqual(
            list(Request.objects.all()[:10]),
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


class RequestsListTest(TestCase):
    fixtures = ['requests.json']

    def setUp(self):
        self.LAST_ITEM_DELTA = 4  # No matters how far from the end

    def test_view_correct_list_without_providing_last_item_id(self):
        """If we do not providing id of last item,
        view should return last 10 items"""
        response = self.client.get('/requests/list/')  # AJAX request
        requests = serializers.serialize(
            'json',
            list(Request.objects.all()[:10])
        )
        self.assertEqual(requests, response.content)

    def test_view_correct_list_with_providing_last_item_id(self):
        """If we providing id of last item,
        view should return JSON accordingly to this value"""
        # We should do +1 because of new request
        response = self.client.get(
            '/requests/list/',
            {"last_id": Request.objects.count() - self.LAST_ITEM_DELTA + 1})
        requests = serializers.serialize(
            'json',
            list(Request.objects.all()[:self.LAST_ITEM_DELTA])
        )
        self.assertEqual(requests, response.content)

    def test_view_process_last_item_correctly(self):
        """In case when there are no new requests,
        view should return only this request in list"""
        response = self.client.get('/requests/list/',
                                   {"last_id": Request.objects.count()})
        requests = serializers.serialize('json',
                                         list(Request.objects.all()[0:1]))
        self.assertEqual(requests, response.content)
