# -*- coding: utf-8 -*-
from django import forms
from localflavor.us.forms import USStateField, USZipCodeField, USPhoneNumberField

from affiliates.models import Affiliate

from .models import User


class UserForm(forms.ModelForm):

    class Meta:
        # Set this form to use the User model.
        model = User

        # Constrain the UserForm to just these fields.
        fields = ("first_name", "last_name", "street1", "street2", "city", "state", "postal_code", "country")


class UserSignupForm(forms.Form):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    phone = USPhoneNumberField()
    street1 = forms.CharField(label=u'Street Address 1')
    street2 = forms.CharField(label=u'Street Address 2', required=False)
    city = forms.CharField()
    state = USStateField()
    postal_code = USZipCodeField()
    country = forms.CharField()
    referral_code = forms.CharField(required=False, widget=forms.HiddenInput)

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone = self.cleaned_data['phone']
        user.street1 = self.cleaned_data['street1']
        user.street2 = self.cleaned_data['street2']
        user.city = self.cleaned_data['city']
        user.state = self.cleaned_data['state']
        user.postal_code = self.cleaned_data['postal_code']
        user.country = self.cleaned_data['country']
        user.save()
        referral_code = self.cleaned_data['referral_code']
        if referral_code:
            Affiliate.objects.sign_up_affiliate_user_with_code(user, 
                                                               referral_code)
        else:
            Affiliate.objects.sign_up_affiliate_user_with_zip(user, 
                                                              user.postal_code)

