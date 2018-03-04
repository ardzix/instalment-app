# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Project panel.helloyuna.io
# 
# Author: Arif Dzikrullah
#         arif@helloyuna.io
#         ardzix@hotmail.com
#         http://ardz.xyz
# 
# File Created: Thursday, 1st March 2018 1:51:11 pm
# Last Modified: Saturday, 3rd March 2018 7:32:58 pm
# Modified By: Arif Dzikrullah (ardzix@hotmail.com)
# 
# Hand-crafted & Made with Love
# Copyright - 2017 Yuna & Co, https://helloyuna.io
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from __future__ import unicode_literals

from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import Group 
from libs.view import ProtectedMixin
from libs.datatable import Datatable
from ..forms import GroupForm


class GroupView(ProtectedMixin, TemplateView):
    template_name = "superuser/group.html"

    def get(self, request, *args, **kwargs):

        if request.GET.get('draw', None) != None:
            return self.datatable(request)

        return self.render_to_response({})

    def delete(self, request):
        o_id = request.body.split("=")[1]
        qs = Group.objects.filter(id__exact = o_id).first()
        qs.delete()
        return self.render_to_response({})

    def datatable(self, request):
        def get_permission_list(self):
            return " | ".join(self.permissions.values_list("name", flat=True))
        
        Group.add_to_class("get_permission_list",get_permission_list)
        qs = Group.objects.all()
        defer = ['id', 'name', 'get_permission_list']

        d = Datatable(request, qs, defer, key="id")
        return d.get_data()


class GroupFormView(ProtectedMixin, TemplateView):
    template_name = "superuser/group.form.html"

    def get(self, request, *args, **kwargs):
        edit = request.GET.get("edit")

        if edit:
            form = GroupForm(instance=Group.objects.get(id=edit))
        else:
            form = GroupForm()

        return self.render_to_response({"form":form})

    def post(self, request):
        edit = request.GET.get("edit")

        if edit:
            form = GroupForm(request.POST, instance=Group.objects.get(id=edit))
        else:
            form = GroupForm(request.POST)

        if form.is_valid():
            group = form.save(commit=False)
            group.save()            
            group.permissions = form.cleaned_data['permissions']
            group.save()
            messages.success(request, 'Group (%s) has been saved.' % group.name)
            return redirect("superuser:group")
        else:
            return self.render_to_response({"form":form})