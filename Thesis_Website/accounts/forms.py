from django import forms
from django.forms import ModelForm
from .models import *



class userForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('first_name','last_name','username','email','status','department')

class agentForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('first_name','last_name','username','email','status','department')

class adminForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('first_name','last_name','username','email','status','department')

class assForm(forms.ModelForm):
	class Meta:
		model = agent_od
		fields = ('category','level')

class profileForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('profile_pic',)
	










       
