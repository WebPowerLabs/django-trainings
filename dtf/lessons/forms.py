from django import forms
from lessons.models import Lesson
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, ButtonHolder, HTML


class LessonCreateFrom(forms.ModelForm):
    video_path = forms.CharField(required=False, widget=forms.HiddenInput())
    video_pk = forms.CharField(required=False, widget=forms.HiddenInput())
    helper = FormHelper()
    helper.layout = Layout(Fieldset(
                '',
                'name',
                'description',
                'published',
                'thumbnail',
                HTML("""<div id="div_id_video" class="form-group">
                          <label for="id_video">Video</label><br />
                          <span class="btn btn-primary fileinput-button
                          {% if object.video %} hidden{% endif %}">
                            <i class="fa fa-plus"></i>&nbsp;
                            <span class="fileinput-title">
                              Select video file
                            </span>
                            <input id="id_video" type="file" name="video"
                            data-url="{% url 'lessons:upload_video_file' %}"
                            class="fileuploader">
                          </span>
                          <span class="btn btn-danger fileinput-button-remove
                          {% if not object.video %} hidden{% endif %}">
                            <i class="fa fa-times"></i>&nbsp;
                            <span class="fileinput-title">
                              Remove {{ object.video.filename }}
                            </span>
                          </span>
                        </div>
                        <div class="hidden progress active progress-striped"
                        role="progressbar" aria-valuemax="100"
                        aria-valuemin="0" aria-valuenow="0">
                          <div class="progress-bar progress-bar-success"
                          style="width:0%;"></div></div>"""),
                'video_path',
                'video_pk',
                'audio',
                'homework',
                'tags'),
                ButtonHolder(Submit('save_changes',
                                    'Save changes',
                                    css_class="btn-success")))

    class Meta:
        model = Lesson
        exclude = ['owner', 'course']
        
    def __init__(self, *args, **kwargs):
        super(LessonCreateFrom, self).__init__(*args, **kwargs)
        if self.instance.video:
            self.fields['video_pk'].initial = self.instance.video.id
