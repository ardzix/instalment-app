# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# 
# Author: Arif Dzikrullah
#         ardzix@hotmail.com
# 
# File Created: Sunday, 14th January 2018 3:43:47 pm
# Last Modified: Sunday, 14th January 2018 3:44:10 pm
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
from app.models import Finance

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
