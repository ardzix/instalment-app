# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# 
# Author: Arif Dzikrullah
#         ardzix@hotmail.com
# 
# File Created: Wednesday, 10th January 2018 11:37:22 pm
# Last Modified: Tuesday, 20th February 2018 9:45:41 pm
# Modified By: Arif Dzikrullah (ardzix@hotmail.com)
# 
# Give the best to the world
# Copyright - 2018 Ardz.Co
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from django.forms import *
from django.conf import settings
from app.models import *
from django.contrib.auth.models import User

class UserForm(ModelForm):
    password = CharField(required=False)
    password.widget = TextInput(attrs={'class':'form-control'})

    class Meta:
        model = User
        exclude = ('date_joined', 'password',)        
        widgets = {
            'username': TextInput(attrs={'class':'form-control'}),
            'first_name': TextInput(attrs={'class':'form-control'}),
            'last_name': TextInput(attrs={'class':'form-control'}),
            'email': EmailInput(attrs={'class':'form-control'}),
        }

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        exclude = settings.EXCLUDE_FORM_FIELDS + ("background_cover", "avatar")
        widgets = {
            'gender': Select(attrs={'class':'form-control select2'}),
            'id_num': TextInput(attrs={'class':'form-control'}),
            'phone': TextInput(attrs={'class':'form-control'}),
            'birthday': DateTimeInput(attrs={'class':'form-control'}),
            'birthplace': TextInput(attrs={'class':'form-control'}),
            'is_verified': CheckboxInput(attrs={'checked':'checked'}),
        }

class FacilityForm(ModelForm):
    class Meta:
        model = Facility
        exclude = settings.EXCLUDE_FORM_FIELDS
        widgets = {
            'display_name': TextInput(attrs={'class':'form-control'}),
            'short_name': TextInput(attrs={'class':'form-control'}),            
        }      

class VolumeForm(ModelForm):
    class Meta:
        model = Volume
        exclude = settings.EXCLUDE_FORM_FIELDS
        widgets = {
            'display_name': TextInput(attrs={'class':'form-control'}),
            'short_name': TextInput(attrs={'class':'form-control'}),            
            'area_wide': NumberInput(attrs={'class':'form-control'}),            
        }       

class WitnessForm(ModelForm):
    class Meta:
        model = Witness
        exclude = settings.EXCLUDE_FORM_FIELDS
        widgets = {
            'fullname': TextInput(attrs={'class':'form-control'}),
            'id_num': TextInput(attrs={'class':'form-control'}),            
        }           

class FileForm(ModelForm):
    class Meta:
        model = File
        exclude = settings.EXCLUDE_FORM_FIELDS
        widgets = {
            'display_name': TextInput(attrs={'class':'form-control'}),
            'short_name': TextInput(attrs={'class':'form-control'}),            
        }        