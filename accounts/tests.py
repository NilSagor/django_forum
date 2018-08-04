from django.test import TestCase
from django.urls import reverse, resolve
from .views import signup
# Create your tests here.

def test_signup_status_code(self):
	url = reverse('signup')
	response = self.client.get()


def test_signup_url_resolve_signup_view(self):
	view = resovle('/signup/')
	sefl.assertEquals(view.func, signup)
