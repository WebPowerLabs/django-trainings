from django import forms

from courses.models import Course
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class CourseCreateFrom(forms.ModelForm):
    class Meta:
        model = Course

    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.add_input(Submit('save_changes', 'Save changes',
                            css_class="btn-success"))
