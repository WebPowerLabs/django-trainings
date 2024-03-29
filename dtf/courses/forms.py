from django import forms

from courses.models import Course
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, HTML, Div

html_close_button = """
                    <button type="button" class="btn btn-danger" data-dismiss="modal"
                    data-toggle="collapse" data-parent="#accordion"
                    href="#collapseOne">Close</button>
                    """


class CourseCreateFrom(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description', 'published', 'thumbnail']

    helper = FormHelper()
    helper.layout = Layout('name', 'description', 'published', 'thumbnail',
                           Div(HTML(html_close_button),
                               Submit('save_changes', 'Save changes',
                                      css_class='btn-success'),
                               css_class='pull-right'))



