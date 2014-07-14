from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from resources.models import Resource


class ResourceCreateFrom(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['name', 'description', 'published', 'thumbnail', 'type',
                  'file']

    helper = FormHelper()
    helper.add_input(Submit('save_changes', 'Save changes',
                            css_class="btn-success"))
