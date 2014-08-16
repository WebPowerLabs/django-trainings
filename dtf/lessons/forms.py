from django import forms
from lessons.models import Lesson
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, ButtonHolder, HTML


class LessonCreateFrom(forms.ModelForm):
    video_path = forms.CharField(required=False, widget=forms.HiddenInput())
    helper = FormHelper()
    helper.layout = Layout(Fieldset(
                '',
                'name',
                'description',
                'published',
                'thumbnail',
                HTML("""<div id="div_id_video" class="form-group">
                            <label for="id_video">Video</label><br />
                            <span class="btn btn-success fileinput-button">
                                <i class="fa fa-plus"></i>&nbsp;
                                <span class="fileinput-title">Select video file...</span>
                                <input id="id_video" type="file" name="video"
                                    data-url="{% url 'lessons:upload_video' %}"
                                    class="fileuploader">
                            </span>
                            <span class="btn btn-danger fileinput-remove hidden">
                                <i class="fa fa-times"></i>&nbsp;
                                <span class="fileinput-title">Remove </span>
                            </span>
                            <div class="hidden progress progress-striped active"
                                role="progressbar" aria-valuemin="0"
                                aria-valuemax="100" aria-valuenow="0">
                            <div class="progress-bar progress-bar-success"
                                style="width:0%;"></div></div></div>"""),
                'video_path',
                'audio',
                'homework',
                'tags'),
                ButtonHolder(Submit('save_changes',
                                    'Save changes',
                                    css_class="btn-success")))

    class Meta:
        model = Lesson
        exclude = ['owner', 'course']