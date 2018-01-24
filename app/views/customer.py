# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# 
# Author: Arif Dzikrullah
#         ardzix@hotmail.com
# 
# File Created: Thursday, 11th January 2018 1:01:02 pm
# Last Modified: Wednesday, 24th January 2018 10:25:26 am
# Modified By: Arif Dzikrullah (ardzix@hotmail.com)
# 
# Give the best to the world
# Copyright - 2018 Ardz.Co
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from django.views.generic import TemplateView
from django.contrib import messages
from django.shortcuts import redirect, reverse, get_object_or_404
from django.contrib.auth.models import User
from libs.view import ProtectedMixin
from libs.datatable import Datatable
from libs.json_response import JSONResponse
from app.models import Customer

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

        defer = ['id62', 'created_by', 'id_num', 'phone', 'created_at']

        d = Datatable(request, qs, defer)
        d.set_lookup_defer(['created_by__first_name'])
        
        return d.get_data()