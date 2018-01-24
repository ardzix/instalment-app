# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# 
# Author: Arif Dzikrullah
#         ardzix@hotmail.com
# 
# File Created: Sunday, 14th January 2018 3:34:25 pm
# Last Modified: Wednesday, 24th January 2018 11:01:34 am
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
