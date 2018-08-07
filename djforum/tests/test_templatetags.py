from django import forms
from django.test import TestCase

from ..templatetags.form_tags import field_type, input_class


class ExampleForm(forms.Form):
	name = forms.CharField()
	password = forms.CharField(widget = forms.PasswordInput())

	class Meta:
		fields = ('name', 'password')

class FieldTypeTest(TestCase):

	 def test_field_widget_type(self):
	 	form = ExampleForm()
	 	self.assertEquals('TextInput', field_type(form['name']))
	 	self.assertEquals('PasswordInput', field_type(form['password']))

class InputClassTests(TestCase):

	def test_unbound_field_initial_state(self):
		form = ExampleForm()
		self.assertEquals('form-control', input_class(form['name']))

	def test_valid_bound_field(self):
		form = ExampleForm({'name': 'john', 'password': '123'}) # bound form (form + data)
