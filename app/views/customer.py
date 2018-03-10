# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# 
# Author: Arif Dzikrullah
#         ardzix@hotmail.com
# 
# File Created: Thursday, 11th January 2018 1:01:02 pm
# Last Modified: Saturday, 10th March 2018 4:10:43 pm
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
from libs.json_response import JSONResponse
from datatable import Datatable
from app.models import Customer
from app.forms import CustomerForm, UserForm
from datetime import datetime

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


class CustomerFormView(ProtectedMixin, TemplateView):
    template_name = "customer/form.html"
    
    def get(self, request):
        edit = request.GET.get("edit")

        if edit:
            c = Customer.objects.get(id62=edit)
            c_form = CustomerForm(instance=c)
            u_form = UserForm(instance=User.objects.get(id=c.created_by_id))
        else:
            c_form = CustomerForm()
            u_form = UserForm()

        return self.render_to_response({"form":{'user':u_form, 'customer':c_form}})

    def post(self, request):
        edit = request.GET.get("edit")

        if edit:
            c = Customer.objects.get(id62=edit)
            c_form = CustomerForm(request.POST, instance=c)
            u_form = UserForm(request.POST, instance=User.objects.get(id=c.created_by_id))
        else:
            c_form = CustomerForm(request.POST)
            u_form = UserForm(request.POST)

        if u_form.is_valid():
            user = u_form.save(commit=False)
            user.date_joined = datetime.now()
            user.set_password(request.POST.get("password"))
            user.is_staff = False
            user.is_active = True

            if c_form.is_valid():
                user.save()                
                customer = c_form.save(commit=False)
                if edit:
                    customer.updated_by = request.user
                else:
                    customer.created_by = user
                customer.save()

                messages.success(request, 'Customer (%s %s) has been saved.' % (user.first_name, user.last_name))
                
                return redirect(
                    reverse("app:customer")
                )
            else:
                print c_form.errors
        else:
            print u_form.errors

        return self.render_to_response({"form":{'user':u_form, 'customer':c_form}})