from django import forms

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, Submit, Button, Fieldset, HTML

from .models import FacebookGroup

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

class FBGroupCreateForm(forms.ModelForm):

	class Meta:
		model = FacebookGroup
		fields = ["name", "description", "privacy", "cover", "thumbnail", "active"]



	def __init__(self, *args, **kwargs):
		super(FBGroupCreateForm, self).__init__(*args, **kwargs)
		self.fields["privacy"].choices = (('open', 'Open'), ('closed', 'Closed'))
		self.fields["active"].help_text = u'Uncheck to hide group from public'

		self.helper = FormHelper()
		self.helper.form_tag = True
		self.helper.form_class = 'form form-horizontal'
		self.helper.attrs = {"enctype": "multipart/form-data"}
		self.helper.label_class = "col-md-2"
		self.helper.field_class = "col-md-10"
		self.helper.form_action = '.'
		self.helper.layout = Layout(
			'name',
			'description',
			'privacy',
			'cover',
			'thumbnail',
			'active',
			FormActions(
				Submit('submit', 'Submit')
				)
			)