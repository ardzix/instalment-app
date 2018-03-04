# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Project panel.helloyuna.io
# 
# Author: Arif Dzikrullah
#         arif@helloyuna.io
#         ardzix@hotmail.com
#         http://ardz.xyz
# 
# File Created: Thursday, 1st March 2018 1:56:43 pm
# Last Modified: Saturday, 3rd March 2018 7:33:05 pm
# Modified By: Arif Dzikrullah (ardzix@hotmail.com)
# 
# Hand-crafted & Made with Love
# Copyright - 2017 Yuna & Co, https://helloyuna.io
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from __future__ import unicode_literals

from django.views.generic import TemplateView
from django.shortcuts import redirect 
from django.contrib import messages
from django.contrib.auth.models import Permission
from libs.view import ProtectedMixin
from libs.datatable import Datatable
from ..forms import PermissionForm


class PermissionView(ProtectedMixin, TemplateView):
    template_name = "superuser/permission.html"

    def get(self, request, *args, **kwargs):

        if request.GET.get('draw', None) != None:
            return self.datatable(request)

        return self.render_to_response({})

    def delete(self, request):
        o_id = request.body.split("=")[1]
        qs = Permission.objects.filter(id__exact = o_id).first()
        qs.delete()
        return self.render_to_response({})

    def datatable(self, request):
        qs = Permission.objects.all()
        defer = ['id', 'name', 'codename', 'content_type']

        d = Datatable(request, qs, defer, key="id")
        return d.get_data()


class PermissionFormView(ProtectedMixin, TemplateView):
    template_name = "superuser/permission.form.html"

    def get(self, request, *args, **kwargs):
        edit = request.GET.get("edit")

        if edit:
            form = PermissionForm(instance=Permission.objects.get(id=edit))
        else:
            form = PermissionForm()

        return self.render_to_response({"form":form})

    def post(self, request):
        edit = request.GET.get("edit")

        if edit:
            form = PermissionForm(request.POST, instance=Permission.objects.get(id=edit))
        else:
            form = PermissionForm(request.POST)

        if form.is_valid():
            permission = form.save(commit=False)
            permission.save()
            messages.success(request, 'Permission (%s) has been saved.' % permission.name)
            return redirect("superuser:permission")
        else:
            return self.render_to_response({"form":form})