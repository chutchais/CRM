from django import forms
from django.core.validators import RegexValidator
from .models import FileType

class UploadFileForm(forms.Form):
	filetype = forms.ModelChoiceField(queryset= FileType.objects.all(), empty_label="(Please select File Type)")
	file = forms.FileField()