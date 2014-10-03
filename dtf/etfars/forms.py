from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Fieldset, Field
from crispy_forms.bootstrap import FormActions

from .models import Etfar


class EtfarForm(forms.ModelForm):

    class Meta:
        model = Etfar
        fields = ('event', 'thought', 'feeling', 'action', 'result')

    def __init__(self, *args, **kwargs):
        super(EtfarForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class='etfar-form form-horizontal'
        self.helper.form_id = kwargs.get('form_id', 'etfar_tool')
        self.helper.label_class='col-md-3'
        self.helper.field_class='col-md-7'
        self.helper.form_action='.'
        self.helper.layout = Layout(
            Field('event', rows=2, placeholder=self.fields['event'].help_text),
            Field('thought', rows=2, placeholder=self.fields['thought'].help_text),
            Field('feeling', rows=2, placeholder=self.fields['feeling'].help_text),
            Field('action', rows=2, placeholder=self.fields['action'].help_text),
            Field('result', rows=2, placeholder=self.fields['result'].help_text),
            FormActions(
                        Submit('submit', 'Proceed', css_class='btn btn-primary')
                        )
            )