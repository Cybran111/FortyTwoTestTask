from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from apps.hello.models import Request


class EditLinkTagTests(TestCase):
    fixtures = ["requests.json"]

    def test_tag_returns_user_admin_link(self):
        """editlink should return correct link for edit user in admin panel"""
        user = User.objects.get(id=1)
        actual_url = editlink(user)
        expected_url = reverse("admin:user_change", args=[user.id])
        self.assertEqual(actual_url, expected_url)

    def test_tag_returns_request_admin_link(self):
        """editlink should return correct link for edit request in admin panel"""
        req = Request.objects.get(id=1)
        actual_url = editlink(req)
        expected_url = reverse("admin:request_change", args=[req.id])
        self.assertEqual(actual_url, expected_url)

    def test_tag_throws_error_for_wrong_object(self):
        """editlink should throws an error if object is wrong (not a model)"""
        wrong_obj = User  # No matters what it is
        self.assertRaises(BadModelException, editlink, wrong_obj)
