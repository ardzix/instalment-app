# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# 
# Author: Arif Dzikrullah
#         ardzix@hotmail.com
# 
# File Created: Sunday, 14th January 2018 3:43:47 pm
# Last Modified: Saturday, 10th March 2018 4:12:55 pm
# Modified By: Arif Dzikrullah (ardzix@hotmail.com)
# 
# Give the best to the world
# Copyright - 2018 Ardz.Co
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++


from django.views.generic import TemplateView
from django.shortcuts import redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from libs.view import ProtectedMixin
from datatable import Datatable
from libs.json_response import JSONResponse
from app.models import *
from app.forms import FinanceForm, FinanceCOForm

class FinanceView(ProtectedMixin, TemplateView):
    template_name = "finance/index.html"
    
    def get(self, request):
        
        if request.GET.get('draw', None) != None:
            return self.datatable(request)

        return self.render_to_response({})


    def delete(self, request):
        id62 = request.body.split("=")[1]
        qs = Finance.objects.filter(id62__exact = id62).first()
        qs.delete()
        return self.render_to_response({})

    def datatable(self, request):
        qs = Finance.objects.filter(
            deleted_at__isnull = True
        )

        defer = ['id62', 'description', 'created_at']

        d = Datatable(request, qs, defer)
        return d.get_data()


class FinanceFormView(ProtectedMixin, TemplateView):
    template_name = "finance/form.html"
    
    def get(self, request):
        edit = request.GET.get("edit")

        if edit:
            instance = Finance.objects.get(id62=edit)
            if instance.value < 0:
                initial = {"value":instance.value * (-1)}
            else:
                initial = {"type":2}
            form = FinanceForm(instance=instance, initial=initial)
        else:
            form = FinanceForm()

        return self.render_to_response({"form":form})

    def post(self, request):
        edit = request.GET.get("edit")

        if edit:
            instance = Finance.objects.get(id62=edit)
            form = FinanceForm(request.POST, instance=instance)
        else:
            form = FinanceForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            if edit:
                obj.updated_by = request.user
            else:
                obj.created_by = request.user

            obj.content_model = obj.content_type.model_class().__name__
            if request.POST.get("content_object") or not request.POST.get("content_object")== "":
                obj.object_id = request.POST.get("content_object")
            else:
                obj.object_id = None
            if request.POST.get("type") == "1":
                obj.value = obj.value * (-1)
            obj.save()
            messages.success(request, '%s (%s) has been saved.' % (obj.__class__.__name__, obj.__unicode__()))
            return redirect(
                reverse("app:finance")
            )
        else:
            print form.errors

        return self.render_to_response({"form":form})


class FinanceContentObjectAjaxView(ProtectedMixin, TemplateView):
    template_name = "finance/content_object-form.html"

    def get(self, request):
        edit = request.GET.get("edit")
        finance = None
        if edit:
            finance = Finance.objects.filter(id62=edit).first()

        # get content object form from content type
        ct_par = request.GET.get("content_type")
        ct = ContentType.objects.filter(id=ct_par).first()
        co = ct.model_class().objects.all()
        form = FinanceCOForm()
        form.fields['content_object'].queryset = co

        # if finance, initialize the field
        if finance:
            co = finance.content_object
            form.fields['content_object'].initial = co
            
        return self.render_to_response({"form":form})


