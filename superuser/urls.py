# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Project panel.helloyuna.io
# 
# Author: Arif Dzikrullah
#         arif@helloyuna.io
#         ardzix@hotmail.com
#         http://ardz.xyz
# 
# File Created: Monday, 15th January 2018 3:41:42 pm
# Last Modified: Saturday, 3rd March 2018 7:34:48 pm
# Modified By: Arif Dzikrullah (ardzix@hotmail.com)
# 
# Hand-crafted & Made with Love
# Copyright - 2017 Yuna & Co, https://helloyuna.io
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from views.group import *
from views.permission import *
from views.user import *

urlpatterns = [
    # url(r'^admin/', admin.site.urls),

    # Group
    url(r'^group/$', GroupView.as_view(), name='group'),
    url(r'^group/form/$', GroupFormView.as_view(), name='group-form'),

    url(r'^permission/$', PermissionView.as_view(), name='permission'),
    url(r'^permission/form/$', PermissionFormView.as_view(), name='permission-form'),

    url(r'^user/$', UserView.as_view(), name='user'),
    url(r'^user/form/$', UserFormView.as_view(), name='user-form'),
]
