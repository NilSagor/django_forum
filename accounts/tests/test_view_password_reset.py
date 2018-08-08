from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.core import mail
from django.urls import resolve, reverse
from django.test import TestCase


class PasswordResetTests(TestCase):
	def setUp(self):
		url = reverse('password_reset')
		self.response = self.client.get(url)

	def test_status_code(self):
		self.assertEquals(self.response.status_code, 200)

	def test_view_function(self):
		view = resolve('/reset/')
		self.assertEquals(view.func_class, auth_views.PasswrodResetView)

	def test_csrf(self):
		self.assertContains(self.response, 'csrfmiddlewaretoken')

	def test_contains_form(self):
		form = self.response.context.get('form')
		self.assertIsInstance(form, PasswordResetForm)

class SuccessfulPasswordResetTests(TestCase):
	def setUp(self):
		email = 'john@doe.com'
		User.objects.create_user(
			username = 'john',
			email = email,
			password = '123abcdef'
			)
		url = reverse('password_reset')
		self.response = self.client.post(url, {'email': email})

	def test_redirection(self):
		'''
		A valid form submission should reidrect the user to 'password_reset_done'
		'''
		url = reverse('password_reset_done')
		self.assertRedirects(self.response, url)

	def test_send_password_reset_email(self):
		self.assertEqual(1, len(mail.outbox))

class InvalidPasswordResetTests(TestCase):
	def setUp(self):
		url = reverse('password_reset')
		self.response = self.client.post(url, {'email': 'donotexists@email.com'})

	def test_redirections(self):
		'''
		Even invalid emails in the database should redirects the user t 'password_reset_done' view
		'''
		url = reverse('password_reset_done')
		self.assertRedirects(self.response, url)

	def test_no_reset_email_sent(self):
		self.assertEqual(0, len(mail.outbox))