# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# 
# Author: Arif Dzikrullah
#         ardzix@hotmail.com
# 
# File Created: Sunday, 14th January 2018 3:34:25 pm
# Last Modified: Tuesday, 20th February 2018 10:27:47 pm
# Modified By: Arif Dzikrullah (ardzix@hotmail.com)
# 
# Give the best to the world
# Copyright - 2018 Ardz.Co
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++


from django.views.generic import TemplateView
from django.contrib import messages
from django.shortcuts import redirect, reverse, get_object_or_404
from libs.view import ProtectedMixin
from libs.datatable import Datatable
from libs.json_response import JSONResponse
from app.models import Purchase
from app.forms import PurchaseForm

class PurchaseView(ProtectedMixin, TemplateView):
    template_name = "purchase/index.html"
    
    def get(self, request):
        
        if request.GET.get('draw', None) != None:
            return self.datatable(request)

        return self.render_to_response({})


    def delete(self, request):
        id62 = request.body.split("=")[1]
        qs = Purchase.objects.filter(id62__exact = id62).first()
        qs.delete()
        return self.render_to_response({})

    def datatable(self, request):
        qs = Purchase.objects.filter(
            deleted_at__isnull = True
        )

        defer = ['id62', 'volume', 'customer', 'address', 'area_wide', 'created_at']

        d = Datatable(request, qs, defer)
        d.set_lookup_defer(['volume__display_name', 'customer__created_by__first_name'])
        return d.get_data()


class PurchaseFormView(ProtectedMixin, TemplateView):
    template_name = "purchase/form.html"
    
    def get(self, request):
        edit = request.GET.get("edit")

        if edit:
            instance = Purchase.objects.get(id62=edit)
            form = PurchaseForm(instance=instance)
        else:
            form = PurchaseForm()

        return self.render_to_response({"form":form})

    def post(self, request):
        edit = request.GET.get("edit")

        if edit:
            instance = Purchase.objects.get(id62=edit)
            form = PurchaseForm(request.POST, instance=instance)
        else:
            form = PurchaseForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            if edit:
                obj.updated_by = request.user
            else:
                obj.created_by = request.user

            obj.witnesses = form.cleaned_data['witnesses']
            obj.facilities = form.cleaned_data['facilities']
            obj.files = form.cleaned_data['files']
                
            obj.save()
            messages.success(request, '%s (%s) has been saved.' % (obj.__class__.__name__, obj.__unicode__()))

            return redirect(
                reverse("app:purchase")
            )
        else:
            print form.errors

        return self.render_to_response({"form":form})