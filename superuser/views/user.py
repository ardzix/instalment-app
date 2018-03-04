# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Project panel.helloyuna.io
# 
# Author: Arif Dzikrullah
#         arif@helloyuna.io
#         ardzix@hotmail.com
#         http://ardz.xyz
# 
# File Created: Thursday, 1st March 2018 1:56:43 pm
# Last Modified: Sunday, 4th March 2018 6:03:42 pm
# Modified By: Arif Dzikrullah (ardzix@hotmail.com)
# 
# Hand-crafted & Made with Love
# Copyright - 2017 Yuna & Co, https://helloyuna.io
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from __future__ import unicode_literals

from django.views.generic import TemplateView
from django.shortcuts import redirect 
from django.contrib import messages
from django.contrib.auth.models import User
from libs.view import ProtectedMixin
from libs.datatable import Datatable
from ..forms import UserForm


class UserView(ProtectedMixin, TemplateView):
    template_name = "superuser/user.html"

    def get(self, request, *args, **kwargs):

        if request.GET.get('draw', None) != None:
            return self.datatable(request)

        return self.render_to_response({})

    def delete(self, request):
        o_id = request.body.split("=")[1]
        qs = User.objects.filter(id__exact = o_id).first()
        qs.delete()
        return self.render_to_response({})

    def datatable(self, request):
        qs = User.objects.all()
        defer = ['id', 'username', 'first_name', 'last_name', 'date_joined']

        d = Datatable(request, qs, defer, key="id")
        return d.get_data()


class UserFormView(ProtectedMixin, TemplateView):
    template_name = "superuser/user.form.html"

    def get(self, request, *args, **kwargs):
        edit = request.GET.get("edit")

        if edit:
            user = User.objects.get(id=edit)
            form = UserForm(instance=user, initial={'groups':user.groups.all()})
        else:
            form = UserForm()

        return self.render_to_response({"form":form})

    def post(self, request):
        edit = request.GET.get("edit")

        if edit:
            form = UserForm(request.POST, instance=User.objects.get(id=edit))
        else:
            form = UserForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            if request.POST.get("password") and request.POST.get("password") != "":
                user.set_password(request.POST.get("password"))
            
            user.save()
            user.groups = form.cleaned_data['groups']
            user.save()
            messages.success(request, 'User (%s) has been saved.' % user.username)
            return redirect("superuser:user")
        else:
            return self.render_to_response({"form":form})