import django_filters
from lessons.models import Lesson
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms


class LessonForm(forms.Form):
    class Meta:
        model = Lesson

    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.form_method = 'get'
    helper.add_input(Submit('', 'Filter', css_class="btn-success"))


class LessonFilter(django_filters.FilterSet):
    course__name = django_filters.CharFilter(lookup_type='icontains')

    class Meta:
        form = LessonForm
        model = Lesson
        fields = ['course__name', 'tags']

