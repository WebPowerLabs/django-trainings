from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML


def validate_honeypot(value):
    if value:
        print value
        print 'there was a value'
        raise ValidationError(u'Im sorry Mr. or Ms. Bot')


class ContactForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'input-lg', 'placeholder': 'Email'}))
    subject = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'class': 'input-lg', 'placeholder': 'Subject'}))
    feedback = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Your Message...'}), required=False)
    next = forms.HiddenInput()
    honeypot = forms.CharField(max_length=100, validators=[validate_honeypot], 
                               required=False)

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
            'honeypot',
            HTML('<input type="hidden" name="next" value="{{ request.path }}">'),
            HTML('<div class="btn btn-lg btn-block btn-success submit" type="submit" id="submit"><i class="icon-paper-plane-2"></i></div>')
        )


class EmailForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    subject = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    feedback = forms.HiddenInput()
    next = forms.HiddenInput()
    honeypot = forms.CharField(max_length=100, validators=[validate_honeypot], 
                               required=False)

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
            'honeypot',
            HTML('<input type="hidden" name="next" value="{{ request.path }}">'),
             Div(
                Submit('submit', 'Submit!', css_class='btn-lg btn-block btn-success')
            )
        )
