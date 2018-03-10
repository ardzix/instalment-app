# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# 
# Author: Arif Dzikrullah
#         ardzix@hotmail.com
# 
# File Created: Sunday, 14th January 2018 3:31:19 pm
# Last Modified: Saturday, 10th March 2018 4:12:50 pm
# Modified By: Arif Dzikrullah (ardzix@hotmail.com)
# 
# Give the best to the world
# Copyright - 2018 Ardz.Co
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++


from django.views.generic import TemplateView
from django.contrib import messages
from django.shortcuts import redirect, reverse, get_object_or_404
from libs.view import ProtectedMixin
from datatable import Datatable
from libs.json_response import JSONResponse
from app.models import File
from app.forms import FileForm

class FileView(ProtectedMixin, TemplateView):
    template_name = "file/index.html"
    
    def get(self, request):
        
        if request.GET.get('draw', None) != None:
            return self.datatable(request)

        return self.render_to_response({})


    def delete(self, request):
        id62 = request.body.split("=")[1]
        qs = File.objects.filter(id62__exact = id62).first()
        qs.delete()
        return self.render_to_response({})

    def datatable(self, request):
        qs = File.objects.filter(
            deleted_at__isnull = True
        )

        defer = ['id62', 'display_name', 'manager', 'created_at']

        d = Datatable(request, qs, defer)
        d.set_method_defer([{'origin':"manager",'method':"get_url"}])
        
        return d.get_data()


class FileFormView(ProtectedMixin, TemplateView):
    template_name = "file/form.html"
    
    def get(self, request):
        edit = request.GET.get("edit")

        if edit:
            instance = File.objects.get(id62=edit)
            form = FileForm(instance=instance)
        else:
            form = FileForm()

        return self.render_to_response({"form":form})

    def post(self, request):
        edit = request.GET.get("edit")

        if edit:
            instance = File.objects.get(id62=edit)
            form = FileForm(request.POST, instance=instance)
        else:
            form = FileForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            if edit:
                obj.updated_by = request.user
            else:
                obj.created_by = request.user

            print request.FILES.get("manager")
            if request.FILES.get("manager"):
                obj.manager = request.FILES.get("manager")

            print obj.manager

            obj.save()
            messages.success(request, '%s (%s) has been saved.' % (obj.__class__.__name__, obj.display_name))

            return redirect(
                reverse("app:file")
            )
        else:
            print form.errors

        return self.render_to_response({"form":form})
