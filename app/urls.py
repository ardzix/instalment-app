# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# 
# Author: Arif Dzikrullah
#         ardzix@hotmail.com
# 
# File Created: Thursday, 11th January 2018 12:59:20 pm
# Last Modified: Thursday, 25th January 2018 11:36:28 am
# Modified By: Arif Dzikrullah (ardzix@hotmail.com)
# 
# Give the best to the world
# Copyright - 2018 Ardz.Co
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from django.conf.urls import url
from app.views.customer import *
from app.views.facility import *
from app.views.volume import *
from app.views.witness import *
from app.views.file import *
from app.views.purchase import *
from app.views.installment import *
from app.views.finance import *

urlpatterns = [
    url(r'^customer/$', CustomerView.as_view(), name='customer'),
    url(r'^customer/form/$', CustomerFormView.as_view(), name='customer-form'),

    url(r'^facility/$', FacilityView.as_view(), name='facility'),
    url(r'^facility/form/$', FacilityView.as_view(), name='facility-form'),

    url(r'^volume/$', VolumeView.as_view(), name='volume'),
    url(r'^volume/form/$', VolumeView.as_view(), name='volume-form'),

    url(r'^witness/$', WitnessView.as_view(), name='witness'),
    url(r'^witness/form/$', WitnessView.as_view(), name='witness-form'),

    url(r'^file/$', FileView.as_view(), name='file'),
    url(r'^file/form/$', FileView.as_view(), name='file-form'),

    url(r'^purchase/$', PurchaseView.as_view(), name='purchase'),
    url(r'^purchase/form/$', PurchaseView.as_view(), name='purchase-form'),

    url(r'^installment/$', InstallmentView.as_view(), name='installment'),
    url(r'^installment/form/$', InstallmentView.as_view(), name='installment-form'),

    url(r'^finance/$', FinanceView.as_view(), name='finance'),
    url(r'^finance/form/$', FinanceView.as_view(), name='finance-form'),

    url(r'^$', CustomerView.as_view(), name='dashboard'),
]