from django import forms

from .models import UserProfile, UserPrivateProfile


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ["archetype", "anthem", "about"]


class UserPrivateProfileForm(forms.ModelForm):

    class Meta:
        model = UserPrivateProfile
        fields = ["dream",]