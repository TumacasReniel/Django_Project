from typing import Type
from django import forms
from django.forms import ModelForm

from .models import *

class notiForm(forms.ModelForm):
	class Meta:
		model = Notification
		fields = ('is_seen',)