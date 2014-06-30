from django import forms
from django.contrib.contenttypes.models import ContentType

from .models import Feature

class FeatureForm(forms.ModelForm):

	#content_type = forms.ChoiceField("ContentType")
	#object_pk = forms.HiddenField()
	#comment = forms.HiddenField()

	class Meta:
		model = Feature
		fields = ("content_type", "object_pk", "comment")

	def __init__(self, *args, **kwargs):
		super(FeatureForm, self).__init__(*args, **kwargs)

		self.fields["object_pk"].widget = forms.HiddenInput()
		self.fields["comment"].widget = forms.HiddenInput()