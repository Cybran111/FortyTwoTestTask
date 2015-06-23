from django.test import TestCase


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
