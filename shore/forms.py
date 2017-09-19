from django import forms
from django.core.validators import RegexValidator
from .models import FileType

class UploadFileForm(forms.Form):
	filetype = forms.ModelChoiceField(queryset= FileType.objects.filter(status='A'), empty_label="(Please select File Type)")
	file = forms.FileField()