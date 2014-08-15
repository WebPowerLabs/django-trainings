from django import forms
from lessons.models import Lesson
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, ButtonHolder, Field,\
    Div, HTML
from django.core.files.storage import default_storage
import os
from django.core.files.uploadedfile import InMemoryUploadedFile


class LessonCreateFrom(forms.ModelForm):
    video = forms.FileField(required=False)
    video_path = forms.CharField(required=False, widget=forms.HiddenInput())
    

    helper = FormHelper()
    helper.layout = Layout(Fieldset(
            '',
            'name',
            'description',
            'published',
            'thumbnail',
            Field('video',
                  data_url='/lessons/upload_video/',
                  css_class='fileuploader'),
                  HTML("""
                      <div class="hidden progress progress-striped active"
                      role="progressbar" aria-valuemin="0" aria-valuemax="100"
                      aria-valuenow="0">
                      <div class="progress-bar progress-bar-success"
                      style="width:0%;"></div></div>"""),
                                    
                                    
                                    
#             Div(
#                 Div(
#                     css_class="progress-bar progress-bar-success",
#                     style="width:0%;", ),
#                 css_class='hidden progress progress-striped active form-group',
#                 role='progressbar',
#                 aria_valuemin='0',
#                 aria_valuemax="100",
#                 aria_valuenow="0",
#                 ),
            'video_path',
            'audio',
            'homework',
            'tags'),
            ButtonHolder(Submit('save_changes',
                                'Save changes',
                                css_class="btn-success")))
    
        
#     def clean_video(self):
#         import pdb;pdb.set_trace()
#          
#         return self.cleaned_data
    
    class Meta:
        model = Lesson
        exclude = ['owner', 'course']
        
        
