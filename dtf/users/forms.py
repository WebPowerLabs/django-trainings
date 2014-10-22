# -*- coding: utf-8 -*-
from django import forms
from localflavor.us.forms import USStateField, USZipCodeField, USPhoneNumberField

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, Submit, Button, Fieldset, HTML

from affiliates.models import Affiliate

from .models import User


class UserForm(forms.ModelForm):

    class Meta:
        # Set this form to use the User model.
        model = User

        # Constrain the UserForm to just these fields.
        fields = ("phone", )


class UserSignupForm(forms.Form):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    phone = USPhoneNumberField()

    def __init__(self, *args, **kwargs):
        super(UserSignupForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form'
        self.helper.form_action = '.'
        self.helper.layout = Layout(
            'first_name',
            'last_name',
            'username',
            'email',
            'phone',
            'password1',
            'password2',
            FormActions(
                Submit('submit', 'Submit')
                )
            )

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone = self.cleaned_data['phone']
        user.save()


