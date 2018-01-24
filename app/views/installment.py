# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# 
# Author: Arif Dzikrullah
#         ardzix@hotmail.com
# 
# File Created: Sunday, 14th January 2018 3:38:34 pm
# Last Modified: Wednesday, 24th January 2018 11:13:46 am
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
from app.models import Installment

class InstallmentView(ProtectedMixin, TemplateView):
    template_name = "installment/index.html"
    
    def get(self, request):
        
        if request.GET.get('draw', None) != None:
            return self.datatable(request)

        return self.render_to_response({})


    def delete(self, request):
        id62 = request.body.split("=")[1]
        qs = Installment.objects.filter(id62__exact = id62).first()
        qs.delete()
        return self.render_to_response({})

    def datatable(self, request):
        qs = Installment.objects.filter(
            deleted_at__isnull = True
        )

        defer = ['id62', 'purchase', 'customer', 'order', 'created_at']

        d = Datatable(request, qs, defer)
        d.set_method_defer([{'origin':"purchase",'method':"__unicode__"}])
        d.set_lookup_defer(['volume__display_name', 'customer__created_by__first_name'])

        return d.get_data()
