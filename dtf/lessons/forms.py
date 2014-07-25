from django import forms
from lessons.models import Lesson
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class LessonCreateFrom(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['name', 'description', 'published', 'thumbnail', 'audio',
                  'video', 'homework', 'tags']

    helper = FormHelper()
    helper.add_input(Submit('save_changes', 'Save changes',
                            css_class="btn-success"))
