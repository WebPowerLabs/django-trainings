# -*- coding: utf-8 -*-
from django import forms
from localflavor.us.forms import USStateField, USZipCodeField, USPhoneNumberField
from allauth.account.forms import SignupForm
from .models import User


class UserForm(forms.ModelForm):

    class Meta:
        # Set this form to use the User model.
        model = User

        # Constrain the UserForm to just these fields.
        fields = ("first_name", "last_name", "street1", "street2", "city", "state", "postal_code", "country")


class UserSignupForm(SignupForm):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    phone = USPhoneNumberField()
    street1 = forms.CharField(label=u'Street Address 1')
    street2 = forms.CharField(label=u'Street Address 2', required=False)
    city = forms.CharField()
    state = USStateField()
    postal_code = USZipCodeField()
    country = forms.CharField()

