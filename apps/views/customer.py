# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# 
# Author: Arif Dzikrullah
#         ardzix@hotmail.com
# 
# File Created: Thursday, 11th January 2018 1:01:02 pm
# Last Modified: Thursday, 11th January 2018 1:03:46 pm
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
from apps.models import Customer

class CustomerView(ProtectedMixin, TemplateView):
    template_name = "customer/index.html"
    
    def get(self, request):
        
        if request.GET.get('draw', None) != None:
            return self.datatable(request)

        return self.render_to_response({})


    def delete(self, request):
        id62 = request.body.split("=")[1]
        qs = Customer.objects.filter(id62__exact = id62).first()
        qs.delete()
        return self.render_to_response({})

    def datatable(self, request):
        qs = Customer.objects.filter(
            deleted_at__isnull = True
        )

        defer = ['id62', 'created_by', 'created_at']

        d = Datatable(request, qs, defer)
        return d.get_data()