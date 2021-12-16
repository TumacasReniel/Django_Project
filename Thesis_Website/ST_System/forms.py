from typing import Type
from django import forms
from django.forms import ModelForm

from .models import *


class tsForm(forms.ModelForm):
	class Meta:
		model = ticket_statuses
		fields = '__all__'
		
class depForm(forms.ModelForm):
	class Meta:
		model = departments
		fields = '__all__'

class catForm(forms.ModelForm):
	class Meta:
		model = categories
		fields = ('category_name',)

class subcForm(forms.ModelForm):
	class Meta:
		model = sub_categories
		fields = ('sub_category_name',)


class ticketForm(forms.ModelForm):
	class Meta:
		model = tickets
		fields = '__all__'
		
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['category'].queryset = categories.objects.none()
		self.fields['sub_category'].queryset = sub_categories.objects.none()

		if 'department' in self.data:
			department_id = int(self.data.get('department'))
			self.fields['category'].queryset = categories.objects.filter(department_id=department_id)
		elif self.instance.pk:
			self.fields['category'].queryset = self.instance.department.category_set

		if 'category' in self.data:
			category_id = int(self.data.get('category'))
			self.fields['sub_category'].queryset = sub_categories.objects.filter(category_id=category_id)
		elif self.instance.pk:
			self.fields['sub_category'].queryset = self.instance.category.sub_category_set
   

		
    
        
      


		