from django.test import TestCase
from django.urls import reverse, resolve

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


from .views import signup
# Create your tests here.

def setUp(self):
	url = reverse('signup')
	self.response = self.client.get(url)


def test_signup_status_code(self):
	self.assertEquals(self.response.status_code, 200)


def test_signup_url_resolve_signup_view(self):
	view = resovle('/signup/')
	sefl.assertEquals(view.func, signup)

def test_csrf(self):
	self.assertEquals(self.response, 'csrfmiddlewaretoken')

def test_contains_form(self):
	form = self.reponse.context.get('form')
	self.assertIsInstance(form, UserCreationForm)

class SuccessfulSignUpTests(TestCase):

	def setUp(self):
		url = reverse('signup')
		data = {
			'username' : 'john',
			'password1': 'abcdef123456',
			'password2': 'abcdef123456'
		}
		self.response = self.client.post(url, data)
		self.home_url = reverse('home')

	def test_redirection(self):
		'''
		A valid form submission should redirect the user to the homepage
		'''
		self.assertRedirects(self.response, self.home_url)

	def test_user_creation(self):
		self.assertTrue(User.objects.exists())

	def test_user_authentication(self):
		'''
		create a new request to an arbitrary page.
		the resulting response should now have a 'user' to its context, after a successful signup.
		'''
		response = self.client.get(self.home_url)
		user = response.context.get('user')
		self.assertTrue(user.is_authenticated)


class InvalidSignUpTests(TestCase):
	def setUp(self):
		url = reverse('signup')
		self.response = self.client.post(url, {})

	def test_signup_status_code(self):
		'''
		An invlaid form submission should return to the same page
		'''
		self.assertEquals(self.response.status_code, 200)

	def test_form_errors(self):
		form = self.response.context.get('form')
		self.assertTrue(form.errors)

	def test_dont_create_user(self):
		self.assertFalse(User.objects.exists())
