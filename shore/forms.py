from django import forms
from django.core.validators import RegexValidator
from .models import FileType,Origin

A0 ='A0'
B1 ='B1'
TERMINAL_CHOICES = (
		(A0, 'A0-LCMT'),
		(B1, 'B1-LCB1'),
	)


class UploadFileForm(forms.Form):
	terminal = forms.ChoiceField(choices=TERMINAL_CHOICES,initial='B1')
	filetype = forms.ModelChoiceField(queryset= FileType.objects.filter(status='A'), empty_label="(Please select File Type)")
	origin 	 = forms.ModelChoiceField(queryset= Origin.objects.all().order_by('name'), empty_label="(Please select Origin)",required=False,)
	file = forms.FileField()