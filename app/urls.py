# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# 
# Author: Arif Dzikrullah
#         ardzix@hotmail.com
# 
# File Created: Thursday, 11th January 2018 12:59:20 pm
# Last Modified: Thursday, 11th January 2018 3:34:16 pm
# Modified By: Arif Dzikrullah (ardzix@hotmail.com)
# 
# Give the best to the world
# Copyright - 2018 Ardz.Co
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from django.conf.urls import url
from app.views.customer import *

urlpatterns = [
    url(r'^customer/$', CustomerView.as_view(), name='customer'),
    url(r'^customer/form/$', CustomerView.as_view(), name='customer-form'),
]