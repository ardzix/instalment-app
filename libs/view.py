# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# 
# Author: Arif Dzikrullah
#         ardzix@hotmail.com
# 
# File Created: Tuesday, 10th October 2017 11:57:20 am
# Last Modified: Sunday, 4th March 2018 5:04:56 pm
# Modified By: Arif Dzikrullah (ardzix@hotmail.com)
# 
# Give the best to the world
# Copyright - 2018 Ardz.Co
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from django.core.exceptions import PermissionDenied
from django.views.defaults import permission_denied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect

class ProtectedMixin(LoginRequiredMixin):
    login_url = "/account/login/"
    name_space = None
    model = None
    
    def dispatch(self, request, *args, **kwargs):
        # If user not logged in, redirect to login page
        if not request.user.is_authenticated():
            return redirect("account:login")

        # If user is not staff nor super, 403 will be given
        if not (request.user.is_staff or request.user.is_superuser):
            return self.handle_no_permission(request, *args, **kwargs)

        # set app and model access for user to the request
        app_access = []
        model_access = []
        for ct_int in request.user.groups.distinct('permissions__content_type__model').values_list('permissions__content_type', flat = True):
            ct = ContentType.objects.filter(id=ct_int).first()
            if ct:
                if ct.app_label not in app_access:
                    app_access.append(ct.app_label)
                model_access.append("%s:%s" % (ct.app_label, ct.model))

        # Then store the app_access and model_access to the request            
        request.model_access = model_access

        print model_access
        
        if not self.name_space:
            self.name_space = request.resolver_match.namespace
        if not self.model:
            self.model = request.resolver_match.url_name.split("-")[0]

        if not self.permission_allowed(request):
            return self.handle_no_permission(request)

        
        return super(ProtectedMixin, self).dispatch(request, *args, **kwargs)

    def handle_no_permission(self, request):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return permission_denied(request, "403: you're not authorized to access this app")
    
    def get_permissions(self, request):
        return list(request.user.groups.distinct('permissions__codename').values_list('permissions__codename', flat=True).all())

    def permission_allowed(self, request):
        if request.user.is_superuser:
            return True

        edit = request.GET.get("edit")
        if request.method == "GET":
            if "view_"+self.model in self.get_permissions(request):
                return True
        elif edit and request.method == "POST":
            if "change_"+self.model in self.get_permissions(request):
                return True
        elif not edit and request.method == "POST":
            if "add_"+self.model in self.get_permissions(request):
                return True
        elif request.method == "DELETE":
            if "delete_"+self.model in self.get_permissions(request):
                return True

        return False