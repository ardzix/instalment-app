# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# 
# Author: Arif Dzikrullah
#         ardzix@hotmail.com
# 
# File Created: Thursday, 11th January 2018 3:43:19 pm
# Last Modified: Saturday, 10th March 2018 4:12:44 pm
# Modified By: Arif Dzikrullah (ardzix@hotmail.com)
# 
# Give the best to the world
# Copyright - 2018 Ardz.Co
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from django.views.generic import TemplateView
from django.contrib import messages
from django.shortcuts import redirect, reverse, get_object_or_404
from libs.view import ProtectedMixin
from datatable import Datatable
from libs.json_response import JSONResponse
from app.models import Facility
from app.forms import FacilityForm

class FacilityView(ProtectedMixin, TemplateView):
    template_name = "facility/index.html"
    
    def get(self, request):
        
        if request.GET.get('draw', None) != None:
            return self.datatable(request)

        return self.render_to_response({})


    def delete(self, request):
        id62 = request.body.split("=")[1]
        qs = Facility.objects.filter(id62__exact = id62).first()
        qs.delete()
        return self.render_to_response({})

    def datatable(self, request):
        qs = Facility.objects.filter(
            deleted_at__isnull = True
        )

        defer = ['id62', 'display_name', 'description', 'created_at']

        d = Datatable(request, qs, defer)
        return d.get_data()


class FacilityFormView(ProtectedMixin, TemplateView):
    template_name = "facility/form.html"
    
    def get(self, request):
        edit = request.GET.get("edit")

        if edit:
            instance = Facility.objects.get(id62=edit)
            form = FacilityForm(instance=instance)
        else:
            form = FacilityForm()

        return self.render_to_response({"form":form})

    def post(self, request):
        edit = request.GET.get("edit")

        if edit:
            instance = Facility.objects.get(id62=edit)
            form = FacilityForm(request.POST, instance=instance)
        else:
            form = FacilityForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            if edit:
                obj.updated_by = request.user
            else:
                obj.created_by = request.user
            obj.save()
            messages.success(request, '%s (%s) has been saved.' % (obj.__class__.__name__, obj.display_name))

            return redirect(
                reverse("app:facility")
            )
        else:
            print form.errors

        return self.render_to_response({"form":form})