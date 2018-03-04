# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Project panel.helloyuna.io
# 
# Author: Arif Dzikrullah
#         arif@helloyuna.io
#         ardzix@hotmail.com
#         http://ardz.xyz
# 
# File Created: Tuesday, 16th January 2018 12:11:53 pm
# Last Modified: Saturday, 3rd March 2018 8:14:53 pm
# Modified By: Arif Dzikrullah (ardzix@hotmail.com)
# 
# Hand-crafted & Made with Love
# Copyright - 2017 Yuna & Co, https://helloyuna.io
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from django.forms import *
from django.conf import settings
from models import *
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType


class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = {
            'name' :  models.CharField(max_length=255),
            'permissions' : ModelMultipleChoiceField(
                    queryset = Permission.objects.all(),
                )
        }

        widgets = {
            'name': TextInput(attrs={'class':'form-control'}),
            'permissions': SelectMultiple(attrs={'class':'form-control select2'}),
        }

class PermissionForm(ModelForm):
    class Meta:
        model = Permission
        fields = {
            'name' :  models.CharField(max_length=255),
            'codename' :  models.CharField(max_length=255),
            'content_type' : ModelChoiceField(
                    queryset = ContentType.objects.all(),
                )
        }

        widgets = {
            'name': TextInput(attrs={'class':'form-control'}),
            'codename': TextInput(attrs={'class':'form-control'}),
            'content_type': Select(attrs={'class':'form-control select2'}),
        }
    

class UserForm(ModelForm):
    password = CharField(required=False)
    password.widget = TextInput(attrs={'class':'form-control'})

    groups = ModelMultipleChoiceField(
        required = False,
        queryset = Group.objects.all(),
        widget = SelectMultiple(attrs={'class':'form-control select2'}),
    )

    class Meta:
        model = User
        exclude = ('date_joined', 'password',)        
        widgets = {
            'username': TextInput(attrs={'class':'form-control'}),
            'first_name': TextInput(attrs={'class':'form-control'}),
            'last_name': TextInput(attrs={'class':'form-control'}),
            'email': EmailInput(attrs={'class':'form-control'}),
        }