# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# 
# Author: Arif Dzikrullah
#         ardzix@hotmail.com
# 
# File Created: Saturday, 10th March 2018 4:19:59 pm
# Last Modified: Sunday, 11th March 2018 12:09:52 am
# Modified By: Arif Dzikrullah (ardzix@hotmail.com)
# 
# Give the best to the world
# Copyright - 2018 Ardz.Co
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import datetime
from django.views.generic import TemplateView
from django.contrib import messages
from django.shortcuts import redirect, reverse, get_object_or_404
from libs.view import ProtectedMixin
from datatable import Datatable
from libs.json_response import JSONResponse
from app.models import Finance, Installment, Customer

def get_date_filter_request(qs, request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    if start_date == "null":
        start_date = None
    if end_date == "null":
        end_date = None

    if start_date:
        qs = qs.filter(created_at__gte=start_date)
    if end_date:
        qs = qs.filter(created_at__lte=end_date)

    if not start_date and not end_date:
        qs = qs[0:100]
    
    return qs
    

class FinanceReportView(ProtectedMixin, TemplateView):
    template_name = "report/index.html"

    def get(self, request, *args, **kwargs):
        qs = Finance.objects.filter(deleted_at__isnull=True)
        qs = get_date_filter_request(qs, request)

        table = {
            'title' : "Keuangan",
            'head' : ["No", "ID", "Tanggal", "Deskripsi", "Nilai", "Lampiran"],
            'rows' : []
        }

        total = 0
        for k,v in enumerate(qs):
            row = [
                k+1, 
                v.id62, 
                v.created_at, 
                v.description, 
                v.value, 
                v.content_object
            ]
            table['rows'].append(row)
            total += v.value

        table['foot'] = ["","","","Jumlah","Rp. "+"{:,}".format(total),""]

        return self.render_to_response({'table':table})


class InstallmentReportView(ProtectedMixin, TemplateView):
    template_name = "report/index.html"

    def get(self, request, *args, **kwargs):
        qs = Installment.objects.filter(deleted_at__isnull=True)
        qs = get_date_filter_request(qs, request)        


class CustomerReportView(ProtectedMixin, TemplateView):
    template_name = "report/index.html"

    def get(self, request, *args, **kwargs):
        qs = Customer.objects.filter(deleted_at__isnull=True)
        qs = get_date_filter_request(qs, request)
        