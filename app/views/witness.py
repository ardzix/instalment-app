# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# 
# Author: Arif Dzikrullah
#         ardzix@hotmail.com
# 
# File Created: Sunday, 14th January 2018 3:27:04 pm
# Last Modified: Wednesday, 7th February 2018 8:24:52 pm
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
from app.models import Witness
from app.forms import WitnessForm

class WitnessView(ProtectedMixin, TemplateView):
    template_name = "witness/index.html"
    
    def get(self, request):
        
        if request.GET.get('draw', None) != None:
            return self.datatable(request)

        return self.render_to_response({})


    def delete(self, request):
        id62 = request.body.split("=")[1]
        qs = Witness.objects.filter(id62__exact = id62).first()
        qs.delete()
        return self.render_to_response({})

    def datatable(self, request):
        qs = Witness.objects.filter(
            deleted_at__isnull = True
        )

        defer = ['id62', 'fullname', 'id_num', 'address', 'created_at']

        d = Datatable(request, qs, defer)
        return d.get_data()


class WitnessFormView(ProtectedMixin, TemplateView):
    template_name = "witness/form.html"
    
    def get(self, request):
        edit = request.GET.get("edit")

        if edit:
            instance = Witness.objects.get(id62=edit)
            form = WitnessForm(instance=instance)
        else:
            form = WitnessForm()

        return self.render_to_response({"form":form})

    def post(self, request):
        edit = request.GET.get("edit")

        if edit:
            instance = Witness.objects.get(id62=edit)
            form = WitnessForm(request.POST, instance=instance)
        else:
            form = WitnessForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            if edit:
                obj.updated_by = request.user
            else:
                obj.created_by = request.user
            obj.save()
            messages.success(request, '%s (%s) has been saved.' % (obj.__class__.__name__, obj.fullname))

            return redirect(
                reverse("app:witness")
            )
        else:
            print form.errors

        return self.render_to_response({"form":form})
