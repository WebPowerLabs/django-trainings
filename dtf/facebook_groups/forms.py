from django import forms

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, Submit, Button, Fieldset, HTML

class FBGroupFeedForm(forms.Form):
	message = forms.CharField()

	def __init__(self, *args, **kwargs):
		super(FBGroupFeedForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_tag = True
		self.helper.form_class = 'form'
		self.helper.form_action = '.'
		self.helper.layout = Layout(
			'message',
			FormActions(
				Submit('submit', 'Submit')
				)
			)

class FBGroupCreateForm(forms.Form):
	name = forms.CharField()
	description = forms.CharField()
	privacy = forms.ChoiceField(choices=(('open', 'Open'), ('closed', 'Closed')))
	#admin = forms.CharField()

	def __init__(self, *args, **kwargs):
		super(FBGroupCreateForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_tag = True
		self.helper.form_class = 'form'
		self.helper.form_action = '.'
		self.helper.layout = Layout(
			'name',
			'description',
			'privacy',
			FormActions(
				Submit('submit', 'Submit')
				)
			)