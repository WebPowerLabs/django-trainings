from django_comments.forms import CommentForm
from dtf_comments.models import DTFComment
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class DTFCommentForm(CommentForm):

    def get_comment_model(self):
        return DTFComment

    def get_comment_create_data(self):
        data = super(DTFCommentForm, self).get_comment_create_data()
        return data


class DTFCommentShareForm(forms.ModelForm):

    class Meta:
        model = DTFComment
        fields = ['comment']

    helper = FormHelper()
    helper.add_input(Submit('save_changes', 'Save changes',
                            css_class="btn-success"))
