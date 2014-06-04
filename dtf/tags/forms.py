from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from tags.models import Tag


class TagCreateFrom(forms.ModelForm):
    class Meta:
        model = Tag

    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.add_input(Submit('save_changes', 'Save changes',
                            css_class="btn-success"))