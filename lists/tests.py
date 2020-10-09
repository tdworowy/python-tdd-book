from django.test import TestCase


class HomePageTest(TestCase):

    def test_home_page_returns_html(self):
        response = self.client.get('/') # use Django test client
        self.assertTemplateUsed(response, 'home.html')
