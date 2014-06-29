from django import forms
from django.utils.translation import ugettext_lazy as _

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, Submit, Button, Fieldset, HTML
from crispy_forms.bootstrap import InlineField, StrictButton

class ContactForm(forms.Form):
	email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'input-lg', 'placeholder': 'Email'}))
	subject = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'class': 'input-lg', 'placeholder': 'Subject'}))
	feedback = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Your Message...'}))
	next = forms.HiddenInput()

	def __init__(self, *args, **kwargs):
		super(ContactForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_tag = True
		self.helper.form_class = 'contact-form'
		self.helper.form_show_labels = False
		self.helper.form_action = 'contact'
		self.helper.form_id = 'contact-form'
		self.helper.layout = Layout(
            'email',
            'subject',
            'feedback',
            HTML('<input type="hidden" name="next" value="{{ request.path }}">'),
            HTML('<div class="btn btn-lg btn-block btn-success submit" type="submit" id="submit"><i class="icon-paper-plane-2"></i></div>')
        )


class EmailForm(forms.Form):
	email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
	subject = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'placeholder': 'Name'}))
	feedback = forms.HiddenInput()
	next = forms.HiddenInput()

	def __init__(self, *args, **kwargs):
		super(EmailForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_tag = True
		self.helper.form_class = 'contact-form'
		self.helper.form_show_labels = False
		self.helper.form_action = 'contact'
		self.helper.form_id = 'email-form'
		self.helper.layout = Layout(
            'subject',
            'email',
            'feedback',
            HTML('<input type="hidden" name="next" value="{{ request.path }}">'),
         	Div(
            	Submit('submit', 'Submit!', css_class='btn-lg btn-block btn-success')
            )
        )