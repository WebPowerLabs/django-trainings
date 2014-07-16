from django.forms.models import ModelChoiceField
from django_comments.forms import CommentForm
from dtf_comments.models import DTFComment
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from facebook_groups.models import FacebookGroup


class DTFCommentForm(CommentForm):

    def get_comment_model(self):
        return DTFComment

    def get_comment_create_data(self):
        data = super(DTFCommentForm, self).get_comment_create_data()
        return data


class DTFCommentShareForm(forms.ModelForm):
    object_pk = ModelChoiceField(queryset='', label="Select facebook group:")

    class Meta:
        model = DTFComment
        fields = ['comment', 'object_pk']
        widgets = {
          'comment': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, user, *args, **kwargs):
        super(DTFCommentShareForm, self).__init__(*args, **kwargs)
        qs = FacebookGroup.objects.purchased(user)
        self.fields['object_pk'].queryset = qs

    helper = FormHelper()
    helper.form_class = 'share-form'
    helper.add_input(Submit('share', 'Share', css_class="btn-success "
                                                                 "btn-share"))

